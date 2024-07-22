import board
from digitalio import *
import analogio
import microcontroller
import busio as io
import adafruit_ticks
import gc
import os
import math
import supervisor
import adafruit_lis3dh
import rp2pio

import random
import time

from SettingsReader import *
from LedString import LedString
from CommandParser import CommandParser
from serialCommandReader import serialCommandReader
from animReader import animReader

spi = io.SPI(board.GP18, board.GP19, board.GP20)
cs = DigitalInOut(board.GP17)
lis3dh = adafruit_lis3dh.LIS3DH_SPI(spi, cs)

lis3dh.range = adafruit_lis3dh.RANGE_4_G
lis3dh.data_rate = adafruit_lis3dh.DATARATE_25_HZ

LEDOE = DigitalInOut(board.GP9)
LEDOE.direction = Direction.OUTPUT
LEDOE.value = 1

ana = analogio.AnalogIn(board.A0)

bt1 = DigitalInOut(board.GP10)
bt1.direction = Direction.INPUT

bt2 = DigitalInOut(board.GP11)
bt2.direction = Direction.INPUT

bt3 = DigitalInOut(board.GP12)
bt3.direction = Direction.INPUT

bt4 = DigitalInOut(board.GP13)
bt4.direction = Direction.INPUT

'''Gate Statemachine variable,
0 = low battery, no display allowed
1 = startup
2 = ready
3 = dialing
4 = connected
5 = closing

20 = show bat voltage
30 = accel ring mode'''
gateState = 1


mainChevOffset = 36
outerChevOffset = mainChevOffset+36
innerChevOffset = outerChevOffset+36
wormholeOffset = innerChevOffset+36


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
    AR.setAnim(sets.StartupFile)
    
def getBatVoltage():
    return (ana.value*sets.ADCCalScale)+sets.ADCCalOffset




def main():
    global gateState
    trap = False
    bttrap = False
    lastRandCheck = time.monotonic()
    shutdownTime = 0
    currentTime = time.monotonic()
    while True:
        batV = getBatVoltage()
        currentTime = time.monotonic()
        if batV < sets.BatLowVoltageThresh:
            CP.Halt()
            CP.ClearAll()
            CP.frcShow()
            gateState = 0
            
        if bt2.value and bt1.value and bt3.value:
            bttrap = False
            
        if not bt3.value and not bttrap and gateState != 30:
            bttrap = True
            CP.Halt()
            CP.ClearAll()
            CP.setDefaultBrightness()
            gateState = 30
            
        if gateState == 30:
            ringColor = 0x505050
            wormColor = 0x00000B
            ax, ay, az = lis3dh.acceleration
            mag = math.sqrt(math.pow(ax,2)+math.pow(ay,2))
            theta = math.degrees(math.atan2(ax,ay))
            CP.ClearAll()
            if mag < 0.3:
                CP.Set(slice(mainChevOffset,mainChevOffset+18,6),0x880600)
                CP.Set(slice(innerChevOffset,innerChevOffset+18,6),0x880600)
                CP.Set(slice(outerChevOffset,outerChevOffset+18,6),0x880600)
                CP.Set(slice(mainChevOffset+1,mainChevOffset+18,6),0x880600)
                CP.Set(slice(innerChevOffset+1,innerChevOffset+18,6),0x880600)
                CP.Set(slice(outerChevOffset+1,outerChevOffset+18,6),0x880600)
            else:
                center = (190.0+theta)%360
                num = abs(205-((mag/9.8)*200.0))
                left = int((center - (num/2))/10.0)
                right = int((center + (num/2))/10.0)
                if right > 36:
                    CP.Set(slice(0,right-36),ringColor)
                    CP.Set(slice(wormholeOffset,wormholeOffset+(right-36)),wormColor)
                    right = 36
                if left < 0:
                    CP.Set(slice(36+left,36),ringColor)
                    CP.Set(slice(wormholeOffset+(36+left),wormholeOffset+36),wormColor)
                    left = 0
                CP.Set(slice(left,right),ringColor)
                CP.Set(slice(wormholeOffset+left,wormholeOffset+right),wormColor)
            CP.frcShow()
            if not bt3.value and not bttrap:
                bttrap = True
                trap = False
                CP.Halt()
                CP.ClearAll()
                CP.frcShow()
                gateState = 2
                
        if not bt2.value and not bttrap and gateState != 20:
            bttrap = True
            gateState = 20
            CP.Halt()
            CP.ClearAll()
            CP.setDefaultBrightness()
            first = int(batV)
            second = int((batV-first)*10.0)
            third = int((batV-first)*100.0)-second*10
            CP.Set(slice(mainChevOffset,mainChevOffset+first*2),0x880600)
            CP.Set(slice(innerChevOffset,innerChevOffset+first*2),0x880600)
            CP.Set(slice(outerChevOffset,outerChevOffset+first*2),0x880600)
            CP.Set(slice(0,second),0x101010)
            CP.Set(slice(wormholeOffset,wormholeOffset+third),0x101010)
            CP.frcShow()
            
        if gateState == 20:
            if not bt2.value and not bttrap:
                bttrap = True
                trap = False
                CP.Halt()
                CP.ClearAll()
                CP.frcShow()
                gateState = 2
            
        if gateState == 1:
            if AR.animFinished:
                gateState = 2
                
        elif gateState == 2:
            if currentTime > (lastRandCheck+sets.RandomDialCheckInterval) and sets.RandomDialChance != 0:
                lastRandCheck = currentTime
                if random.randint(0,100) < sets.RandomDialChance:
                    gateState = 3
            if not bt1.value and not bttrap:
                bttrap = True
                gateState = 3
                
        elif gateState == 3:
            if not trap:
                AR.setAnim("dial.anim")
                trap = True
            if AR.animFinished:
                trap = False
                if sets.AutoCloseTime != 0:
                    shutdownTime = currentTime + sets.AutoCloseTime
                gateState = 4
                
        elif gateState == 4:
            if not trap:
                AR.setAnim("idle.anim")
                trap = True
            if AR.animFinished:
                trap = False
            if currentTime > shutdownTime and sets.AutoCloseTime != 0:
                trap = False
                gateState = 5
            if not bt1.value and not bttrap:
                bttrap = True
                trap = False
                gateState = 5
                
        elif gateState == 5:
            if not trap:
                AR.setAnim("close.anim")
                trap = True
            if AR.animFinished:
                trap = False
                lastRandCheck = currentTime
                gateState = 2
        AR.cyclicCall()
        seReader.cyclicCall()
        time.sleep(0.001)





if __name__ == '__main__':
    initAll()
    main()


