from CommandParser import CommandParser

class animReader():
    CP = None
    sets = None
    file = None
    fileName = None
    animFinished = True

    def __init__(self,leds,sets):
        self.CP = CommandParser(leds,sets)
        self.sets = sets
        
    def deinit(self):
        if self.file != None:
            self.file.close()
        self.file = None
        self.fileName = None
        self.animFinished = True

    def openFile(self,name):
        self.file = open(name,'rt')
        self.fileName = name

    def readAndFormat(self):
        line = self.file.readline()
        if line == None or line == "" or line == '':
            return None
        else:
            return line[0:len(line)-2]

    def parseLine(self):
        line = self.readAndFormat()
        if line != None:
            self.CP.parse(line)
            return True
        else:
            self.deinit()
            return False

    def setAnim(self,name):
        self.animFinished = False
        self.openFile(name)
        
    def cyclicCall(self):
        if self.sets.haltRequested == True:
            self.deinit()
            self.sets.haltRequested = False
        if self.sets.loadRequested == True:
            file = self.sets.loadReqFile
            if file != "":
                self.deinit()
                self.setAnim(self.sets.loadReqFile)
            else:
                raise Exception("no file provided")
            self.sets.loadRequested = False
        if self.CP.isReady() and self.file != None and not self.animFinished:
            self.animFinished = not self.parseLine()
            return 1
        else:
            return None

