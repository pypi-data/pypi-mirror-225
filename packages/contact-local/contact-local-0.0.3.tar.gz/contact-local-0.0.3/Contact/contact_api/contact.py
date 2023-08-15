import mysql.connector
from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local
from circles_local_database_python.connection import DatabaseFunctions
from datetime import datetime


load_dotenv()
obj = {
    'component_id': 123
}
logger_local.init(object=obj)



db = DatabaseFunctions("contact_table")
connection = db.connect()




def insert(first_name,last_name,phone,
                   birthday,email,location,job_title,organization):
    try:
        object1 = {
            'first_name': first_name
        }
        logger_local.start(object=object1)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO contact.contact_table (
            first_name,
            last_name,
            phone1,
            birthday,
            email1,
            address1_street,
            job_title,
            organization
        )
        VALUES (
             %s, %s, %s, %s, %s, %s, %s,%s
        )
        """

        data_values = (
            first_name,
            last_name,
            phone,
            birthday,
            email,
            location,
            job_title,
            organization
        )

        cursor.execute(insert_query, data_values)
        connection.commit()
    except mysql.connector.Error as err:
        logger_local.error(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()


def update(person_id, name_prefix, first_name, additional_name, job_title, id):
    try:
        object1 = {
            'person_id': person_id,
            'name_prefix': name_prefix,
            'first_name': first_name,
            'additional_name': additional_name,
            'job_title': job_title,
            

        }
        logger_local.start(object=object1)
        cursor = connection.cursor()
        update_query = """
        UPDATE contact.contact_table
        SET
            person_id = %s,
            name_prefix = %s,
            first_name = %s,
            additional_name = %s,
            job_title=%s
        WHERE
            id = %s
        """

        data_values = (
            person_id,
            name_prefix,
            first_name,
            additional_name,
            job_title,
            id
        )

        cursor.execute(update_query, data_values)
        connection.commit()
        logger_local.end("contact updated"+str(id))
    except mysql.connector.Error as err:
        logger_local.exception(f"Error: {err}", err)
        connection.rollback()
    finally:
        cursor.close()


def fire(contact_id):
    try:
        object1 = {
            'contact_id': contact_id,
        }
        logger_local.start(object=object1)
        cursor = connection.cursor()
        update_query = """
        UPDATE contact.contact_table
        SET
            last_sync_timestamp = %s
        WHERE
            id = %s
        """

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data_values = (
            current_time,
            contact_id
        )

        cursor.execute(update_query, data_values)
        connection.commit()
        logger_local.end("contact fired"+str(id))
    except mysql.connector.Error as err:
        logger_local.exception(f"Error: {err}", err)
        connection.rollback()
    finally:
        cursor.close()


def lastId():
    try:
        cursor = connection.cursor()
        query = "SELECT LAST_INSERT_ID();"
        cursor.execute(query)
        last_inserted_id = cursor.fetchone()[0]
        return last_inserted_id
    except mysql.connector.Error as err:
        logger_local.error(f"Error: {err}")
    finally:
        cursor.close()