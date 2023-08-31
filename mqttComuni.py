import paho.mqtt.client as mqtt
import json
import time

class MqttClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):

        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id)
        self.connected = False
        if username is not None and password is not None:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.payload = ''

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexão estabelecida com sucesso! - on_connect")
            self.connected = True
        else:
            print("Falha na conexão. Código de retorno =", rc)
            self.connected = False

    def on_publish(self, client, userdata, mid):
        print("Mensagem publicada com sucesso!")

    def on_message(self, client, userdata, msg):
        print(f"Nova mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
        self.payload = msg.payload.decode()

    def on_disconnect(self, client, userdata, msg):
        print("Disconectado!!!")

    def connect(self):
        print("Connect")
        self.client.connect(self.broker, port=self.port, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        """print('publish')
        print('topic')
        print(topic)
        print('message')
        print(message)"""
        if self.connected:
            self.client.publish(topic, message)
        else:
            print("Não conectado ao broker MQTT. - Publish")

    def subscribe(self, topic, qos=0):
        if self.connected:
            self.client.subscribe(topic, qos)
        else:
            print("Não conectado ao broker MQTT. - Subscribe")

    def connectGota(self, diciPay, type):
        time.sleep(1)
        if type == 1:
            pub = diciPay['topicpub'].split('+')
            topicPub = pub[0] + diciPay['id'] + pub[1]
            #diciPay['status'] = 'start'

        if type == 2:
            pub = diciPay['topicpub2'].split('+')
            topicPub = pub[0] + diciPay['id'] + pub[1]
            #diciPay['status'] = 'steady'

        if type == 3:
            pub = diciPay['topicpub2'].split('+')
            topicPub = pub[0] + diciPay['id'] + pub[1]

        pay = {"status": diciPay['status'], "temppv": diciPay['temppv'], "tempaux": diciPay['tempaux']}

        print("topicPub: "+str(topicPub))
        print("pay: " +str(pay))
        json_string = json.dumps(pay)
        self.client.publish(topicPub, json_string)
        time.sleep(1)

    def recMQTT(self):
        pay = self.payload
        self.payload = ''
        return pay

#if __name__ == '__main__':
    #diciPay = {'id': '0623', 'topicpub': 'senfio/monitore/+/gota/cb/jiga/status',
    #'topicsub': 'senfio/monitore/+/gota/cb/jiga/status/return', 'status': 'start', 'temppv': '1.0', 'tempaux': '0.8'}


    #mqtt_client = MqttClient(broker="connectt.vps-kinghost.net", client_id='0623', username="admin", password="##Cd9500$$")
    # Conectando ao broker
    #mqtt_client.connect()
    #time.sleep(2)
    #value = mqtt_client.connectGota(diciPay)
    #print(type(value))
    #print(value)
