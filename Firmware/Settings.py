import microcontroller as mc
import struct

class settings:

    scrollMode = 0 #0 = static, 1 = continuous, 2 = delay between, 3 = random delay between
    scrollXAmnt = 0 #number of pixels to scroll in x per scan
    scrollYAmnt = 0 #number of pixels to scroll in y per scan
    scrollDelay = 0 #delay (ms) between scroll scans (between frames)
    
    animLength = 0 #number of frames in the animation
    animInterval = 500 #time to wait on last frame before restarting animation (ms)
    animRandLower = 100 #lower limit for random interval (ms)
    animRandUpper = 5000 #upper limit for random interval (ms)
    
    brightness = 1.0 #global brightness (0.0 to 1.0)
    
    def readint(self, text, name):
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
        
    def readfloat(self, text, name):
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
        
        #Read Brightness
        self.brightness = self.readfloat(text, "Brightness: ")
        
        #Read Scroll Mode
        self.scrollMode = self.readint(text, "Scroll Mode: ")
        
        if self.scrollMode != 0:        
            #Read X Scroll Amount
            self.scrollXAmnt = self.readint(text, "Scroll X Per Frame: ")
            
            #Read Y Scroll Amount
            self.scrollYAmnt = self.readint(text, "Scroll Y Per Frame: ")
            
            #Read Scroll Frame Delay
            self.scrollDelay = self.readfloat(text, "Scroll Frame Delay: ")
        
            #Read Animation Length
            self.animLength = self.readint(text, "Animation Length: ")
            
            if self.scrollMode == 2:
                #Read Animation Interval
                self.animInterval = self.readfloat(text, "Animation Interval: ")
            
            if self.scrollMode == 3:
                #Read Animation Random Interval Lower
                self.animRandLower = self.readfloat(text,"Animation Random Interval Lower: ")
                
                #Read Animation Random Interval Upper
                self.animRandUpper = self.readfloat(text,"Animation Random Interval Upper: ")


