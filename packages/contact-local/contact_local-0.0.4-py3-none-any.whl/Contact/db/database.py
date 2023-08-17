import mysql
import os


def connect_to_database():
    mydb = mysql.connector.connect(
        host=os.getenv("RDS_HOSTNAME"),
        user=os.getenv("RDS_USERNAME"),
        password=os.getenv("RDS_PASSWORD"),
        database=os.getenv("RDS_DB_NAME"),
    )
    return mydb
