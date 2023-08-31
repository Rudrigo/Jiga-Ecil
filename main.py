import configparser
import json
import time
from displayI2c import OLEDDisplay
import RPi.GPIO as GPIO
import time

from mqttComuni import MqttClient
from serialComuni import CommdSerial

class TrafficLight:
    def __init__(self):

        self.diciConfig = {}
        self.diciPayload = {}

        #------------ Display --------------
        self.display = OLEDDisplay(128, 64)
        self.display.clear_display()

        #------------- GPIO ----------------
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinBTN1 = 17
        self.pinBTN2 = 27
        self.pinLED = 4
        # ---------------- GPIO SETUP ---------------------
        GPIO.setup(self.pinBTN1, GPIO.IN)
        GPIO.setup(self.pinBTN2, GPIO.IN)
        GPIO.setup(self.pinLED, GPIO.OUT)
        # ---------------- GPIO ESTADO INICIAL ---------------------
        GPIO.input(self.pinBTN1)
        GPIO.input(self.pinBTN2)
        GPIO.output(self.pinLED, 0)

        # Estados da máquina de estado
        self.state1 = 0
        self.state2 = 0

        cfg = configparser.ConfigParser()
        cfg.read('config.ini')

        self.cTest = CommdSerial()

        self.diciPayload["id"] = cfg.get('DEFAULT', 'id')

        self.diciConfig["server"] = cfg.get('mqtt', 'server')
        self.diciConfig["port"] = cfg.get('mqtt', 'port')
        self.diciConfig["qos"] = cfg.get('mqtt', 'qos')
        self.diciConfig["username"] = cfg.get('mqtt', 'username')
        self.diciConfig["password"] = cfg.get('mqtt', 'password')
        self.diciPayload["topicpub"] = cfg.get('mqtt', 'topicpub')
        self.diciPayload["topicpub2"] = cfg.get('mqtt', 'topicpub2')
        self.diciPayload["topicsub"] = cfg.get('mqtt', 'topicsub')

        self.mqtt_client = MqttClient(broker=self.diciConfig["server"], client_id='501', username=self.diciConfig["username"],
                                 password=self.diciConfig["password"])
        self.tempRef = 999
        self.modeRef = ''
        self.count = 0
        self.state = 0
        self.diciMedia = {'m1': 9.99, 'm2': 9.99, 'm3': 9.99, 'm4': 9.99, 'm5': 9.99}

    def startMQTT(self):
        sub = self.diciPayload['topicsub'].split('+')
        topicSub = sub[0] + self.diciPayload['id'] + sub[1]
        print("Topic Subscriber: "+str(topicSub))
        self.mqtt_client.connect()
        time.sleep(5)
        self.mqtt_client.subscribe(topicSub)

    def receiveMQTT(self):
        payload = self.mqtt_client.recMQTT()
        return payload

    def getTemp(self):
        time.sleep(1)
        try:
            val = self.cTest.monitorTemp()
            temp = val.split(';')
            return {'temppv': temp[0], 'tempaux': temp[1]}
        except:
            val = self.cTest.monitorTemp()
            try:
                temp = val.split(';')
                return {'temppv': temp[0], 'tempaux': temp[1]}
            except:
                return {'temppv': 0.0, 'tempaux': 0.0}

    def startEcil(self, type):
        print("Start Ecil")
        if type == 1:
            self.display.clear_display()
            self.display.show_text("Iniciando!!!", 0, 0)
            self.display.show_text("Jiga ECIL", 0, 15)
            self.display.show_text("Checando Comun", 0, 30)
            self.diciPayload["status"] = 'start'
        elif type == 2:
            self.display.clear_display()
            self.display.show_text("Temperatura", 0, 0)
            self.display.show_text("Estável", 0, 15)
            self.diciPayload["status"] = 'steady'
        elif type == 3:
            self.display.clear_display()
            self.display.show_text("Payload", 0, 0)
            self.display.show_text("Confirmado!", 0, 15)
            self.diciPayload["status"] = 'OK'

        time.sleep(2)
        try:
            temp = self.getTemp()
            self.display.clear_display()
            self.display.show_text("Temp PV: ", 0, 0)
            self.display.show_text(str(temp['temppv']), 80, 0)
            self.diciPayload["temppv"] = temp['temppv']

            self.display.show_text("Temp AUX: ", 0, 15)
            self.display.show_text(str(temp['tempaux']), 80, 15)
            self.diciPayload["tempaux"] = temp['tempaux']

            self.display.show_text("Aguarda GOTA", 0, 30)
            value = self.mqtt_client.connectGota(self.diciPayload, type)
            return value

        except Exception as e:
            print('Exception:')
            print(e)
            self.display.clear_display()
            self.display.show_text("Erro Conn USB: ", 0, 0)
            return {'ERRO':0}

    def configTemp(self, temp):
        self.display.clear_display()
        self.display.show_text("Nova Temp: ", 0, 0)
        self.display.show_text(str(temp), 95, 0)
        self.display.show_text("Ecil estabi...", 0,15)
        self.startEcil(3)
        print('Nova temperatura: '+str(temp))
        self.cTest.sendTemp(float(temp))
        time.sleep(1)

    def calcular_media(self,dicionario):
        soma = 0.0
        count = 0
        for valor in dicionario.values():
            soma += float(valor)
            count += 1
        if count == 0:
            return 0  # Evitar divisão por zero
        media = soma / count
        return media

    def compare_within_percentage(self, value1, value2, percentage):
        if value1 == value2:
            return True
        diff = abs(value1 - value2)
        threshold = (percentage / 100) * max(abs(value1), abs(value2))
        return diff <= threshold
        #Exemplo de uso
        #value_a = 10.0
        #value_b = 9.8
        #percentage_margin = 2  # Margem de 2%

    def run(self):
        self.startMQTT()
        self.startEcil(1)
        while True:
            print("self.receiveMQTT()")
            try:
                result = json.loads(self.receiveMQTT())
                print("result*")
                print(result)
                try:
                    self.tempRef = float(result["set_temp"])
                except:
                    pass
                try:
                    self.modeRef = result["status"]
                except:
                    pass
                print("Tempe**** Referência: "+str(self.tempRef))
                print("Mode**** Referência: " + str(self.modeRef))
                self.configTemp(result["set_temp"])
            except:
                pass

            input_value1 = GPIO.input(self.pinBTN1)
            input_value2 = GPIO.input(self.pinBTN2)

            if self.state1 == input_value1:
                self.display.clear_display()
                self.display.show_text("BTN 1", 0, 0)
                self.display.show_text("Inicia ", 0, 15)
                print("BTN 1")
                time.sleep(2)
                self.startEcil(1)

            elif self.state2 == input_value2:
                self.display.clear_display()
                self.display.show_text("BTN 2", 0, 0)
                self.display.show_text("Abortado ", 0, 15)
                print("BTN 2")
                time.sleep(2)
                break

            if self.modeRef == "start":
                if self.count >= 5:
                    print('Contagem chegou a 10')
                    temp = self.getTemp()
                    for key, value in self.diciMedia.items():
                        print(f"Chave: {key} - Valor: {value}")
                        if key == 'm1':
                            if value == 9.99:
                                self.diciMedia['m1'] = temp['tempaux']
                                break
                        elif key == 'm2':
                            if value == 9.99:
                                self.diciMedia['m2'] = temp['tempaux']
                                break
                        elif key == 'm3':
                            if value == 9.99:
                                self.diciMedia['m3'] = temp['tempaux']
                                break
                        elif key == 'm4':
                            if value == 9.99:
                                self.diciMedia['m4'] = temp['tempaux']
                                break
                        elif key == 'm5':
                            if value == 9.99:
                                self.diciMedia['m5'] = temp['tempaux']
                                break
                            else:
                                result = self.calcular_media(self.diciMedia)
                                print("Media: "+str(result))
                                print("Temp Ref: "+str(self.tempRef))
                                if self.compare_within_percentage(self.tempRef, result, 1.5):
                                    print("Os valores são considerados iguais dentro da margem especificada.")
                                    self.display.clear_display()
                                    self.display.show_text("Temperatura: ", 0, 0)
                                    self.display.show_text(str(self.tempRef), 85, 0)
                                    self.display.show_text("Estável!", 0, 15)
                                    self.startEcil(2)
                                    self.diciMedia = {'m1': 9.99, 'm2': 9.99, 'm3': 9.99, 'm4': 9.99, 'm5': 9.99}

                                else:
                                    print("Os valores não são considerados iguais dentro da margem especificada.")
                                    self.diciMedia = {'m1': 9.99, 'm2': 9.99, 'm3': 9.99, 'm4': 9.99, 'm5': 9.99}

                    self.count = 0
                    print(self.diciMedia)

                print('******************************************')
                time.sleep(2)
                self.count = self.count+1

            elif self.modeRef == "reset":
                time.sleep(2)
                print("Mode reset....")

            else:
                time.sleep(2)
                print("Loop inicial")

if __name__ == "__main__":
    traffic_light = TrafficLight()
    traffic_light.run()
