from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection
import mysql.connector
from shapely.geometry import Point
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

def insert_person(person_id: int, number: int, gender_id: int, last_coordinate: Point , location_id: int) -> None:
    logger_local.start()
    try:
        conn = connection.Connection("person").connect()
        db_cursor = connection.Connection.cursor(conn)
        query = ("INSERT INTO person.person_table (person_id, number, gender_id, last_coordinate, location_id,start_timestamp) VALUES ({}, {}, {}, {}, {}, CURRENT_TIMESTAMP)".
                 format(person_id, number, gender_id, last_coordinate, location_id))

        db_cursor.execute(query)
        conn.commit()
        print("Person inserted successfully.")
        insert_person_ml(person_id,person_id)
    except mysql.connector.Error as err:
        print("Error:", err)
    logger_local.end()


def insert_person_ml(id: int,person_id: int) -> None:
    logger_local.start()
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)

    query = ("INSERT INTO person.person_ml_table (id, person_id) VALUES ({},{})".format(id,person_id))

    db_cursor.execute(query)
    conn.commit()
    logger_local.end()
