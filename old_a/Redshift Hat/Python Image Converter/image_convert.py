from __future__ import print_function
from PIL import Image
import sys

def processImage(infile):
    global frameNum
    frameNum = 0;
    try:
        im = Image.open(infile)
    except IOError:
        print ("Cant load" + infile)
        sys.exit(1)
    i = 0
    mypalette = im.getpalette()

    try:
        while 1:
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            new_im.save('process\image'+str(i)+'.png')
            frameNum=frameNum+1

            i += 1
            im.seek(im.tell() + 1)

    except EOFError:
        pass # end of sequence


def matrixWireAdjust(x, y): #Change depending on how the matrix's pixels are labeled
    if x%2==0:
        return y + (x*8)
    else:
        return ((x+1)*8) - (y + 1)
    
def returnRGB(image_path, frame_delay): #Frame delay in ms
    image = Image.open(image_path)
    width, height = image.size
    image = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
    z = 0
    for x in range(width):
        for y in range(height):
            z = matrixWireAdjust(x, y)
            print("strip.setPixelColor("+ str(z) +", Color"+str(image.getpixel((x, y)))+")")
            
    print("time.sleep("+str(frame_delay/1000.0)+")")
    print("strip.show()")
    print("if mode_change == True:")
    print("    mode_change = False")
    print("    return 0")
    
    

    
    
def processGif(image_path, frame_delay):
    processImage(image_path)
    for x in range(0, frameNum):
        returnRGB('process\image'+str(x)+'.png' ,frame_delay)

processGif('image.gif', 100)
