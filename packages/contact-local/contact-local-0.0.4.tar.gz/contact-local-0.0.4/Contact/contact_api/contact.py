import mysql.connector
from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local
from circles_local_database_python.connection import Connection
from datetime import datetime
from logger_local.LoggerComponentEnum import LoggerComponentEnum



load_dotenv()


obj = {
    'component_id': 123,
    'componenet_name':'contact-local',
    'comopmnenet_categroy':LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email':'shavit.m@circ.zone'

    
}
logger_local.init(object=obj)



db = Connection("contact")
connection = db.connect()


class contact:

    def __init__(self):
        pass

    @staticmethod
    def insert(first_name,last_name,phone,
                    birthday,email,location,job_title,organization):
        try:
            object1 = {
                'first_name': first_name
            }
            logger_local.start(object=object1)
            connection.connect()
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
            cursor.close()
            connection.commit()
            connection.close()
        except mysql.connector.Error as err:
            logger_local.error(f"Error: {err}")
        finally:
            logger_local.info("contact added "+first_name)

    @staticmethod
    def update(person_id, name_prefix, first_name, additional_name, job_title, id):
        try:
            object1 = {
            'idToChange' :id
            }
            logger_local.start(object=object1)
            connection.connect()
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
            cursor.close()
            connection.commit()
            connection.close()
        except mysql.connector.Error as err:
            logger_local.exception(f"Error: {err}", err)
        finally:
            logger_local.info("contact updated"+str(id))
            cursor.close()

    @staticmethod
    def delete(contact_id):
        try:
            object1 = {
                'contact_id': contact_id,
            }
            logger_local.start(object=object1)
            connection.connect()
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
            cursor.close()
            connection.commit()
            connection.close()
        except mysql.connector.Error as err:
            logger_local.exception(f"Error: {err}", err)
        finally:
            logger_local.info("contact deleted"+str(id))
