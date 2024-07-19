import board
from digitalio import *
import microcontroller
import busio as io
import adafruit_ticks
import gc
import os
import supervisor
import asyncio
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
    AR = animReader(CP)
    seReader = serialCommandReader(CP)
    LEDOE.value = 0
    CP.ClearAll()
    CP.frcShow()



async def main():
    trap = False
    while True:
        if not bt1.value and not trap:
            trap = True
            AR.playAnim("dial.anim")
        elif not bt1.value and trap:
            trap = False
            AR.playAnim("close.anim")
        #await asyncio.sleep_ms(10)
    
    

async def go():
    await asyncio.gather(asyncio.create_task(main()), asyncio.create_task(seReader.serTask()))


if __name__ == '__main__':
    initAll()
    asyncio.run(go())
                
            
