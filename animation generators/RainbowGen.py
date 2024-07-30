import colorsys

defFrameDelay = 10

f = open("rainbow.anim","w")

mainChevOffset = 36
outerChevOffset = mainChevOffset+36
innerChevOffset = outerChevOffset+36
wormholeOffset = innerChevOffset+36

def formatColor(color):
    return str("C"+f"{color:#0{8}x}\n"[2:])
        
def rgb_int2tuple(rgbint):
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

def rgb_tuple2int(tup=(0, 0, 0)):
    return tup[2] + (tup[1] << 8) + (tup[0] << 16)
    
def colorHSV(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    
def colorRGB(red, green, blue):
    return colorsys.rgb_to_hsv(red,green,blue)
    
def scaleHue(val):
    return (abs(val)%36)/36.0
    
def formatHsv(h,s,v):
    return formatColor(rgb_tuple2int(colorHSV(h,s,v)))
    
def writeHeader():
    f.write("CLR\n")
    f.write("DEFDLY T"+str(defFrameDelay)+"\n")
    f.write("BRT B0.6\n")
    
def rainbowFrame(offset):
    f.write("SET I0 "+formatHsv(scaleHue(offset),1.0,1.0))
    for i in range(0,36):
        f.write(formatHsv(scaleHue(offset+i),1.0,1.0))
        
    
if __name__ == '__main__':
    writeHeader()
    rainbowFrame(0)
    f.close()
    
    