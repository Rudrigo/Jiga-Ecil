import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

class OLEDDisplay:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        self.image = Image.new('1', (width, height))
        self.draw = ImageDraw.Draw(self.image)
        # self.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15, encoding="unic")
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf", 15, encoding="unic")

    def clear_display(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.disp.image(self.image)
        self.disp.display()

    def show_text(self, text, x, y):
        self.draw.text((x, y), text, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def show_image(self, image):
        self.disp.image(image)
        self.disp.display()

# Exemplo de uso
#if __name__ == '__main__':
    #display = OLEDDisplay(128, 64)
    #display.clear_display()
    #display.show_text("Jiga ECIL", 0, 0)
    #display.show_text("Modo:Inicial", 0, 18)
    #display.show_text("Temp:-10C", 0, 36)