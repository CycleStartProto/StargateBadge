import board
from SettingsReader import BoardSettings
from adafruit_neopxl8 import NeoPxl8
import colorsys

class LedString:
    settings = None
    pixels = []
    brightness = 1.0
    def __init__(self,sets):
        self.settings = sets
        firstChannel = board.GP0
        self.pixels = NeoPxl8(
            firstChannel,
            self.settings.StrandLength*8,
            num_strands = 8,
            auto_write=False,
            brightness=self.settings.DefaultBrightness,
        )
        self.brightness = self.settings.DefaultBrightness
        self.show()
        
    def rgb_int2tuple(self, rgbint):
        return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

    def rgb_tuple2int(self, tup=(0, 0, 0)):
        return tup[2] + (tup[1] << 8) + (tup[0] << 16)

    def colorHSV(self, hue, sat, val):
        return self.rgb_tuple2int(colorsys.hsv_to_rgb(hue,sat,val))
        
    def setBrightness(self, brightness):
        if brightness >= 1.0:
            self.brightness = 1.0
        elif brightness <= 0.0:
            self.brightness = 0.0
        else:
            self.brightness = brightness
        self.pixels.brightness = self.brightness
        
    def show(self):
        self.pixels.show()