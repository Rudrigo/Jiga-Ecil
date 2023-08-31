import binascii
import configparser
import serial
import time
import struct

class CommdSerial():
    def __init__(self):
        print("Command Test")

        self.diciSerial ={}
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini')

        self.diciSerial['port'] = self.cfg.get('serial', 'serial')
        self.diciSerial['baud'] = self.cfg.get('serial', 'baudrate')
        self.diciSerial['stat'] = self.cfg.get('serial', 'stat')

        self.diciGetsCommands = {
            'getTempAuxProbe': [1, 82, 187, 221, 0, 0, 0, 0],
            'getTempSetPoint': [1, 82, 177, 221, 0, 0, 0, 0],
            'getTempPV':       [1, 82, 178, 221, 0, 0, 0, 0],
            'getValorCHEntrada': [1, 82, 170, 221, 0, 0, 0, 0],
            'getConfigCHEntrada': [1, 82, 170, 204, 0, 0, 0, 0]
        }

        self.tolerancia = 0.1
        self.contagemQld = 10

    def montPayload(self, end, cmd, cha, mod, bt1, bt2, bt3, bt4):
        crc = (end ^ cmd ^ cha ^ mod ^ bt1 ^ bt2 ^ bt3 ^ bt4)
        print('montPayload')
        payBody = [hex(end)[2:]]
        payBody.append(hex(cmd)[2:])
        payBody.append(hex(cha)[2:])
        payBody.append(hex(mod)[2:])
        payBody.append(hex(bt1)[2:])
        payBody.append(hex(bt2)[2:])
        payBody.append(hex(bt3)[2:])
        payBody.append(hex(bt4)[2:])
        payBody.append(hex(crc)[2:])
        newPay = []
        for i in payBody:
            if len(i) == 1:
                newPay.append('0' + i)
            else:
                newPay.append(i)
        print(newPay)
        paySend = binascii.unhexlify(''.join(newPay))
        return paySend

    def verifyPort(self):
        try:
            objVerify = serial.Serial(self.diciSerial['port'])
            if objVerify:
                return True
        except serial.SerialException:
            return False

    def writePort(self, cmd):
        listCmd = []
        try:
            Obj_porta = serial.Serial(self.diciSerial['port'], self.diciSerial['baud'], timeout=0.1)
            Obj_porta.write(cmd)
            response = Obj_porta.readline()  # Currently stops reading on timeout...
            Obj_porta.close()
            value = response.hex(sep=' ')
            for i in value.split(' '):
                listCmd.append(i)
            return listCmd

        except serial.SerialException:
            print("ERRO: Verifique se ha algum dispositivo conectado na porta!")
            return {'ERRO':0000}

    # Converte a string hexadecimal para bytes
    def ieee754_hex_to_decimal(self, hex_string):
        hex_bytes = bytes.fromhex(hex_string)
        if len(hex_bytes) != 4:
            raise ValueError("A string hexadecimal deve conter exatamente 8 dígitos.")
        decimal_value = struct.unpack('f', hex_bytes)[0]
        return decimal_value

    # Empacota o número decimal usando o formato 'f' (float de 4 bytes - IEEE 754)
    # Se você deseja mais precisão, use o formato 'd' (float de 8 bytes - IEEE 754)
    def decimal_to_ieee754_hex(self, decimal_value):
        binary_representation = struct.pack('f', decimal_value)
        hex_representation = binary_representation.hex()
        return hex_representation

    # Empacota o número decimal usando o formato 'f' (float de 4 bytes - IEEE 754)
    def decimal_to_ieee754_hex(self, decimal_value):
        binary_representation = struct.pack('f', decimal_value)
        hex_representation = binary_representation.hex()
        return hex_representation

    def reverse_list(self, input_list):
        return input_list[::-1]

    def hex_to_decimal(self, hex_string):
        decimal_value = int(hex_string, 16)
        return decimal_value

    def sendTemp(self, temp):
        print("Temperatura setada: "+str(temp))
        result = self.decimal_to_ieee754_hex(temp)
        resultList = [result[i:i + 2] for i in range(0, len(result), 2)]
        resultList = self.reverse_list(resultList)
        pay = self.montPayload(1, 87, 177, 221, self.hex_to_decimal(resultList[0]), self.hex_to_decimal(resultList[1]), self.hex_to_decimal(resultList[2]), self.hex_to_decimal(resultList[3]))
        rest = self.writePort(pay)  # Escrever set - point
        return rest

    def getTemp(self, cmd):
        result = self.writePort(self.montPayload(cmd[0], cmd[1], cmd[2], cmd[3], cmd[4], cmd[5], cmd[6], cmd[7]))
        result = self.ieee754_hex_to_decimal(str(result[7]+result[6]+result[5]+result[4]))
        return round(result, 2)

    def monitorTemp(self):
        cmd1 = self.diciGetsCommands['getTempPV']
        time.sleep(1)
        cmd2 = self.diciGetsCommands['getTempAuxProbe']
        time.sleep(1)
        while(True):
            try:
                temp = self.getTemp(cmd1)
                print("A temperatura PV = " + str(temp))
                time.sleep(1)
                temp2 = self.getTemp(cmd2)
                print("A temperatura AuxProbe = " + str(temp2))
                time.sleep(1)
                return str(temp)+";"+str(temp2)
            except:
                print("*Erro na leitura")
                #quit()
                return {'ERRO':0000}


#if __name__ == '__main__':
    #cTest = CommdSerial()
    #temp = '10'

    #if cTest.verifyPort():
        #print('Porta OK')
    #else:
        #print('Porta Erro!')

    #cTest.monitorTemp()
    #time.sleep(2)
    #ret = cTest.sendTemp(-8.00)
    #print(cTest.sendTemp(float(temp)))



