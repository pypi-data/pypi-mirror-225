import sys
import os
import datetime
from dotenv import load_dotenv
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory,'..'))
from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection
from person_local_python_package.src.delete_person_table import delete_person
from person_local_python_package.src.update_person_table import (update_person_birthday_date,
                                     update_person_first_name,
                                     update_person_nickname,
                                     update_person_last_name,
)

import pytest



load_dotenv()  
logger_local.init(object = {"component_id":169 })


@pytest.mark.test
def test_update_person_birthday_date():
    update_person_birthday_date(2,"2008-08-31")
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    query = ("SELECT birthday_date FROM person.person_table WHERE id = {}".format(2))
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_cursor.close()
    conn.close()
    assert result[0] == datetime.date(2008, 8, 31)

@pytest.mark.test
def test_update_person_first_name():
    update_person_first_name(22,"Tal")
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    query = ("SELECT first_name FROM person.person_table WHERE id = {}".format(22))
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_cursor.close()
    conn.close()
    assert result[0] == "Tal"

@pytest.mark.test
def test_update_person_first_name():
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    query = ("SELECT first_name FROM person.person_table WHERE id = {}".format(22))
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_cursor.close()
    conn.close()
    assert result[0] == "Evgeni"

@pytest.mark.test
def test_update_person_nickname():
    update_person_nickname(2,"Batata")
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    query = ("SELECT nickname FROM person.person_table WHERE id = {}".format(2))
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_cursor.close()
    conn.close()
    assert result[0] == "Batata"
    

@pytest.mark.test
def test_update_person_last_name():
    update_person_last_name(22,"Blala")
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)
    query = ("SELECT last_name FROM person.person_table WHERE id = {}".format(22))
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    db_cursor.close()
    conn.close()
    assert result[0] == "Blala"
