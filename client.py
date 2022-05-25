import time, log

from opcua import Client
from opcua.ua.uaerrors._auto import BadNoCommunication

from distributor import get_config, select_tags, insert_tags_values

config = get_config()
logger = log.get_logger(__name__)


def create_client(to_which_table):
    try:
        client = Client(("opc.tcp://" + config['opcserver_master']['opc_host'] + ":" + config['opcserver_master']['opc_port']))
        client.connect()
        logger.info(f"Connection to master server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
        process_client(client, to_which_table)
    except Exception:
        client = Client(("opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port']))
        logger.warning(f"Connection to slave server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
        client.connect()
        process_client(client, to_which_table)
    finally:
        client.disconnect()


def process_client(client, to_which_table):
    tags = select_tags()
    logger.info("Данные прочитаны с базы данных")
    dict_value = {}
    counter = 0
    for tag in tags:
        node = client.get_node("ns=1;s=" + tag)
        try:
            value = node.get_value()
            dict_value[tag] = value
        except Exception as e:
            dict_value[tag] = 0
            counter += 1
            # print("Status code: " + e)
    if counter > 0:
        logger.warning("Пустые значения")
    logger.info("Данные собраны с сервера opc")
    
    # for key in dict_value:
    #     logger.info("{0} : {1}".format(key, dict_value[key]))

    # TODO: def_insert_in_database
    insert_tags_values(dict_value, to_which_table)
    logger.info("Данные отправлены в базу данных")
    


