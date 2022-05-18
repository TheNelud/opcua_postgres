import time

from opcua import Client

from distributor import get_config, select_tags, insert_tags_values

config = get_config()


def create_client():
    global client
    try:
        client = Client(("opc.tcp://" + config['opc_host_master'] + ":" + config['opc_port_master']))
        client.connect()
        print(f"Connection to master server: opc.tcp://{config['opc_host_master']}:{config['opc_port_master']}")
        while True:
            process_client(client)
    except Exception:
        client = Client(("opc.tcp://" + config['opc_host_slave'] + ":" + config['opc_port_slave']))
        print(f"Connection to slave server: opc.tcp://{config['opc_host_slave']}:{config['opc_port_slave']}")
        client.connect()
        while True:
            process_client(client)
    finally:
        client.disconnect()




def process_client(client):
    tags = select_tags()
    dict_value = {}
    for tag in tags:
        value_node = client.get_node("ns=1;s=" + tag)
        value = value_node.get_value()
        dict_value[tag] = value
    print("Read tags in PostgreSQL DB and values in OPC UA Server!")
    for key in dict_value:
        print("{0} : {1}".format(key, dict_value[key]))

    # TODO: def_insert_in_database
    insert_tags_values(dict_value)
    try:
        time.sleep(int(config['cl_rate']))
    except KeyboardInterrupt as e:
        print(f"Closing in manual mode {e}")


