import psycopg2


class SQLManager:
    def __init__(self, setting_dict):
        self.conn = psycopg2.connect(**setting_dict)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute(
            "CREATE TABLE Shops ("
            "id INT PRIMARY KEY,"
            "name varchar NOT NULL,"
            "address varchar,"
            "staff_amount INT NOT NULL"
            ");"
        )

        self.cur.execute(
            "CREATE TABLE Departments ("
            "id INT PRIMARY KEY,"
            "sphere varchar NOT NULL,"
            "staff_amount INT NOT NULL,"
            "shop_id INT REFERENCES Shops(id)"
            ");"
        )

        self.cur.execute(
            "CREATE TABLE Items ("
            "id INT PRIMARY KEY,"
            "name varchar NOT NULL,"
            "description varchar,"
            "price INT NOT NULL,"
            "department_id INT REFERENCES Departments(id)"
            ");"
        )

        self.conn.commit()

    def insert_data(self):
        self.cur.execute(
            "INSERT INTO Shops VALUES"
            "(1, 'Auchan', null, 250),"
            "(2, 'IKEA', 'Street Žirnių g. 56, Vilnius, Lithuania.', 500);"
        )

        self.cur.execute(
            "INSERT INTO Departments VALUES "
            "(1, 'Furniture', 250, 1),"
            "(2, 'Furniture', 300, 2),"
            "(3, 'Dishes', 200, 2);"
        )

        self.cur.execute(
            "INSERT INTO Items VALUES"
            "(1, 'Table', 'Cheap wooden table', 300, 1),"
            "(2, 'Table', null, 750, 2),"
            "(3, 'Bed', 'Amazing wooden bed', 1200, 2),"
            "(4, 'Cup', null, 10, 3),"
            "(5, 'Plate', 'Glass plate', 20, 3);"
        )

        self.conn.commit()

    def select_data(self, task: int):
        if task == 1:
            self.cur.execute(
                "SELECT * FROM Items "
                "WHERE description IS NOT NULL"
            )
        elif task == 2:
            self.cur.execute(
                "SELECT DISTINCT sphere FROM Departments "
                "WHERE staff_amount > 200"
            )
        elif task == 3:
            self.cur.execute(
                "SELECT address FROM Shops "
                "WHERE address SIMILAR TO '[iI]%'"
            )
        elif task == 4:
            self.cur.execute(
                "SELECT Items.name "
                "FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id "
                "WHERE Departments.sphere = 'Furniture'"
            )
        elif task == 5:
            self.cur.execute(
                "SELECT DISTINCT Shops.name FROM Shops, "
                "(SELECT * FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id "
                "WHERE Items.description IS NOT NULL) tmp "
                "WHERE tmp.shop_id = Shops.id"
            )
        elif task == 6:
            self.cur.execute(
                "SELECT tmp.name, tmp.description, tmp.price, "
                "tmp.sphere AS \"department_sphere\", "
                "tmp.staff_amount AS \"department_staff_amount\", "
                "shops.name AS \"shop_name\", shops.address AS \"shop_address\", "
                "shops.staff_amount AS \"shop_staff_amount\" "
                "FROM (SELECT * FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id) tmp "
                "INNER JOIN shops ON tmp.shop_id = shops.id"
            )
        elif task == 7:
            self.cur.execute(
                "SELECT name FROM items"
                "ORDER BY name"
                "OFFSET 2 LIMIT 2"
            )
        elif task == 8:
            self.cur.execute(
                "SELECT items.name, departments.sphere "
                "FROM Items INNER JOIN departments "
                "ON Items.department_id = departments.id"
            )
        elif task == 9:
            self.cur.execute(
                "SELECT items.name, departments.sphere "
                "FROM Items LEFT JOIN departments "
                "ON Items.department_id = departments.id"
            )
        elif task == 10:
            self.cur.execute(
                "SELECT items.name, departments.sphere "
                "FROM Items RIGHT JOIN departments "
                "ON Items.department_id = departments.id"
            )
        elif task == 11:
            self.cur.execute(
                "SELECT items.name, departments.sphere "
                "FROM Items FULL JOIN departments "
                "ON Items.department_id = departments.id"
            )
        elif task == 12:
            self.cur.execute(
                "SELECT items.name, departments.sphere "
                "FROM Items CROSS JOIN departments"
            )
        elif task == 13:
            self.cur.execute(
                "SELECT shops.name, count(tmp.name), sum(tmp.price), "
                "max(tmp.price), min(tmp.price), avg(tmp.price) "
                "FROM (SELECT * FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id) tmp "
                "INNER JOIN shops ON tmp.shop_id = shops.id "
                "GROUP BY shops.id "
                "HAVING count(tmp.name) > 1"
            )
        elif task == 14:
            self.cur.execute(
                "SELECT shops.name, array_agg(tmp.name) "
                "FROM (SELECT * FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id) tmp "
                "INNER JOIN shops ON tmp.shop_id = shops.id "
                "GROUP BY shops.id"
            )

        results = self.cur.fetchall()
        return results

    def update_data(self):
        self.cur.execute(
            "UPDATE items "
            "SET price = price + 100 "
            "WHERE name SIMILAR TO '(%[eE]|[bB]%)'"
        )

        self.conn.commit()

    def delete_data(self, task: int):
        if task == 1:
            self.cur.execute(
                "DELETE FROM Items "
                "WHERE price > 500 AND description IS NULL"
            )

        elif task == 2:
            self.cur.execute(
                "DELETE FROM items "
                "WHERE id IN (SELECT tmp.id FROM "
                "(SELECT items.id, departments.shop_id "
                "FROM Items INNER JOIN Departments "
                "ON Items.department_id = Departments.id) tmp "
                "INNER JOIN shops ON tmp.shop_id = shops.id "
                "WHERE shops.address IS NULL)"
            )

        elif task == 3:
            self.cur.execute(
                "DELETE FROM items "
                "WHERE id IN (SELECT items.id FROM "
                "items INNER JOIN departments "
                "ON items.department_id = departments.id "
                "WHERE departments.staff_amount < 225 "
                "OR departments.staff_amount > 275)"
            )

        elif task == 4:
            self.cur.execute(
                "TRUNCATE TABLE items, departments, shops;"
            )

        self.conn.commit()

    def drop_tables(self):
        self.cur.execute(
            "DROP TABLE departments, items, shops;"
        )

        self.conn.commit()
        self.cur.close()
        self.conn.close()
