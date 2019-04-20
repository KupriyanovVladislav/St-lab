from sqlalchemy import Column, Integer, \
    String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    staff_amount = Column(Integer)

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.address}, {self.staff_amount}'


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sphere = Column(String)
    staff_amount = Column(Integer)
    shop_id = Column(Integer, ForeignKey("shop.id"))

    def __repr__(self):
        return f'{self.id}, {self.sphere}, {self.staff_amount}, {self.shop_id}'


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Integer)
    department_id = Column(Integer, ForeignKey("department.id"))

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.description},' \
            f' {self.price}, {self.department_id}'
