from opcua import Client
from parse_config import ParserXML
from logger_info import LogginMyApp
from postgres import Postgres


class OpcUAClient():
    def __init__(self):
        self.pXML = ParserXML().parser()
        self.logger= LogginMyApp().get_logger(__name__)
        self.selectTags = Postgres().selectTags()
        self.dictValue = {}
        self.counter = 0

    def connectClient(self):
        try:
            self.client = Client(self.pXML['opcserver_master']['opc_host'])
            self.client.connect()
            self.logger.info("Connect master server: " + self.pXML['opcserver_master']['opc_host'])
            
        except Exception:
            self.client = Client(self.pXML['opcserver_slave']['opc_host'])
            self.client.connect()
            self.logger.warning("Connect slave server: " + self.pXML['opcserver_master']['opc_host'])
        
    def processPostrgres(self):
        for self.tag in [self.elem[0] for self.elem in self.selectTags]:
            for self.elem in [self.elem[1] for self.elem in self.selectTags]:
                self.node = self.connectClient().get_node('ns=1;s=' + str(self.selectTags))
                print(self.node)
                try:
                    self.value = self.node.get_value()
                    self.dictValue[self.elem] = self.value
                except Exception as e:
                    self.dictValue[self.elem] = 0
                    self.counter += 1
        print(self.dictValue)
        if self.counter > 0: 
            self.logger.warning("Пустые значения")
        self.logger.info("Данные собраны с сервера OPC")

        #TODO : отправление в базу данных значений с сервера OPC



    def processAlpha(self):
        # TODO: Отправление из базы данных на сервер Alpha
        pass
        

if __name__ == '__main__':
    OpcUAClient().connectClient()