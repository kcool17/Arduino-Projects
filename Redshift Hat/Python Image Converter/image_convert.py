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


def returnRGB(image_path):
    image = Image.open(image_path)
    width, height = image.size
    image = Image.composite(image, Image.new('RGB', image.size, 'white'), image)
    for x in range(width):
        for y in range(height):
            print(str(image.getpixel((x, y))), end=', ')

    print("\n\n\n")
    
    
    
    
    
def processGif(image_path):
    processImage(image_path)
    for x in range(0, frameNum):
        returnRGB('process\image'+str(x)+'.png')

processGif('image.gif')

