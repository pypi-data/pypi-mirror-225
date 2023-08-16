from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection

logger_local.init(object = {"component_id":169 })

def conn_db(db,query):
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    db_cursor.execute(query)
    conn.commit()

def update_person_day(id,day):
    query = ("UPDATE person.person_table SET day = {} WHERE id = {}".format(day,id))
    conn_db("person",query)

def update_person_month(id,month):
    query = ("UPDATE person.person_table SET month = {} WHERE id = {}".format(month,id))
    conn_db("person",query)

def update_person_year(id,year):
    query = ("UPDATE person.person_table SET year = {} WHERE id = {}".format(year,id))
    conn_db("person",query)

def update_person_birthday_date(id,birthday_date):
    query = ("UPDATE person.person_table SET birthday_date = '{}' WHERE id = {}".format(birthday_date,id))
    conn_db("person",query)

def update_person_first_name(id,first_name):
    query = ("UPDATE person.person_table SET first_name = '{}' WHERE id = {}".format(first_name,id))
    conn_db("person",query)
    update_person_ml_first_name(id,first_name)

def update_person_ml_first_name(id,first_name): 
    query = ("UPDATE person.person_ml_table SET first_name = '{}' WHERE id = {}".format(first_name,id))
    conn_db("person",query)

def update_person_nickname(id,nickname):
    query = ("UPDATE person.person_table SET nickname = '{}' WHERE id = {}".format(nickname,id))
    conn_db("person",query)

def update_person_last_name(id,last_name):
    query = ("UPDATE person.person_table SET last_name = '{}' WHERE id = {}".format(last_name,id))
    conn_db("person",query)
    update_person_ml_last_name(id,last_name)

def update_person_ml_last_name(id,last_name):
    query = ("UPDATE person.person_ml_table SET last_name = '{}' WHERE id = {}".format(last_name,id))
    conn_db("person",query)

