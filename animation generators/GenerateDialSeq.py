import colorsys
glyphColor = (20,20,20)
chevronColor = (0,57,255)
wormholeColor = (100,180,255)

wormholeIdleBrightness = 0.1
mainBrightness = 0.5

outgoingDialFrameDelay = 60
incomingDialFrameDelay = 100

mainChevOffset = 36
outerChevOffset = mainChevOffset+36
innerChevOffset = outerChevOffset+36
wormholeOffset = innerChevOffset+36



f = open("outgoing.anim","w")

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
    
glyphColor = rgb_tuple2int(glyphColor)
chevronColor = rgb_tuple2int(chevronColor)
wormholeColor = colorsys.rgb_to_hsv(wormholeColor[0]/255.0,wormholeColor[1]/255.0,wormholeColor[2]/255.0)

keeponArray = []

def writeHeader(delay):
    f.write("CLR\n")
    f.write("DEFDLY T"+str(delay)+"\n")
    f.write("BRT B"+str(mainBrightness)+"\n")
    
    
def dialLeft(start,end):
    start = start%36
    end = end%36
    f.write("SET I"+str(start)+" "+formatColor(glyphColor))
    f.write("DLY\n")
    if start not in keeponArray:
        f.write("CLR I"+str(start)+"\n")
    i = start-1
    j = 0
    while True:
        if i <= -1:
            i = 35
        f.write("SET I"+str(i%36)+"\n")
        f.write("DLY\n")
        if i%36 not in keeponArray:
            f.write("CLR I"+str(i%36)+"\n")
        i-=1
        j+=1
        if i == end:
            if j >= 18:
                break
    f.write("SET I"+str(end%36)+"\n")
    f.write("DLY\n")
    keeponArray.append(end%36)
    
def dialRight(start,end):
    start = start%36
    end = end%36
    if abs(end-start) < 18:
        end = end+36
    f.write("SET I"+str(start)+" "+formatColor(glyphColor))
    f.write("DLY\n")
    if start not in keeponArray:
        f.write("CLR I"+str(start)+"\n")
    for i in range(start+1,end):
        f.write("SET I"+str(i%36)+"\n")
        f.write("DLY\n")
        if i%36 not in keeponArray:
            f.write("CLR I"+str(i%36)+"\n")
    f.write("SET I"+str(end%36)+"\n")
    f.write("DLY\n")
    keeponArray.append(end%36)
    
def encodeChevron(num):
    f.write("SET I"+str(outerChevOffset+num*2)+":"+str(outerChevOffset+num*2+2)+" "+formatColor(chevronColor))
    f.write("SET I"+str(innerChevOffset+num*2)+":"+str(innerChevOffset+num*2+2)+" "+formatColor(chevronColor))
    f.write("DLY T300\n")
    f.write("SET I"+str(mainChevOffset+num*2)+":"+str(mainChevOffset+num*2+2)+" "+formatColor(chevronColor))
    f.write("DLY T500\n")
    
def incomeChevron(num):
    f.write("SET I"+str(outerChevOffset+num*2)+":"+str(outerChevOffset+num*2+2)+" "+formatColor(chevronColor))
    f.write("SET I"+str(innerChevOffset+num*2)+":"+str(innerChevOffset+num*2+2)+" "+formatColor(chevronColor))
    f.write("SET I"+str(mainChevOffset+num*2)+":"+str(mainChevOffset+num*2+2)+" "+formatColor(chevronColor))
    
def lockChevrons():
    f.write("SET I"+str(outerChevOffset)+":"+str(outerChevOffset+18)+" "+formatColor(chevronColor))
    f.write("SET I"+str(innerChevOffset)+":"+str(innerChevOffset+18)+" "+formatColor(chevronColor))
    f.write("SET I"+str(mainChevOffset)+":"+str(mainChevOffset+18)+" "+formatColor(chevronColor))
    f.write("CLR I0:36\n")
    f.write("DLY\n")
    
def wormhole():
    colorh = wormholeColor
    color = rgb_tuple2int(colorHSV(wormholeColor[0],wormholeColor[1],wormholeColor[2]))
    f.write("DEFDLY T7\n")
    f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
    f.write("DLY\n")
    while colorh[2] > 0.02:
        colorh = (colorh[0],colorh[1],colorh[2]-0.01)
        color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
        f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
        f.write("DLY\n")
    while colorh[2] < wormholeIdleBrightness:
        colorh = (colorh[0],colorh[1],colorh[2]+0.002)
        color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
        f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
        f.write("DLY\n")
        
def shutdown():
    colorh = (wormholeColor[0],wormholeColor[1],wormholeIdleBrightness)
    color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
    f.write("DEFDLY T7\n")
    f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
    f.write("DLY\n")
    while colorh[2] < 1.0:
        color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
        colorh = (colorh[0],colorh[1],colorh[2]+0.02)
        f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
        f.write("DLY\n")
    f.write("CLR I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+"\n")
    f.write("DLY T1000\n")
    f.write("CLR\n")
    f.write("SHOW\n")
    
def idle():
    colorh = (wormholeColor[0],wormholeColor[1],wormholeIdleBrightness)
    color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
    f.write("DEFDLY T50\n")
    f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
    f.write("DLY\n")
    while colorh[2] > 0.01:
        color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
        colorh = (colorh[0],colorh[1],colorh[2]-0.002)
        f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
        f.write("DLY\n")
    while colorh[2] < wormholeIdleBrightness:
        color = rgb_tuple2int(colorHSV(colorh[0],colorh[1],colorh[2]))
        colorh = (colorh[0],colorh[1],colorh[2]+0.002)
        f.write("SET I"+str(wormholeOffset)+":"+str(wormholeOffset+36)+" "+formatColor(color))
        f.write("DLY\n")
    
def incoming():
    for i in range(1,36):
        f.write("SET I"+str(i)+" "+formatColor(glyphColor))
        if i%4 == 0:
            incomeChevron(int(i/4))
        f.write("DLY\n")
    f.write("SET I0 "+formatColor(glyphColor))
    incomeChevron(0)
    f.write("DLY\n")
    
    
if __name__ == '__main__':
    writeHeader(outgoingDialFrameDelay)
    dialLeft(0,4)
    encodeChevron(1)
    dialRight(4,8)
    encodeChevron(2)
    dialLeft(8,12)
    encodeChevron(3)
    dialRight(12,24)
    encodeChevron(6)
    dialLeft(24,28)
    encodeChevron(7)
    dialRight(28,32)
    encodeChevron(8)
    dialLeft(32,36)
    encodeChevron(0)
    lockChevrons()
    wormhole()
    f.close()
    f = open("incoming.anim","w")
    writeHeader(incomingDialFrameDelay)
    incoming()
    wormhole()
    f.close()
    f = open("close.anim","w")
    shutdown()
    f.close()
    f = open("idle.anim","w")
    idle()
    f.close()
    