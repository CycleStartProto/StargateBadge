class BoardSettings:
    
    #Global interface variables
    loadRequested = False
    loadReqFile = ""
    haltRequested = False

    #settings Managed By this class:
    Mode = 2
    SerialID = 0
    StartupFile = ""
    BoardCurrentLimit = 1000
    StrandLength = 8
    DefaultFrameDelay = 15
    DefaultBrightness = 0.3
    ShuntCalScale = 0
    ShuntCalOffset = 0
    
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
        
        #Read Operating Mode
        self.Mode = self.readInt(text,"Mode: ")
        #Read Serial Channel ID
        self.SerialID = self.readInt(text,"Serial ID: ")
        #Read Startup File
        self.StartupFile = self.readString(text,"Startup File: ")
        #Read Board Current Limit
        self.BoardCurrentLimit = self.readInt(text,"Board Current: ")
        #Read Strand Lengths
        self.StrandLength = self.readInt(text,"Strand Length: ")
        #Read Default Frame Delay
        self.DefaultFrameDelay = self.readInt(text,"Default Frame Delay: ")
        #Read Default Brightness
        self.DefaultBrightness  = self.readFloat(text,"Default Brightness: ")
        #Read Current Shunt Scale
        self.ShuntCalScale = self.readFloat(text,"Shunt Scale: ")
        #Read Current Shunt Offset
        self.ShuntCalOffset = self.readFloat(text,"Shunt Offset: ")
        
    def printSettings(self):
        print("Mode: "+str(self.Mode))
        print("Serial ID: "+str(self.SerialID))
        print("Startup File: "+self.StartupFile)
        print("Board Current Limit: "+str(self.BoardCurrentLimit))
        print("Strand Length: "+str(self.StrandLength))
        print("Default Frame Delay: "+str(self.DefaultFrameDelay))
        print("Default Brightness: "+str(self.DefaultBrightness))
        print("Shunt Scale: "+str(self.ShuntCalScale))
        print("Shunt Offset: "+str(self.ShuntCalOffset))
        
        
if __name__ == '__main__':
    sets = BoardSettings("BoardSettings.txt")
    sets.printSettings()


