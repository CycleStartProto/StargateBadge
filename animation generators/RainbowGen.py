import colorsys

defFrameDelay = 2

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
    
def scaleMainHue(val):
    return abs((val%36)/36.0)
    
def scaleChevHue(val):
    return abs((val%18)/18.0)
    
def formatHsv(h,s,v):
    return formatColor(rgb_tuple2int(colorHSV(h,s,v)))
    
def writeHeader():
    f.write("DEFDLY T"+str(defFrameDelay)+"\n")
    f.write("BRT B0.5\n")
    
def rainbowFrame(offset):
    f.write("SET I0 "+formatHsv(scaleMainHue(offset),1.0,0.1))
    for i in range(1,36):
        f.write(formatHsv(scaleMainHue(offset-i),1.0,0.1))
    f.write("SET I"+str(mainChevOffset)+" "+formatHsv(scaleChevHue(offset),1.0,1.0))
    for i in range(1,18):
        f.write(formatHsv(scaleChevHue(offset+i),1.0,1.0))
    f.write("SET I"+str(outerChevOffset)+" "+formatHsv(scaleChevHue(offset),1.0,1.0))
    for i in range(1,18):
        f.write(formatHsv(scaleChevHue(offset+i),1.0,1.0))
    f.write("SET I"+str(innerChevOffset)+" "+formatHsv(scaleChevHue(offset),1.0,1.0))
    for i in range(1,18):
        f.write(formatHsv(scaleChevHue(offset+i),1.0,1.0))
    f.write("SET I"+str(wormholeOffset)+" "+formatHsv(scaleMainHue(offset),1.0,0.1))
    for i in range(1,36):
        f.write(formatHsv(scaleMainHue(offset+i),1.0,0.1))
        
    
if __name__ == '__main__':
    writeHeader()
    for i in range(0,36):
        rainbowFrame(i)
        f.write("SHOW\n")
    f.close()
    
    