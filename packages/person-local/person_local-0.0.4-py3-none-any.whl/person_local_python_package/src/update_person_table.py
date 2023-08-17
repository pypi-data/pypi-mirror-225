from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection
import datetime
from logger_local.LoggerComponentEnum import LoggerComponentEnum

EXTERNAL_USER_COMPONENT_ID = 169
EXTERNAL_USER_COMPONENT_NAME = 'person-local'
object_init = {
    'component_id': EXTERNAL_USER_COMPONENT_ID,
    'component_name':EXTERNAL_USER_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email":"jenya.b@circ.zone"
}

logger_local.init(object=object_init)

def conn_db(db: str,query: str) -> None:
    logger_local.start()
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    db_cursor.execute(query)
    conn.commit()
    logger_local.end()

def update_person_day(id: int,day: int) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET day = {} WHERE person_id = {}".format(day,id))
    conn_db("person",query)
    logger_local.end()

def update_person_month(id: int,month: int) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET month = {} WHERE person_id = {}".format(month,id))
    conn_db("person",query)
    logger_local.end()

def update_person_year(id: int,year: int) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET year = {} WHERE person_id = {}".format(year,id))
    conn_db("person",query)
    logger_local.end()

def update_person_birthday_date(id: int,birthday_date: datetime.date) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET birthday_date = '{}' WHERE person_id = {}".format(birthday_date,id))
    conn_db("person",query)
    logger_local.end()

def update_person_first_name(id: int,first_name: str) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
    conn_db("person",query)
    update_person_ml_first_name(id,first_name)
    logger_local.end()

def update_person_ml_first_name(id: int,first_name: str) -> None:
    logger_local.start()
    query = ("UPDATE person.person_ml_table SET first_name = '{}' WHERE person_id = {}".format(first_name,id))
    conn_db("person",query)
    logger_local.end() 

def update_person_nickname(id: int,nickname: str) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET nickname = '{}' WHERE person_id = {}".format(nickname,id))
    conn_db("person",query)
    logger_local.end()

def update_person_last_name(id: int,last_name: str) -> None:
    logger_local.start()
    query = ("UPDATE person.person_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
    conn_db("person",query)
    update_person_ml_last_name(id,last_name)
    logger_local.end()

def update_person_ml_last_name(id: int,last_name: str) -> None:
    logger_local.start()
    query = ("UPDATE person.person_ml_table SET last_name = '{}' WHERE person_id = {}".format(last_name,id))
    conn_db("person",query)
    logger_local.end()