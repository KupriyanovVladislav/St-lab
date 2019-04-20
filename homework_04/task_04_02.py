from sqlalchemy import create_engine, and_, or_, func, select, join
from sqlalchemy.orm import sessionmaker
from models import Shop, Department, Item, Base
from sqlalchemy.sql.expression import literal


class AlchemyManager:
    def __init__(self, username: str, password: str, db_name: str):
        self.conn_str = f'postgresql://{username}:{password}@localhost:5432/{db_name}'
        self.engine = create_engine(self.conn_str)
        self.session = sessionmaker(bind=self.engine)()
        self.Base = Base

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

    def insert_data(self):
        self.session.add_all([
            Shop(name="Auchan", address=None, staff_amount=250),
            Shop(name="IKEA", address="Street Žirnių g. 56, Vilnius, Lithuania.",
                 staff_amount=250)
        ])
        self.session.commit()

        self.session.add_all([
            Department(sphere="Furniture", staff_amount=250, shop_id=1),
            Department(sphere="Furniture", staff_amount=300, shop_id=2),
            Department(sphere="Dishes", staff_amount=200, shop_id=2)
        ])
        self.session.commit()

        self.session.add_all([
            Item(name="Table", description="Cheap wooden table", price=300, department_id=1),
            Item(name="Table", description=None, price=750, department_id=2),
            Item(name="Bed", description="Amazing wooden table", price=1200, department_id=2),
            Item(name="Cup", description=None, price=10, department_id=3),
            Item(name="Plate", description="Glass Plate", price=20, department_id=3)
        ])
        self.session.commit()

    def select_data(self, task: int):
        if task == 1:
            return [item.__repr__() for item in self.session.query(Item) if item.description]
        elif task == 2:
            return list({department.sphere for department in self.session.query(Department)
                         if department.staff_amount > 200})
        elif task == 3:
            return [shop.address for shop in filter(lambda x: x.address, self.session.query(Shop))
                    if shop.address.startswith(('i', 'I'))]
        elif task == 4:
            return [item.name for item in self.session.query(Item).filter(
                and_(
                    Item.department_id == Department.id,
                    Department.sphere == "Furniture"
                )
            )]
        elif task == 5:
            return [shop.name for shop in self.session.query(Shop).filter(
                and_(
                    Shop.id == Department.shop_id,
                    Item.department_id == Department.id, Item.description.isnot(None))
            )]
        elif task == 6:
            return [(item.name, department.sphere, shop.name) for item, department, shop
                    in self.session.query(Item, Department, Shop).filter(
                and_(
                    Item.department_id == Department.id,
                    Department.shop_id == Shop.id
                )
            )]
        elif task == 7:
            return self.session.query(Item).order_by(Item.name).offset(2).limit(2)
        elif task == 8:
            return [(item.name, department.sphere) for item, department
                    in self.session.query(Item, Department).join(Department)]
        elif task == 9:
            return [(item.name, department.sphere if department else None) for item, department
                    in self.session.query(Item, Department).outerjoin(Department)]
        elif task == 10:
            return [(item.name if item else None, department.sphere) for department, item
                    in self.session.query(Department, Item).outerjoin(Item)]
        elif task == 11:
            return [(item.name if item else None, department.sphere if department else None) for department, item
                    in self.session.query(Department, Item).join(Item, full=True)]
        elif task == 12:
            return [(item.name, department.sphere) for department, item
                    in self.session.query(Department, Item).join(Item, literal(True))]
        elif task == 13:
            return self.session.execute(
                select([
                    Shop.name,
                    func.count(Item.name),
                    func.sum(Item.price),
                    func.max(Item.price),
                    func.min(Item.price),
                    func.avg(Item.price)
                ]).select_from(join(Item, join(Department, Shop))).group_by(Shop.id).having(func.count(Item.id) > 1)
            ).fetchall()
        elif task == 14:
            return self.session.execute(
                select([Shop.name, func.array_agg(Item.name)]).select_from(
                    join(Item, join(Department, Shop))
                ).group_by(Shop.id)
            ).fetchall()

    def update_data(self):
        self.session.query(Item).filter(
            or_(Item.name.ilike('%e'), Item.name.ilike('b%'))
        ).update({Item.price: Item.price + 100}, synchronize_session='fetch')

        self.session.commit()

    def delete_data(self, task: int):
        if task == 1:
            self.session.query(Item).filter(
                and_(Item.price > 500, Item.description.is_(None))
            ).delete(synchronize_session='fetch')
        elif task == 2:
            self.session.query(Item).filter(
                and_(
                    Item.department_id == Department.id,
                    Department.shop_id == Shop.id,
                    Shop.address.is_(None)
                )
            ).delete(synchronize_session='fetch')
        elif task == 3:
            self.session.query(Item).filter(
                and_(
                    Item.department_id == Department.id,
                    or_(
                        Department.staff_amount < 225,
                        Department.staff_amount > 275
                    )
                )
            ).delete(synchronize_session='fetch')
        elif task == 4:
            self.session.execute("TRUNCATE TABLE Item, Department, Shop")

        self.session.commit()

    def drop_tables(self):
        self.session.execute("DROP TABLE Item, Department, Shop")
        self.session.commit()
        self.session.close()
