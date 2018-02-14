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
    for y in range(height):
        for x in range(width):
            z = x + y
            print("matrix.drawPixel("+ str(x) + ", " + str(y) +", matrix.Color"+str(image.getpixel((x, y)))+");")
            
    print("delay("+str(frame_delay)+");")
    print("matrix.show();")
    
    

    
    
def processGif(image_path, frame_delay):
    processImage(image_path)
    for x in range(0, frameNum):
        returnRGB('process\image'+str(x)+'.png' ,frame_delay)

processGif('image.gif', 100)

