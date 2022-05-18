import xml.etree.ElementTree as ET
import psycopg2
from psycopg2 import OperationalError
from psycopg2._psycopg import Error


def get_config(config_file="config.xml"):
    tree = ET.parse(config_file)
    root = tree.getroot()
    result = {}
    for inside_elements in root:
        for element in inside_elements:
            result[element.tag] = element.text

    return result


def create_connection():
    config = get_config()
    connection = None
    try:
        connection = psycopg2.connect(database=config['db_name'],
                                      user=config['db_user'],
                                      password=config['db_password'],
                                      host=config['db_host'],
                                      port=config['db_port'])

        print("Conncetion to PostgreSQL DB successful")
        return connection
    except OperationalError as e:
        print(f"The error {e} occurred")


def select_tags():
    config = get_config()
    connect = create_connection()
    sql_select = "SELECT " + config['tb_column_tag'] + ",inout FROM " + config['tb_name'] + " WHERE " + config[
        'tb_column_tag'] + " IS NOT NULL"
    cursor = connect.cursor()
    try:
        cursor.execute(sql_select)
        return [i[0] for i in cursor.fetchall()]
    except Error as e:
        print(f"The error {e} occurred")
