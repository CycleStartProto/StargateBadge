import usb_cdc
import board
from CommandParser import CommandParser
import asyncio
import busio

MODE_USB = 0
MODE_HARDWARE = 1

class serialCommandReader():
    #serial object for reading
    ser = None
    
    #command parsing object
    CP = None
    
    #Serial mode (USB or hardware)
    Mode = MODE_USB
    
    #input data string storage object
    indata = ''
    
    def __init__(self,comparse, Mode = MODE_USB, txPin = board.GP20, rxPin = board.GP21, bRate = 115200):
        self.Mode = Mode
        if self.Mode == MODE_USB:
            self.ser = usb_cdc.data
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        elif self.Mode == MODE_HARDWARE:
            self.ser = busio.UART(txPin, rxPin, baudrate=bRate)
            self.ser.reset_input_buffer()
        self.CP = comparse
        
    
        
    def readData(self):
        readIn = self.ser.readline()
        self.indata = readIn.decode()[:len(readIn)-1]
        
        
    def parseCommand(self):
        if self.CP.parse(self.indata) == None:
            self.ser.write("ACK\n\r".encode())
        else:
            self.ser.write("NACK\n\r".encode())
            print(self.indata)
        self.ser.flush()
            
    async def handleSer(self):
        self.readData()        
        self.parseCommand()
        
    async def serTask(self):
        while True:
            if self.ser.in_waiting > 0:
                self.handleSer()
            else:
                await asyncio.sleep_ms(10)
        
    