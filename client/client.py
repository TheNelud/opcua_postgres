import time, log

from opcua import Client
from opcua.ua.uaerrors._auto import BadNoCommunication

from distributor import get_config, select_tags, insert_tags_values

config = get_config()
logger = log.get_logger(__name__)


def create_client():
    try:
        client = Client(("opc.tcp://" + config['opcserver_master']['opc_host'] + ":" + config['opcserver_master']['opc_port']))
        logger.info(f"Connection to master server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
        return client.connect()
    except Exception:
        client = Client(("opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port']))
        logger.warning(f"Connection to slave server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
        return client.connect()
    finally:
        client.disconnect()


def process_postgres(client, to_which_table):
    tags = select_tags()

    dict_value = {}

    logger.info("Данные прочитаны с базы данных")
    
    counter = 0
    for tag in [elem[0] for elem in tags]:
        for elem in [elem[1] for elem in tags]:
            node = client.get_node(f"ns=1;s=" + str(tag))
            # print(node)
            try:
                value = node.get_value()
                dict_value[elem] = value
            except Exception as e:
                dict_value[elem] = 0
                counter += 1
            # print("Status code: " + e)
    print(dict_value) 
    if counter > 0:
        logger.warning("Пустые значения")
    logger.info("Данные собраны с сервера opc")
    
    for key in dict_value:
        logger.info("{0} : {1}".format(key, dict_value[key]))

    # TODO: def_insert_in_database
    insert_tags_values(dict_value, to_which_table)

    logger.info("Данные отправлены в базу данных")

#TODO: Отправление из базы данных на сервер Alpha

def process_alpha():
    pass
     
def postgres_opc_postgres(to_which_table):
    process_postgres(create_client(), to_which_table)

def postgres_opc():
    process_alpha()

