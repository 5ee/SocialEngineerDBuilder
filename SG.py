# -*- coding: utf-8 -*-
"""
"""
from __future__ import print_function

import sys
import sqlalchemy
from User import user_model
from Common import get_DB_engine,init_User_table,get_DB_session,preConstruct


def gen_parse_class(f_name):
    """
    """
    # Read the first line
    with open(f_name) as f:
        sep,columns = preConstruct(f.readline())

    if sep == 'SPACE':
        sep = ' '
    columns = [c.strip() for c in columns]

    # check column name
    if not check_col_name(columns): raise Exception('Invalid column name!')

    # inner define function
    def parse_line_to_dic(self,line):
        """
        The generated class __init__()
        """
        row_elements = line.split(sep)
        row_elements = [r.strip() for r in row_elements]
        kargs = {}
        for ele_i in range(len(columns)):
            try:
                if columns[ele_i] == 'ignore':
                    pass
                else:
                    kargs[columns[ele_i]] = row_elements[ele_i]
            except Exception,e:
                sys.stdout.write(e)
        # do the init
        super(spec_user_model,self).__init__(**kargs)

    # inner define class
    spec_user_model = type('spec_user_model',(user_model,),{'__init__':parse_line_to_dic})

    # return class like this:
    """
     Class spec_user_model(user_model):
         def __init__(self,):
             row_elements = line.split(sep)
             kargs = {}

             for ele_i in range(len(row_elements)):
                 kargs[ele_i] = row_elements[ele_i]
                 # do the init
                 super().__init__(**kargs)
    """
    # usage():
    # user = spec_user_model(username='user',password='pass',...)
    # session.commit(user)
    return spec_user_model


# do one job
def save_to_db(fname,user_class,single_file=False,lines_num=1000):
    """
    """
    sess = get_DB_session()
    #sess.autocommit = True
    with open(fname) as f:
        if single_file==True:
            f.readline()
        while True:
            line_n = 0
            for line in f:
                try:
                    user = user_class(line)
                    sess.add(user)
                    line_n += 1

                    if line_n % lines_num == 0:
                        sess.commit()
                        print("\r Processed {0} lines\r".format(line_n),file=sys.stdout,end=" ")
                        sys.stdout.flush()
                except Exception,e:
                    print("exception found :\n  line:{0}\n  content:{1}   exception:{2}\n".format(line_n,line,e))
            sess.commit()
            print("\n {0} datalines Finished\r".format(line_n),file=sys.stdout)
            break
    return True

# do all dirty jobs
def save_all_to_db():
    init_User_table()
    if len(sys.argv) == 2:
        user_class = gen_parse_class(sys.argv[1])
        save_to_db(sys.argv[1],user_class,single_file=True)
    elif len(sys.argv) == 3:
        user_class = gen_parse_class(sys.argv[2])
        save_to_db(sys.argv[1],user_class,single_file=False)
    elif len(sys.argv) == 4:
        user_class = gen_parse_class(sys.argv[2])
        save_to_db(sys.argv[1],user_class,single_file=True)
    else:
        raise Exception('Error argument number!')

# build column line
def build_col_line(columns):
    line = ""
    for c in columns:
        # init
        if line == '':
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
        sep,columns = preConstuct(f.readline())

    if sep == 'SPACE':
        sep = ' '
    columns = [c.strip() for c in columns]
    if not check_col_name(columns): return False

    col_line = build_col_line(columns)
    table_name = model.__tablename__

    sql_query = """LOAD DATA LOCAL INFILE '{0}'
    INTO TABLE {1}
    FIELDS TERMINATED BY '{2}'
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


def do_load_data_from_file():
    init_User_table()
    if len(sys.argv) == 2:
        do_load_data_from_file(sys.argv[1],sys.argv[1],single_file=True)
    elif len(sys.argv) == 3:
        do_load_data_from_file(sys.argv[1],sys.argv[2],single_file=False)
    elif len(sys.argv) == 4:
        do_load_data_from_file(sys.argv[1],sys.argv[2],single_file=True)
    else:
        raise Exception('Error argument number!')

if __name__ == '__main__':
    save_all_to_db()
