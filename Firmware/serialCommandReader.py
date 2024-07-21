import usb_cdc
import board
from CommandParser import CommandParser
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
    
    oldReady = True
    
    endOfLine = False

    def __init__(self,leds,sets, Mode = MODE_USB, txPin = board.GP20, rxPin = board.GP21, bRate = 115200):
        self.Mode = Mode
        if self.Mode == MODE_USB:
            self.ser = usb_cdc.data
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        elif self.Mode == MODE_HARDWARE:
            self.ser = busio.UART(txPin, rxPin, baudrate=bRate)
            self.ser.reset_input_buffer()
        else:
            raise exception("invalid serial type")
        self.CP = CommandParser(leds,sets)



    def readData(self):
        while self.ser.in_waiting > 0:
            char = self.ser.read(1).decode()
            if char == "\n" or char == "\r":
                self.endOfLine = True
                self.ser.flush()
                break
            self.indata = self.indata+char


    def parseCommand(self):
        if self.CP.parse(self.indata) == 1:
            if self.CP.isReady():
                self.ser.write("ACK\n\r".encode())
            else:
                self.ser.write("WAIT\n\r".encode())
        else:
            self.ser.write("NACK\n\r".encode())
            print(self.indata)
        

    def handleSer(self):
        self.readData()
        if self.endOfLine:
            self.parseCommand()
            self.indata = ''
            self.endOfLine = False

    def cyclicCall(self):
        isready = self.CP.isReady()
        if self.oldReady != isready:
                print("changed")
                print(self.oldReady)
                print(isready)
                self.oldReady = isready
                if isready:
                    self.ser.write("ACK\n\r".encode())
        if isready:
            if self.ser.in_waiting > 0:
                self.handleSer()



