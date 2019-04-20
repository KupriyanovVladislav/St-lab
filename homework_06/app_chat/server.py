from psycopg2 import connect

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.options
from tornado.log import enable_pretty_logging

# settings for connecting to database
setting_dict = {}


def run_db(setting_dict: dict):
    with connect(**setting_dict) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE message
            (
            message_id SERIAL PRIMARY KEY,
            message_user VARCHAR(30) NOT NULL,
            message_content VARCHAR NOT NULL,
            message_room INT NOT NULL            
            )
            """
        )
    conn.close()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html', name='', room='', error='')

    def post(self):
        error = ''
        name = self.get_body_argument('name')
        room = self.get_body_argument('room')
        if name == 'ADMIN' and int(room) == 11:
            return self.redirect(f'/{room}/{name}/')

        if isinstance(name, str) and 1 <= int(room) <= 10:
            return self.redirect(f'/{room}/{name}/')

        elif not (isinstance(name, str)):
            error = 'Недопустимое имя!'

        elif not 1 <= int(room) <= 10:
            error = 'Недопустимая комната'

        self.render('templates/index.html', name=name, room=room, error=error)


class Room(tornado.web.RequestHandler):
    def get(self, room: str, name: str):
        if name == 'ADMIN' and int(room) == 11:
            self.render("templates/admin.html")

        else:
            self.render("templates/messenger.html")

    def post(self, room: int, name: str):
        type_submit = self.get_argument('type_submit')
        room = self.get_argument('number')

        if type_submit == "clear":
            with connect(**setting_dict) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"""
                    DELETE FROM message
                    WHERE message_room={room}"""
                )
                conn.commit()
            for user in RoomSocket.rooms[int(room) - 1]:
                user.on_message('get messages')

        elif type_submit == 'restart':
            for user in RoomSocket.rooms[int(room) - 1]:
                user.write_message("disconnect")

        self.render('templates/admin.html')


class RoomSocket(tornado.websocket.WebSocketHandler):
    rooms = [set() for _ in range(10)]

    def open(self, room: int, name: str):
        self.conn = connect(**setting_dict)
        self.name = name
        self.room = int(room)

        RoomSocket.rooms[self.room - 1].add(self)
        self.update_online()
        self.on_message('get messages')

    def on_close(self):
        self.conn.close()
        RoomSocket.rooms[self.room - 1].remove(self)
        self.update_online()

    def on_message(self, message: str):
        if message.startswith('message=') or message == 'get messages':
            with self.conn.cursor() as cursor:
                if message != 'get messages':
                    message = message[8:]
                    cursor.execute(
                        f"""
                        INSERT INTO message
                        (message_user, message_content, message_room)
                        VALUES ('{self.name}', '{message}', {self.room})"""
                    )

                cursor.execute(
                    f"""
                    SELECT message_user, message_content FROM message
                    WHERE message_room={self.room}
                    ORDER BY message_id"""
                )

                messages = cursor.fetchall()

            self.conn.commit()

            result = ''

            for message in messages:
                result += f'{message[0]}: {message[1]} <br>'

            for user in RoomSocket.rooms[self.room - 1]:
                user.write_message(result)

    def get_online(self):
        message = 'Online: '
        clients = 0

        for _ in RoomSocket.rooms[self.room - 1]:
            clients += 1

        message += str(clients)

        return message

    def update_online(self):
        online = self.get_online()
        for user in RoomSocket.rooms[self.room - 1]:
            user.write_message(online)


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/(\d+)/(\w+)/', Room),
        (r'/(\d+)/([\w ]+)/ws', RoomSocket)
    ])


if __name__ == "__main__":
    run_db(setting_dict)
    app = make_app()
    app.listen(8888)
    enable_pretty_logging()
    tornado.ioloop.IOLoop.current().start()
