import time

from opcua import Client
from opcua.ua.uaerrors._auto import BadNoCommunication

from distributor import get_config, select_tags, insert_tags_values

config = get_config()


def create_client(to_which_table):
    try:
        client = Client(("opc.tcp://" + config['opcserver_master']['opc_host'] + ":" + config['opcserver_master']['opc_port']))
        client.connect()
        print(f"Connection to master server: opc.tcp://{config['opcserver_master']['opc_host']}:{config['opcserver_master']['opc_port']}")
        process_client(client)
    except Exception:
        client = Client(("opc.tcp://" + config['opcserver_slave']['opc_host'] + ":" + config['opcserver_slave']['opc_port']))
        print(f"Connection to slave server: opc.tcp://{config['opcserver_slave']['opc_host']}:{config['opcserver_slave']['opc_port']}")
        client.connect()
        process_client(client, to_which_table)
    finally:
        client.disconnect()


def process_client(client, to_which_table):
    tags = select_tags()
    print(tags)
    dict_value = {}
    for tag in tags:
        node = client.get_node("ns=1;s=" + tag)
        # print(node.get_data_value())
        try:
            value = node.get_value()
            dict_value[tag] = value
        except Exception as e:
            dict_value[tag] = 0
            # print("Status code: " + e)
    print("Read tags in PostgreSQL DB and values in OPC UA Server!")
    
    for key in dict_value:
        print("{0} : {1}".format(key, dict_value[key]))

    # TODO: def_insert_in_database
    insert_tags_values(dict_value, to_which_table)
    # try:
    #     time.sleep(int(config['rate_5_min']['cl_rate']))
    # except KeyboardInterrupt as e:
    #     print(f"Closing in manual mode {e}")


