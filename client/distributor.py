from datetime import datetime
from time import time
import xml.etree.ElementTree as ET
import psycopg2, log
import pytz
from psycopg2 import *
from psycopg2._psycopg import Error

logger = log.get_logger(__name__)


def get_config(config_file="config.xml"):
    tree = ET.parse(config_file)
    root = tree.getroot()
    external_result = {}
    for external_elements in root:
        inside_result = {}
        external_result[external_elements.tag] = inside_result
        for element in external_elements:
            inside_result[element.tag] = element.text
    return external_result


def create_connection():
    config = get_config()
    connection = None
    try:
        connection = psycopg2.connect(database=config["database"]['db_name'],
                                      user=config["database"]['db_user'],
                                      password=config["database"]['db_password'],
                                      host=config["database"]['db_host'],
                                      port=config["database"]['db_port'])
        logger.info("Подключение к базе данных прошло успешно")
        return connection
    except OperationalError as e:
        logger.warning(f"The error {e} occurred")


def select_tags():
    config = get_config()
    connect = create_connection()
    sql_select = f"SELECT {config['database']['tb_column_tag']}, hfrpok FROM {config['database']['tb_name']} WHERE hfrpok IS NOT NULL "
    cursor = connect.cursor()
    try:
        cursor.execute(sql_select)
        return [i for i in cursor.fetchall()]
    except Error as e:
        logger.warning(f"The error {e} occurred")
    finally:
        cursor.close()
        connect.close()


def select_hfrpok():
    config = get_config()
    connect = create_connection()
    sql_hfrpok = f"SELECT hfrpok FROM {config['database']['tb_name']} "
    cursor = connect.cursor()
    dict_hfrpok = [elem for elem in cursor.fetchall()]


def insert_tags_values(dict_value, to_which_table):
    config = get_config()
    connect = create_connection()

    # tz = pytz.timezone(config['time_zone'])

    for key, value in dict_value.items():
        timestamp = datetime.now()
        # app_info.\"5min_params\" config['rate_5_min']['cl_table']
        # sql_insert = f"INSERT INTO {to_which_table} ({config['cl_value_volumn']} , {config['cl_column_tag']}) VALUES (\'{value}\', \'{key}\')"
        sql_insert = f"INSERT INTO {to_which_table} (val ,timestamp ,hfrpok_id) VALUES (\'{value}\', \'{timestamp}\', \'{key}\')"
        cursor = connect.cursor()
        try:
            cursor.execute(sql_insert)
            connect.commit()
        except Error as e:
            logger.warning(f"The error {e} occurred")


def select_data_alpha():
    config = get_config()
    connection = create_connection()
    sql_tag_name = f"SELECT {config['database']['alpha_column_tag']}, {config['database']['alpha_column_value']} FROM {config['database']['data_to_alpha']} is not null"
    cursor = connection.cursor()
    try:
        cursor.execute(sql_tag_name)
        return [item for item in cursor.fetchall()]
    except Error as e:
        logger.warning(f"The error {e} occurred")
    finally:
        cursor.close()
        connection.close()
