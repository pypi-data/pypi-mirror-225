import mysql.connector
from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local
from circles_local_database_python.connection import Connection


db = Connection("contact")
connection = db.connect()


def create_contact_table():

    mycursor = connection.cursor()
    mycursor.execute("USE contact")

    # Create the outgoing_message table
    mycursor.execute("""
                            CREATE TABLE IF NOT EXISTS contact_table (
                            id BIGINT UNSIGNED AUTO_INCREMENT,
                            owner_profile_id BIGINT UNSIGNED NULL,
                            account_name VARCHAR(255) NULL,
                            person_id BIGINT UNSIGNED NULL,
                            uploaded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                            last_sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                            name_prefix VARCHAR(255) NULL,
                            first_name VARCHAR(255) NULL,
                            additional_name VARCHAR(255) NULL,
                            last_name VARCHAR(255) NULL,
                            full_name VARCHAR(255) NULL,
                            name_suffix VARCHAR(255) NULL,
                            nickname VARCHAR(255) NULL,
                            display_as VARCHAR(255) NULL,
                            title VARCHAR(255) NULL,
                            organization VARCHAR(255) NULL,
                            organization_profile_id BIGINT UNSIGNED NULL,
                            job_title VARCHAR(255) NULL,
                            department VARCHAR(255) NULL,
                            notes TEXT NULL,
                            email1 VARCHAR(255) NULL,
                            email2 VARCHAR(255) NULL,
                            email3 VARCHAR(255) NULL,
                            phone1 VARCHAR(255) NULL,
                            phone2 VARCHAR(255) NULL,
                            phone3 VARCHAR(255) NULL,
                            address1_street VARCHAR(255) NULL,
                            address1_city VARCHAR(255) NULL,
                            address1_state VARCHAR(255) NULL,
                            address1_postal_code VARCHAR(255) NULL,
                            address1_country VARCHAR(255) NULL,
                            address2_street VARCHAR(255) NULL,
                            address2_city VARCHAR(255) NULL,
                            address2_state VARCHAR(255) NULL,
                            address2_postal_code VARCHAR(255) NULL,
                            address2_country VARCHAR(255) NULL,
                            birthday DATE NULL,
                            day INT UNSIGNED NULL,
                            month INT UNSIGNED NULL,
                            year INT UNSIGNED NULL,
                            cira bool NULL,
                            anniversary DATE NULL,
                            website1 VARCHAR(255) NULL,
                            website2 VARCHAR(255) NULL,
                            website3 VARCHAR(255) NULL,
                            photo_url VARCHAR(255) NULL,
                            photo_file_name VARCHAR(255) NULL,
                            source VARCHAR(255) NULL,
                            PRIMARY KEY(id),
                            FOREIGN KEY(owner_profile_id) REFERENCES profile.profile(id)
                            )
                        """)
    # commit change and Close the database connection
    connection.commit()
    mycursor.close()
    connection.close()


def get_contact_by_id(contact_id):
    try:
        connection.connect()
        cursor = connection.cursor()
        select_query = """
        SELECT * FROM contact.contact_table
        WHERE
            id = %s
        """

        cursor.execute(select_query, (contact_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        logger_local.error(f"Error: {err}")
    


def get_contact_by_first_name(first_name):
    try:
        connection.connect()
        cursor = connection.cursor()
        select_query = """
        SELECT * FROM contact.contact_table
        WHERE
            first_name = %s
        """

        cursor.execute(select_query, (first_name,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except mysql.connector.Error as err:
        logger_local.error(f"Error: {err}")
   
