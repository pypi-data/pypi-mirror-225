from logger_local.LoggerLocal import logger_local
from circles_local_database_python import connection

logger_local.init(object = {"component_id":169 })

def delete_person(id):
    conn = connection.Connection("person").connect()
    db_cursor = connection.Connection.cursor(conn)

    query = ("UPDATE person.person_table SET end_timestamp = CURRENT_TIMESTAMP WHERE id = {}".format(id))
    db_cursor.execute(query)
    conn.commit()
