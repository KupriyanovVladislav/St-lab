from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, \
    Text, select, join, func, or_, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

username, password, db_name = "postgres", "Vlad1234", "markets"
conn_str = f'postgresql://{username}:{password}@localhost:5432/{db_name}'
engine = create_engine(conn_str)

Session = sessionmaker(bind=engine)
session = Session()

# ручное описание моделей
Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    def __repr__(self):
        return f'Group {self.number}'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    faculty = Column(String)


class Student(Base):
    __tablename__ = 'student'

    def __repr__(self):
        return f'Student {self.name} {self.surname}'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    description = Column(Text)
    group_id = Column(Integer, ForeignKey('groups.id'))
    groups = relationship(Group, backref='students')


result = session.query(Student, Group).join(Group)
print(f'Студенты с группами: {list(result)}')

group = session.query(Group).first()
print(f'Студенты группы {group.number}: {list(group.students)}')

# автоматическая генерация моделей
Base = automap_base()
Base.prepare(engine, reflect=True)
Student = Base.classes.student
Group = Base.classes.groups

Student.__repr__ = lambda self: f'Student {self.name} {self.surname}'
Group.__repr__ = lambda self: f'Group {self.number}'

result = session.query(Student, Group).join(Group)
print(f'Студенты с группами: {list(result)}')

result = select(
    [Student]
).select_from(
    join(Student, Group)
).where(
    Student.age > 22
)
print(session.execute(result).fetchall())

result = select(
    [Group.number, func.array_agg(Student.name)]
).select_from(
    join(Student, Group)
).group_by(
    Group.id
)
print(session.execute(result).fetchall())

# insert
new_group = Group(number=301, faculty='FIR')
session.add(new_group)
session.commit()
new_student_1 = Student(
    name='Jack', surname='Sparrow', age=28, group_id=new_group.id
)
new_student_2 = Student(
    name='Harry', surname='Potter', age=19, group_id=new_group.id
)
session.add_all([new_student_1, new_student_2])
session.commit()

# select
print(
    session.query(Student).filter(Student.name.isnot(None)).all()
)
print(
    session.query(Student.name).filter(Student.age > 22).distinct().all()
)
print(
    session.query(Student.name, Student.age).filter(
        Student.name.startswith('H')
    ).all()
)
print(
    session.query(Student, Group).join(Group).filter(
        Group.number > 200
    ).all()
)

print(
    session.query(Student).limit(2).offset(2).all()
)

# update
session.query(Student).filter(
    or_(
        Student.name.startswith('H'), Student.name.endswith('k')
    )
).update(
    {Student.age: Student.age + 1}, synchronize_session='fetch'
)
session.commit()

student = session.query(Student).order_by(-Student.id).first()
student.age += 1
session.commit()

# delete
session.query(Student).filter(
    and_(
        Student.age > 20, Student.description.is_(None)
    )
).delete()
session.commit()

session.query(Student).delete()

student = session.query(Student).order_by(-Student.id).first()
session.delete(student)
session.commit()
