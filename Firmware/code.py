import board
from digitalio import *
import microcontroller
import busio as io
import adafruit_ticks
import gc
import os
import supervisor
import rp2pio

import random
import time

from SettingsReader import *
from LedString import LedString
from CommandParser import CommandParser
from serialCommandReader import serialCommandReader
from animReader import animReader



LEDOE = DigitalInOut(board.GP9)
LEDOE.direction = Direction.OUTPUT
LEDOE.value = 1

bt1 = DigitalInOut(board.GP10)
bt1.direction = Direction.INPUT


def initAll():
    global dispFilePath
    global ser
    global LEDOE
    global sets
    global analog
    global leds
    global CP
    global AR
    global seReader
    microcontroller.cpu.frequency = 133000000
    sets = BoardSettings("BoardSettings.txt")
    leds = LedString(sets)
    CP = CommandParser(leds,sets)
    AR = animReader(leds,sets)
    seReader = serialCommandReader(leds,sets)
    LEDOE.value = 0
    CP.ClearAll()
    CP.frcShow()



def main():
    trap = False
    while True:
        if AR.animFinished:
            if not bt1.value and not trap:
                trap = True
                AR.setAnim("dial.anim")
            elif not bt1.value and trap:
                trap = False
                AR.setAnim("close.anim")
        AR.cyclicCall()
        seReader.cyclicCall()
        time.sleep(0.001)





if __name__ == '__main__':
    initAll()
    main()


