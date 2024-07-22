class BoardSettings:
    
    #Global interface variables
    loadRequested = False
    loadReqFile = ""
    haltRequested = False

    #settings Managed By this class:
    StartupFile = ""
    StrandLength = 8
    DefaultFrameDelay = 15
    DefaultBrightness = 0.3
    BatLowVoltageThresh = 3.0
    ADCCalScale = 0
    ADCCalOffset = 0
    
    AutoCloseTime = 0
    RandomDialCheckInterval = 0
    RandomDialChance = 0
    
    def __init__(self, filename):
        self.loadSettings(filename)
    
    def readString(self,text,name):
        retval = ""
        try:
            startIndex = text.index(name)
        except:
            print("Failed to find: "+name+" in file")
        else:
            j = startIndex+len(name)
            parsestring = ""
            while text[j] != ";":
                parsestring = parsestring+text[j]
                j+=1
            retval = parsestring
        finally:
            return retval
            
    def readInt(self, text, name):
        retval = 0
        try:
            startIndex = text.index(name)
        except:
            print("Failed to find: "+name+" in file")
        else:
            j = startIndex+len(name)
            parsestring = ""
            while text[j] != ";":
                parsestring = parsestring+text[j]
                j+=1
            retval = int(parsestring)
        finally:
            return retval
        
    def readFloat(self, text, name):
        retval = 0
        try:
            startIndex = text.index(name)
        except:
            print("Failed to find: "+name+" in file")
        else:
            j = startIndex+len(name)
            parsestring = ""
            while text[j] != ";":
                parsestring = parsestring+text[j]
                j+=1
            retval = float(parsestring)
        finally:
            return retval

    def loadSettings(self, file):
        with open(file, 'rt') as f:
            text = f.read()
        
        #Read Startup File
        self.StartupFile = self.readString(text,"Startup File: ")
        #Read Strand Lengths
        self.StrandLength = self.readInt(text,"Strand Length: ")
        #Read Default Frame Delay
        self.DefaultFrameDelay = self.readInt(text,"Default Frame Delay: ")
        #Read Default Brightness
        self.DefaultBrightness  = self.readFloat(text,"Default Brightness: ")
        #Read Current Shunt Scale
        self.ADCCalScale = self.readFloat(text,"ADC Scale: ")
        #Read Current Shunt Offset
        self.ADCCalOffset = self.readFloat(text,"ADC Offset: ")
        #Read the auto close time
        self.AutoCloseTime = self.readFloat(text,"Auto Close Time: ")
        #Read Random Dial Check Interval
        self.RandomDialCheckInterval = self.readFloat(text,"Random Dial Check: ")
        #Read Random Dial Check Chance
        self.RandomDialChance = self.readInt(text,"Random Dial Chance: ")
        #Read Battery Low Voltage Threshold
        self.BatLowVoltageThresh = self.readFloat(text,"Low Voltage Thresh: ")
        
    def printSettings(self):
        print("Mode: "+str(self.Mode))
        print("Serial ID: "+str(self.SerialID))
        print("Startup File: "+self.StartupFile)
        print("Strand Length: "+str(self.StrandLength))
        print("Default Frame Delay: "+str(self.DefaultFrameDelay))
        print("Default Brightness: "+str(self.DefaultBrightness))
        print("ADC Scale: "+str(self.ShuntCalScale))
        print("ADC Offset: "+str(self.ShuntCalOffset))
        
        
if __name__ == '__main__':
    sets = BoardSettings("BoardSettings.txt")
    sets.printSettings()


