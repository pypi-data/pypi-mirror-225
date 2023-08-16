from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection
import mysql.connector

logger_local.init(object = {"component_id":169 })

def insert_person(person_id, number, gender_id, last_coordinate, location_id):
    try:
        conn = connection.Connection("person").connect()
        db_cursor = connection.Connection.cursor(conn)
        query = ("INSERT INTO person.person_table (id, number, gender_id, last_coordinate, location_id,start_timestamp) VALUES ({}, {}, {}, {}, {}, CURRENT_TIMESTAMP)".
                 format(person_id, number, gender_id, last_coordinate, location_id))

        db_cursor.execute(query)
        conn.commit()
        print("Person inserted successfully.")
        insert_person_ml(person_id,person_id)
    except mysql.connector.Error as err:
        print("Error:", err)


def insert_person_ml(id,person_id):
    
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)

    query = ("INSERT INTO person.person_ml_table (id, person_id) VALUES ({},{})".format(id,person_id))

    db_cursor.execute(query)
    conn.commit()
