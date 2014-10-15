# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function

import sys
import sqlalchemy
from User import user_model
from Common import get_DB_engine,init_User_table,get_DB_session,preConstruct,check_col_name


# build column line
def build_col_line(columns):
    line = ""
    for c in columns:
        # init
        if line == '':
            if c == 'ignore':
                line = '{0}'.format('@dummy')
            else:
                line = '{0}'.format(c)
            continue
        # ignore case
        if c == 'ignore':
            line = "{0},@dummy".format(line)
        # append col
        else:
            line =  "{0},{1}".format(line,c)
    return line


# build sql string
def build_sql_by_tmpl(source_file,template,single_file=False,model=user_model):
    """
    """
    if single_file == True:
        template = source_file
        ignore_lines = 'IGNORE 1 LINES'
    else:
        ignore_lines = ''

    with open(template) as f:
        sep,columns = preConstruct(f.readline())

    if sep == 'SPACE':
        sep = '\s'
    columns = [c.strip() for c in columns]
    if not check_col_name(columns): return False

    col_line = build_col_line(columns)
    table_name = model.__tablename__

    sql_query = """LOAD DATA LOCAL INFILE '{0}'
    INTO TABLE {1}
    FIELDS TERMINATED BY '{2}'
    ENCLOSED BY '\\''
    LINES TERMINATED BY '\\r\\n'
    {3}
    ({4});
    """.format(
        source_file,
        table_name,
        sep,
        ignore_lines,
        col_line
    )
    return sql_query


def do_exc_sql_loadfile(sql):
    sess = get_DB_engine()
    print(sql)
    #sess.execute(sql)

def do_load_data_from_file():
    import os
    pwd = os.getcwd()
    source_file = pwd+'/'+sys.argv[1]
    templ = pwd+'/'+sys.argv[2]

    init_User_table()
    if len(sys.argv) == 2:
        sql = build_sql_by_tmpl(source_file,templ,single_file=True)
        do_exc_sql_loadfile(sql)
    elif len(sys.argv) == 3:
        sql = build_sql_by_tmpl(source_file,templ,single_file=False)
        do_exc_sql_loadfile(sql)
    elif len(sys.argv) == 4:
        sql = build_sql_by_tmpl(source_file,templ,single_file=True)
        do_exc_sql_loadfile(sql)
    else:
        raise Exception('Error argument number!')


if __name__ == '__main__':
    do_load_data_from_file()
