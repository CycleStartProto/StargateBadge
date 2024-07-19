from LedString import LedString
import random
import time
import asyncio

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
    
    #Print debug output
    debug = False
    
    #local frame delay 
    frmDelay = 0
    
    #local brightness
    localBright = 0
    
    #call pixels.show() when a delay is called
    showOnDelay = True
    
    def __init__(self,ledStringIn,settings):
        self.leds = ledStringIn
        self.sets = settings
        self.frmDelay = self.sets.DefaultFrameDelay
        self.localBright = self.sets.DefaultBrightness
    
    def parse(self, instr):
        str = instr
        if self.Command == 2:
            return self.parseSet(instr)
        elif self.Command == 1:
            if str[0] == "I":
                self.lastSlice = self.make_slice(str[1:len(str)])
                self.Clear(self.lastSlice)
                return None
            else:
                return self.parseFullCommand(instr)
        else:
            return self.parseFullCommand(instr)
            
    def parseSet(self,instr):
        str = instr
        if str[0] == "I":
            strAr = str.split(" ")
            self.lastSlice = self.make_slice(strAr[0][1:len(strAr[0])])
            self.Index = self.lastSlice.stop-1
            if len(strAr) == 1:
                self.Set(self.lastSlice,self.Color)
                return None
            elif len(strAr) == 2:
                self.Color = int(strAr[1][1:len(strAr[1])],16)
                self.Set(self.lastSlice,self.Color)
                return None
            else:
                raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
        elif str[0] == "C" and str[1] != "L":
            self.Color = int(str[1:len(str)],16)
            self.Index = self.Index+1
            self.Set(slice(self.Index,self.Index+1),self.Color)
            return None
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
                        return None
                    elif len(strAr) == 1:
                        self.ClearAll()
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 3:
                    if len(strAr) == 1:
                        asyncio.run(self.Delay())
                        return None
                    elif len(strAr) == 2:
                        asyncio.run(self.DelayTime(int(strAr[1][1:len(strAr[1])])))
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 4:
                    if len(strAr) == 2:
                        self.setDefDelay(int(strAr[1][1:len(strAr[1])]))
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 5:
                    if len(strAr) == 3:
                        asyncio.run(self.RandomDelay(int(strAr[1][1:len(strAr[1])]),int(strAr[2][1:len(strAr[2])])))
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 6:
                    if len(strAr) == 2:
                        self.Brightness(float(strAr[1][1:len(strAr[1])]))
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 7:
                    if len(strAr) == 1:
                        self.setDefaultBrightness()
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 8:
                    if len(strAr) == 2:
                        self.LoadAnim(strAr[1][0:len(strAr[1])])
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 9:
                    if len(strAr) == 1:
                        self.Halt()
                        return None
                    else:
                        raise Exception("Failed To Parse Command, Incorrect Number of Parameters")
                elif self.Command == 10:
                    if len(strAr) == 1:
                        self.frcShow()
                        return None
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
        if self.debug:
            print("Clearing All")
        self.leds.pixels.fill(0)
        
    def Clear(self,indicies):
        if self.debug:
            print("Clearing: "+str(indicies))
        self.leds.pixels[indicies] = [(0,0,0)]*len(self.leds.pixels[indicies])
        
    def Set(self, indicies, color):
        if self.debug:
            print("Setting: "+str(indicies)+" to color: "+f"{color:#0{8}x}")
        self.leds.pixels[indicies] = [self.leds.rgb_int2tuple(color)]*len(self.leds.pixels[indicies])
        
    async def Delay(self):
        if self.debug:
            print("delaying 1 frame")
        if self.showOnDelay:
            self.leds.show()
        await asyncio.sleep_ms(self.frmDelay)
    
    def setDefDelay(self, delTime):
        if self.debug:
            print("seting default frame delay to: "+str(delTime)+" ms")
        self.frmDelay = delTime
        
    async def DelayTime(self, delTime):
        if self.debug:
            print("Delaying "+str(delTime)+" ms")
        if self.showOnDelay:
            self.leds.show()
        await asyncio.sleep_ms(delTime)
        
    async def RandomDelay(self,Lower,Upper):
        if self.debug:
            print("Random Delay, Lower: "+str(Lower)+" Upper: "+str(Upper))
        if self.showOnDelay:
            self.leds.show()
        await asyncio.sleep_ms(random.randint(Lower,Upper))
        
    def Brightness(self,val):
        if self.debug:
            print("Setting Brightness: "+str(val))
        self.localBright = val
        self.leds.setBrightness(val)
        self.leds.show()
        
    def setDefaultBrightness(self):
        if self.debug:
            print("Restoring Default Brightness")
        self.localBright = self.sets.DefaultBrightness
        self.leds.setBrightness = self.localBright
        self.leds.show()
        
    def frcShow(self):
        if self.debug:
            print("updating pixels")
        self.leds.show() 
        
    #!!! these are NOT implimented yet !!!#
    def LoadAnim(self,file):
        if self.debug:
            print("Loading anim file: "+file)
        
    def Halt(self):
        if self.debug:
            print("Halting Current animation")
            
    
        
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
    
    