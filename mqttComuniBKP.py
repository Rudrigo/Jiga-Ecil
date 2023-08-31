import configparser
from random import random, randrange
import paho.mqtt.client as mqtt
import time

"""class CommdMqtt():
    def __init__(self):
        print("MQTT Functions")

        self.diciConfMqtt ={}
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')

        self.diciConfMqtt['server'] = self.cfg.get('mqtt', 'server')
        self.diciConfMqtt['port'] = self.cfg.get('mqtt', 'port')
        self.diciConfMqtt['qos'] = self.cfg.get('mqtt', 'qos')
        self.diciConfMqtt['username'] = self.cfg.get('mqtt', 'username')
        self.diciConfMqtt['password'] = self.cfg.get('mqtt', 'password')
        self.diciConfMqtt['topicpub'] = self.cfg.get('mqtt', 'topicpub')
        self.diciConfMqtt['topicsub'] = self.cfg.get('mqtt', 'topicsub')
        self.diciConfMqtt['keepalive'] = self.cfg.get('mqtt', 'keepalive')
        self.diciConfMqtt['userid'] = self.cfg.get('mqtt', 'userid')"""

class MqttClient:
    def __init__(self, broker_address, port=1883, client_id='500', username=None, password=None):
        self.client = mqtt.Client(client_id)

        if username is not None and password is not None:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_address = broker_address
        self.port = port

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado com código de resultado {rc}")

    def on_message(self, client, userdata, message):
        print(f"Mensagem recebida '{message.payload.decode()}' no topic '{message.topic}'")

    def connect(self):
        self.client.connect(self.broker_address, self.port)
        self.client.loop_start()

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Inscrito no topic '{topic}'")

    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"Mensagem publicada '{message}' no topic '{topic}'")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Desconectado")

    def sorteio(self):
        result = randrange(1, 100)
        return result

if __name__ == '__main__':
    mqtt_client = MqttClient("connectt.vps-kinghost.net", username="admin", password="##Cd9500$$")
    mqtt_client.connect()
    mqtt_client.subscribe("test/topic")
    time.sleep(5)
    mqtt_client.publish("test/topic", mqtt_client.sorteio())
    time.sleep(5)
    mqtt_client.disconnect()