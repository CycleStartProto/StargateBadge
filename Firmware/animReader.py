from CommandParser import CommandParser

class animReader():
    CP = None
    file = None
    def __init__(self,comparser):
        self.CP = comparser
        
    def openFile(self,name):
        self.file = open(name,'rt')    
        
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
            return None
            
    def playAnim(self,name):
        self.openFile(name)
        while self.parseLine():
            pass
        