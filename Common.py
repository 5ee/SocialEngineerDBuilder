# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function

import sys
import sqlalchemy
from User import user_model


def get_DB_engine():
    from User import engine
    return engine


def init_User_table(model=user_model):
    engine = get_DB_engine()
    if engine.has_table(model.__tablename__) == False:
        model.metadata.create_all(engine)
        sys.stdout.write(" table {0} init success!\n".format(model.__tablename__))
        return True


def get_DB_session(engine=get_DB_engine()):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def preConstruct(form_line):
    """
    parse the line with '|',the first parameter is seperator
    """
    sep,form = form_line.split(' ')
    columns = [col_name for col_name in form.split('|') if col_name != '']
    return sep,columns


def check_col_name(columns):
    table_columns = ['username','username_zh','password','email',
                    'identify_number','cell_phone','ip_addr','living_place','ignore']
    for c in columns:
        if c not in table_columns:
            raise Exception('invalid column name {0}'.format(c))
            return False
    return True
