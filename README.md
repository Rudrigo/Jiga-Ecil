# Jiga-Ecil
Sistema em python3 

Jiga Ecil (Sistema desenvolvindo em Python3 ) - 31/08/23
O sistema rodará em linux(raspbian) na Raspberry PI 3  

Preparar ambiente:

Passo 1:
  Instalar OS Desktop Raspbian: https://www.raspberrypi.com/documentation/computers/getting-started.html

Passo 2: 
  sudo apt install python3-pip    
  sudo pip install Adafruit-SSD1306
  sudo pip3 install paho-mqtt
  sudo pip3 install pyserial
  sudo apt install -y i2c-tools
  sudo apt install -y git
  git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
  cd Adafruit_Python_SSD1306
  sudo python3 setup.py install

Passo 3:
  O programa deve ser instalado dentro da pasta em qualquer direório, exemplo "/home/pi/Desktop/JIGA" dentro 
  dela copiar todos arquivos do git.
  Para executar o programa basta usar o comando '$python3 main.py'

Modelo de contrato entre Jiga e Gota:
  Ao ligar jiga envia para GOTA: 
  senfio/monitore/0111/gota/cb/jiga/status/ack {"status": "start", "temppv": "8.0", "tempaux": "7.98"}
  
  Gota envia para Jiga a primeira vez/inicio:
  senfio/monitore/0111/gota/cb/jiga/status {"timeack": "30/08/23 17:43:07", "status": "start", "set_temp": "8.0"}
  
  Jiga confirma recebimento em:
  senfio/monitore/0111/gota/cb/jiga/steady/ack { "status": "OK", "temppv": "8.0", "tempaux": "7.98"}
  
  Jiga envia estabiliade em:
  senfio/monitore/0111/gota/cb/jiga/steady/ack { "status": "steady", "temppv": "8.0", "tempaux": "7.98"}
  
  Gota envia para Jiga a reset:
  senfio/monitore/0111/gota/cb/jiga/status {"timeack": "30/08/23 17:43:07", "status": "reset"}


Arquivo config.ini nele contempla as configurações diversas:
---------------------- Arquivo *.ini -------------------------------
  [DEFAULT]
  version=1.0
  author=Rudrigo Lima
  id=0111 // Código de identidade da máquina
 
  [mqtt] // Parâmetros do servidor MQTT
  server=connectt.net
  port=1883
  qos=0
  username=#######
  password=#######
  topicpub=senfio/monitore/+/gota/cb/jiga/status/ack
  topicpub2=senfio/monitore/+/gota/cb/jiga/steady/ack
  topicsub=senfio/monitore/+/gota/cb/jiga/status
  keepalive=60
  userid = 500
  
  [serial] // Porta serial USB
  serial=/dev/ttyUSB0
  baudrate=9600
  stat=1
