#!/usr/bin/env python2
from init_database import Base, User, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_database import Base, User, Item

engine = create_engine('sqlite:///catelog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def seeding():
        # add admin:
    admin = User(username='Admin', title='Admin')
    admin.hash_password('123456')
    session.add(admin)
    session.commit()

    # add item1:
    # name = Column(String(250))
    # address = Column(String(250))
    # category = Column(String(250))
    # description = Column(String(1250))
    item1 = Item(name='newyear', category='Chinese', address='China,TaiWan',
                 description='This is a tradition when new year comes in China')
    session.add(item1)
    session.commit()
    item2 = Item(name='Christmas', category='America', address='America, Eu',
                 description='This is a tradition in America')
    session.add(item2)
    item3 = Item(name='Adult\'s Day', category='Japan', address='Japan',
                 description='This is a tradition in Japan')
    session.add(item3)
    session.commit()


if __name__ == '__main__':
    seeding()
