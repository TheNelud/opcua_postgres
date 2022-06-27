import time, log

from opcua import Client
from opcua import ua
from opcua.ua.uaerrors._auto import BadNoCommunication

from distributor import *

config = get_config()
# logger = log.get_logger(__name__)


def create_client_post_to_post(to_which_table):
    try:
        client = Client(
            ("opc.tcp://" + config['opcserver_master']['opc_host'] + ":" + config['opcserver_master']['opc_port']))
        print("Connection to master server: opc.tcp://"+config['opcserver_master']['opc_host']+":"+config['opcserver_master']['opc_port']+"\"")
        # logger.info(
        #     "Connection to master server: opc.tcp://"+config['opcserver_master']['opc_host']+":"+config['opcserver_master']['opc_port']+"\"")
        client.connect()
        process_postgres(client, to_which_table)
    except Exception:
        client = Client(
            ("opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port']))
        print("Connection to master server: opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port'] + "\"")
        # logger.warning(
        #     "Connection to master server: opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port'] + "\"")

        client.connect()
        process_postgres(client, to_which_table)
    finally:
        client.disconnect()


def create_client_post_alpha():
    try:
        client = Client(("opc.tcp://admin@" + config['opcserver_master']['opc_host'] + ":" + config['opcserver_master'][
            'opc_port']))
        print("Connection to master server: opc.tcp://"+config['opcserver_master']['opc_host']+":"+config['opcserver_master']['opc_port']+"\"")
        # logger.info(
        #     "Connection to master server: opc.tcp://"+config['opcserver_master']['opc_host']+":"+config['opcserver_master']['opc_port']+"\"")
        client.connect()
        process_alpha(client)
    except Exception:
        client = Client(
            ("opc.tcp://admin@" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port']))
        print("Connection to master server: opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port'] + "\"")
        # logger.warning(
            # f"Connection to slave server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
            # "Connection to master server: opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port'] + "\"")
        client.connect()
        process_alpha(client)
    finally:
        client.disconnect()


def process_postgres(client, to_which_table):
    tags = select_tags()

    dict_value = {}

    # logger.info("Данные прочитаны с базы данных")

    counter = 0
    for tag in [elem[0] for elem in tags]:
        for elem in [elem[1] for elem in tags]:
            node = client.get_node("ns=1;s=" + str(tag))
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
        pass
        print("Пустые значения")
        # logger.warning("Пустые значения")
    print("Данные собраны с сервера opc")
    # logger.info("Данные собраны с сервера opc")

    for key in dict_value:
        print("{0} : {1}".format(key, dict_value[key]))
        # logger.info("{0} : {1}".format(key, dict_value[key]))

    insert_tags_values(dict_value, to_which_table)

    # logger.info("Данные отправлены в базу данных")
    print("Данные собраны с сервера opc")


# TODO: Отправление из базы данных на сервер Alpha

def process_alpha(client):
    tags = select_data_alpha()
    for element in tags:
        print(element)
        node = client.get_node('ns=1;s='+str(element[0]))
        node.set_value(element[1])
        node.get_data_value()

        print(node.get_data_value())

    client.close_session()