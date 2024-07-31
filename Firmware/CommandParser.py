from LedString import LedString
import random
import time

class CommandParser:
    #List of valid commands
    CommandList = [
    "#",
    "CLR",
    "SET",
    "DLY",
    "DEFDLY",
    "RANDLY",
    "BRT",
    "DEFBRT",
    "LOD",
    "HALT",
    "SHOW"]

    #Last (and current) known good command (index of above array)
    Command = -1

    #Last (and current) known good array index
    Index = -1

    #last (and current) array slice
    lastSlice = slice(None,None,None)

    #Last (and current) known good color value
    Color = 0x000000

    #Led String Control Object
    leds = None

    #local frame delay
    frmDelay = 0

    #local brightness
    localBright = 0

    #call pixels.show() when a delay is called
    showOnDelay = True

    #in waiting mode
    waitmode = False

    #monotonic time to run next command
    nextCommandAllowed = 0
    
    #Command Parser Requests a HALT
    haltRequested = False
    
    #command Parser Requests a file load
    loadRequested = False
    
    #load request File name
    loadReqFile = ""

    def __init__(self,ledStringIn,settings):
        self.leds = ledStringIn
        self.sets = settings
        self.frmDelay = self.sets.DefaultFrameDelay
        self.localBright = self.sets.DefaultBrightness

    def isReady(self):
        if time.monotonic()>=self.nextCommandAllowed or not self.waitmode:
            self.waitmode = False
            return True
        else:
            return False

    def parse(self, instr):
        if self.Command == 2:
            return self.parseSet(instr)
        elif self.Command == 1:
            if instr[0] == "I":
                self.lastSlice = self.make_slice(instr[1:len(str)])
                self.Clear(self.lastSlice)
                return 1
            else:
                return self.parseFullCommand(instr)
        else:
            return self.parseFullCommand(instr)


    def parseSet(self,instr):
        if instr[0] == "I":
            strAr = instr.split(" ")
            self.lastSlice = self.make_slice(strAr[0][1:len(strAr[0])])
            self.Index = self.lastSlice.stop-1
            if len(strAr) == 1:
                self.Set(self.lastSlice,self.Color)
                return 1
            elif len(strAr) == 2:
                self.Color = int(strAr[1][1:len(strAr[1])],16)
                self.Set(self.lastSlice,self.Color)
                return 1
            else:
                raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
        elif instr[0] == "C" and instr[1] != "L":
            self.Color = int(instr[1:len(instr)],16)
            self.Index = self.Index+1
            self.singleSet(self.Index,self.Color)
            return 1
        else:
            return self.parseFullCommand(instr)

    def parseFullCommand(self,instr):
        if(instr[0] != "#"):
            strAr = instr.split(" ")
            try:
                self.Command = self.CommandList.index(strAr[0])
            except:
                print("\nInvalid Command, Check Formating, spelling, and capitalization\n")
                return -1
            else:
                if self.Command == 2:
                    if len(strAr) == 3:
                        return self.parseSet(strAr[1]+" "+strAr[2])
                    elif len(strAr) == 2:
                        return self.parseSet(strAr[1])
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 1:
                    if len(strAr) == 2:
                        self.lastSlice = self.make_slice(strAr[1][1:len(strAr[1])])
                        self.Clear(self.lastSlice)
                        return 1
                    elif len(strAr) == 1:
                        self.ClearAll()
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 3:
                    if len(strAr) == 1:
                        self.Delay()
                        return 1
                    elif len(strAr) == 2:
                        self.DelayTime(int(strAr[1][1:len(strAr[1])]))
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 4:
                    if len(strAr) == 2:
                        self.setDefDelay(int(strAr[1][1:len(strAr[1])]))
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 5:
                    if len(strAr) == 3:
                        self.RandomDelay(int(strAr[1][1:len(strAr[1])]),int(strAr[2][1:len(strAr[2])]))
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 6:
                    if len(strAr) == 2:
                        self.Brightness(float(strAr[1][1:len(strAr[1])]))
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 7:
                    if len(strAr) == 1:
                        self.setDefaultBrightness()
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 8:
                    if len(strAr) == 2:
                        self.LoadAnim(strAr[1][0:len(strAr[1])])
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 9:
                    if len(strAr) == 1:
                        self.Halt()
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 10:
                    if len(strAr) == 1:
                        self.frcShow()
                        return 1
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                else:
                    raise Exception("\nInvalid Command\n")


    def make_slice(self,expr):
        def to_piece(s):
            return s and int(s)
        pieces = list(map(to_piece, expr.split(':')))
        if len(pieces) == 1:
            return slice(pieces[0], pieces[0] + 1)
        else:
            return slice(*pieces)

    def ClearAll(self):
        self.leds.pixels.fill(0)

    def Clear(self,indicies):
        self.leds.pixels[indicies] = [(0,0,0)]*len(self.leds.pixels[indicies])

    def singleSet(self,index,color):
        self.leds.pixels[index] = self.leds.rgb_int2tuple(color)
    
    def Set(self, indicies, color):
        self.leds.pixels[indicies] = [self.leds.rgb_int2tuple(color)]*len(self.leds.pixels[indicies])

    def Delay(self):
        if self.showOnDelay:
            self.leds.show()
        self.waitmode = True
        self.nextCommandAllowed = time.monotonic()+(self.frmDelay/1000.0)

    def setDefDelay(self, delTime):
        self.frmDelay = delTime

    def DelayTime(self, delTime):
        if self.showOnDelay:
            self.leds.show()
        self.waitmode = True
        self.nextCommandAllowed = time.monotonic()+(delTime/1000.0)

    def RandomDelay(self,Lower,Upper):
        if self.showOnDelay:
            self.leds.show()
        self.waitmode = True
        self.nextCommandAllowed = time.monotonic()+(random.randint(Lower,Upper)/1000.0)

    def Brightness(self,val):
        self.localBright = val
        self.leds.setBrightness(val)
        self.leds.show()

    def setDefaultBrightness(self):
        self.localBright = self.sets.DefaultBrightness
        self.leds.setBrightness(self.localBright)
        self.leds.show()

    def frcShow(self):
        self.leds.show()

    def LoadAnim(self,file):
        self.sets.loadRequested = True
        self.sets.loadReqFile = file

    def Halt(self):
        self.sets.haltRequested = True



if __name__ == '__main__':
    cp = CommandParser()
    test = [1,2,3,4,5,6,7,8,9]
    cp.parse("BRT B0.5")
    cp.parse("DEFBRT")
    cp.parse("SET I1:5 C0000ff")
    cp.parse("I0 CFF0000")
    cp.parse("I3")
    cp.parse("I4")
    cp.parse("#test")
    cp.parse("I5")
    cp.parse("C00FF00")
    cp.parse("C00FA00")
    cp.parse("DLY")
    cp.parse("CLR I2")
    cp.parse("I3")
    cp.parse("I4")
    cp.parse("I5")
    cp.parse("CLR")
    cp.parse("DLY T50")
    cp.parse("DEFDLY T30")
    cp.parse("RANDLY L10 H1000")
    cp.parse("LOD test.anim")
    cp.parse("HALT")
    cp.parse("#test Comment")


