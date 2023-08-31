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
