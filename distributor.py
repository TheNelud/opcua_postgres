import xml.etree.ElementTree as ET
import psycopg2, log
from psycopg2 import OperationalError
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
    sql_select = f"SELECT {config['database']['tb_column_tag']} FROM {config['database']['tb_name']} WHERE {config['database']['tb_column_tag']} IS NOT NULL "
    cursor = connect.cursor()
    try:
        cursor.execute(sql_select)
        return [i[0] for i in cursor.fetchall()]
    except Error as e:
        logger.warning(f"The error {e} occurred")


def insert_tags_values(dict_value, to_which_table):
    config = get_config()
    connect = psycopg2.connect(database="journal_kovikta",
                               user="postgres",
                               password="postgres",
                               host="127.0.0.1",
                               port=5432)

    for key, value in dict_value.items():
        # app_info.\"5min_params\" config['rate_5_min']['cl_table']
        sql_insert = f"INSERT INTO {to_which_table} (val , hfrpok_id) VALUES (\'{value}\', \'{key}\')"
        cursor = connect.cursor()
        try:
            cursor.execute(sql_insert)
            connect.commit()
        except Error as e:
            logger.warning(f"The error {e} occurred")
