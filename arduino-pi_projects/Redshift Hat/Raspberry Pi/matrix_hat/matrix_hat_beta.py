import RPi.GPIO as GPIO

import time
import math
from datetime import datetime
import random

import threading

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from neopixel import *

import redshift_logo_scroll
import mario_image

#Constants (Sorta)
DEBUG = False
brightness = 100

#OLED Display Vars/Arrays:
modeDisplay = ["Mario Hat","Redshift Logo", "Crossfade", "Multicolor Wipe", "One Color Fill", "Multicolor Fill", "One Color Wipe", "Theater Chase", "Random LED"]
colorDisplay = ["Red", "Green", "Blue", "Orange", "Yellow", "Violet", "Magenta", "Cyan", "Rainbow/Random"]

#Colors:
RED_COLOR = Color(255, 0, 0)
GREEN_COLOR = Color(0, 255, 0)
BLUE_COLOR = Color(0, 0, 255)
ORANGE_COLOR = Color(255, 128, 0)
YELLOW_COLOR = Color(255, 255, 0)
PURPLE_COLOR = Color(128, 0, 255)
CYAN_COLOR = Color(0, 255, 255)
MAGENTA_COLOR = Color(255, 0, 255)

# Input pins:
L_pin = 27 
R_pin = 23 
C_pin = 4 
U_pin = 17 
D_pin = 22 

A_pin = 5 
B_pin = 6 


GPIO.setmode(GPIO.BCM) 

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Load default font.
font = ImageFont.load_default()




# LED strip configuration:
LED_COUNT      = 256     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = brightness   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

global mode_change
mode_change = False
mode = 0
colorVariant = 8 #Red = 0, Green = 1, Blue = 2, Orange = 3, Yellow = 4, Purple = 5, Magenta = 6, Cyan = 7, Rainbow = 8
maxMode = 8




# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    global mode_change
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        if mode_change==True:
            mode_change=False
            return 0
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    global mode_change
    for j in range(iterations):
        for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, color)
                strip.show()
                if mode_change==True:
                    mode_change=False
                    return 0
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    global mode_change
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        if mode_change==True:
            mode_change=False
            return 0
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    global mode_change
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        if mode_change==True:
            mode_change=False
            return 0
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    global mode_change
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            if mode_change==True:
                 mode_change=False
                 return 0
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def clearStrip():
    for j in range(strip.numPixels()):
        strip.setPixelColor(j, Color(0, 0, 0))



def crossFade(strip, startR, startG, startB, endR, endG, endB, steps= 200, wait=5):
    global mode_change
    for x in range(steps):
        if mode_change == True:
            mode_change = False
            return 0
        newR = startR + (endR - startR) * x/steps
        newG = startG + (endG - startG) * x/steps
        newB = startB + (endB - startB) * x/steps
        for z in range(strip.numPixels()):
            strip.setPixelColor(z, Color(newR, newG, newB))
        
        time.sleep(wait/1000.0)
        strip.show()

def randLED(strip, delay=20):
    for x in range(strip.numPixels()):
        strip.setPixelColor(x, Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    strip.show()
    time.sleep(delay/1000.0)
    
def colorFill(strip, color, delay=10):
    strip.setPixelColor(random.randint(0, strip.numPixels()-1), color)
    strip.show()
    time.sleep(delay/1000.0)

def randColorFill(strip, delay=10):
    strip.setPixelColor(random.randint(0, strip.numPixels()-1), Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    strip.show()
    time.sleep(delay/1000.0)


def oledModeUpdate():
    global mode_change
    global mode
    global colorVariant
    global brightness
    newMode = mode
    new_mode_change = mode_change 
    newColorVariant = colorVariant
    newBrightness = brightness
    
    canUpdate = False
    buttonsNeedChecked = False
    upPressed = False
    downPressed = False
    leftPressed = False
    rightPressed = False
    centerPressed = False
    aPressed = False
    bPressed = False
    quitMe=1
    stopUpdate1=False
    jumpVal = 0
    jumpBool = 0
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    #Font
    niceFont = ImageFont.truetype('/home/pi/matrix_hat/PressStart2P.ttf', 8)
    bigFont = ImageFont.truetype('/home/pi/matrix_hat/Minecraft.ttf', 16)

    # Define text and get total width.
    text = "Dr. Sawickipedia's LED Matrix Hat!"
    maxwidth, unused = draw.textsize(text, font=niceFont)

    # Set animation and sine wave parameters.
    amplitude = height/4
    offset = height/2 - 4
    velocity = -2
    startpos = width
    pos = startpos
    
    while quitMe==1:
        if stopUpdate1==True:
            quitMe=2
            thread.exit()
        else:

            
            if GPIO.input(U_pin): # button is released
                if not buttonsNeedChecked:
                    upPressed = False
            else: # button is pressed:
                upPressed = True
                buttonsNeedChecked = True

            if GPIO.input(D_pin): # button is released
                if not buttonsNeedChecked:
                    downPressed = False
            else: # button is pressed:
                downPressed = True
                buttonsNeedChecked = True

            if GPIO.input(L_pin): # button is released
                if not buttonsNeedChecked:
                    leftPressed = False
            else: # button is pressed:
                leftPressed = True
                buttonsNeedChecked = True

            if GPIO.input(R_pin): # button is released
                if not buttonsNeedChecked:
                    rightPressed = False
            else: # button is pressed:
                rightPressed = True
                buttonsNeedChecked = True

            """
            if GPIO.input(C_pin): # button is released
                if not buttonsNeedChecked:
                    centerPressed = False
            else: # button is pressed:
                centerPressed = True
                buttonsNeedChecked = True
            """
            
            if GPIO.input(A_pin): # button is released
                if not buttonsNeedChecked:
                    aPressed = False
            else: # button is pressed:
                if DEBUG:
                    aPressed = True
                    buttonsNeedChecked = True
            """
            if GPIO.input(B_pin): # button is released
                if not buttonsNeedChecked:
                    bPressed = False
            else: # button is pressed:
                bPressed = True
                buttonsNeedChecked = True
            """
            
            #Changes the mode
            if buttonsNeedChecked and GPIO.input(U_pin) and GPIO.input(D_pin) and GPIO.input(L_pin) and GPIO.input(R_pin) and GPIO.input(C_pin) and GPIO.input(A_pin):
                if rightPressed:
                    newColorVariant = 0
                    newMode += 1
                    new_mode_change = True
                elif leftPressed:
                    newColorVariant = 0
                    newMode -= 1 
                    new_mode_change = True
                    
                if upPressed:
                    newColorVariant += 1
                    new_mode_change = True
                elif downPressed:
                    newColorVariant -= 1 
                    new_mode_change = True
                    
                if newMode < 0:
                    newMode = maxMode
                elif newMode > maxMode:
                    newMode = 0

                if newColorVariant < 0:
                    newColorVariant = 8
                elif newColorVariant > 8:
                    newColorVariant = 0

                if DEBUG and aPressed:
                    newBrightness+= 40
                    if newBrightness>255:
                        newBrightness = 60
                    
                
                buttonsNeedChecked = False
                canUpdate = True


            #Updates the display
            if canUpdate and not GPIO.input(C_pin):
                mode = newMode
                colorVariant= newColorVariant
                brightness = newBrightness
                mode_change = new_mode_change
                canUpdate = False
            """
            if not GPIO.input(R_pin):
                mode +=1
                mode_change = True
            elif not GPIO.input(L_pin):
                mode -=1
                mode_change = True
            if mode<0:
                mode = maxMode
            elif mode > maxMode:
                mode = 0
            """
            
            
            #Changes OLED display
            # Draw a black filled box to clear the image.
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            if not GPIO.input(B_pin):
                DEBUG = True
            else:
                DEBUG = False
            if canUpdate or not GPIO.input(B_pin) or not GPIO.input(A_pin):    
                if DEBUG:
                    draw.text((0, 0),       "mode: " + str(mode),  font=font, fill=255)
                    draw.text((0, 8),       "color: " + str(colorVariant),  font=font, fill=255)
                    draw.text((60, 0),       "newMode: " + str(newMode),  font=font, fill=255)
                    draw.text((60, 8),       "newColor: " + str(newColorVariant),  font=font, fill=255)
                    draw.text((0, 16),       "canUpdate: " + str(canUpdate),  font=font, fill=255)
                    draw.text((0, 24),       "brightness: " + str(brightness),  font=font, fill=255)
                    draw.text((0, 32),       "newBrightness: " + str(newBrightness),  font=font, fill=255)
                else:
                    if canUpdate:
                        canUpdateTranscribe = "No"
                    else:
                        canUpdateTranscribe = "Yes"
                    draw.text((0, 0),       "Currently Displaying:",  font=font, fill=255)
                    draw.text((0, 8),       "Mode: " + modeDisplay[mode],  font=font, fill=255)
                    draw.text((0, 16),       "Color: " + colorDisplay[colorVariant],  font=font, fill=255)
                    draw.text((0, 27),       " Screen Updated?: " + canUpdateTranscribe,  font=font, fill=255)
                    draw.text((0, 39),       "To Be Updated To:",  font=font, fill=255)
                    draw.text((0, 47),       "Mode: " + modeDisplay[newMode],  font=font, fill=255)
                    draw.text((0, 55),       "Color: " + colorDisplay[newColorVariant],  font=font, fill=255)
            else:
                draw.line((0, 10, 127,10), fill=1)
                draw.line((0, 53, 127,53), fill=1)
                draw.text((128-(len(modeDisplay[mode])*6), 0),         modeDisplay[mode],  font=font, fill=255)
                draw.text((3, 55),       "Color: " + colorDisplay[colorVariant],  font=font, fill=255)

                #localTime = time.asctime(time.localtime(time.time()))
                jumpBoolAlt = 0
                if jumpBool == 0:
                    jumpBoolAlt =1
                draw.text((8, 13-jumpBoolAlt),       str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second),  font=bigFont, fill=255)
                draw.text((78, 36-jumpBool),       "4048",  font=bigFont, fill=255)
                # Enumerate characters and draw them offset vertically based on a sine wave.
                x = pos
                for i, c in enumerate(text):
                    # Stop drawing if off the right side of screen.
                    if x > width:
                        break
                    # Calculate width but skip drawing if off the left side of screen.
                    if x < -10:
                        char_width, char_height = draw.textsize(c, font=niceFont)
                        x += char_width
                        continue
                    # Calculate offset from sine wave.
                    y = offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
                    # Draw text.
                    draw.text((x, y), c, font=niceFont, fill=255)
                    # Increment x position based on chacacter width.
                    char_width, char_height = draw.textsize(c, font=niceFont)
                    x += char_width
            # Display image.
            disp.image(image)
            disp.display()
            # Move position for next frame.
            pos += velocity
            # Start over if text has scrolled completely off left side of screen.
            if pos < -maxwidth:
                pos = startpos
            if jumpVal==5:
                jumpBool = 1
            elif jumpVal == 0:
                jumpBool = 0

            if jumpBool ==1:
                jumpVal-=1
            else:
                jumpVal+=1
            time.sleep(0.001)

oled_mode_thread = threading.Thread(target=oledModeUpdate)
oled_mode_thread.daemon = True

    
# Main program logic follows:
oled_mode_thread.start()
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    singFillStep = 0
    singWipeStep = False
    wipeStep = -1
    fillStep = -1
    fadeStep = -1
    mode = 0
    print ('Press Ctrl-C to quit.')

    try:
        while 1:
            strip.setBrightness(brightness)
            if mode == 0: #Mario Hat
                mario_image.marioImage(strip, colorVariant)
            elif mode ==1: #Scrolling Redshift Logo
                redshift_logo_scroll.redshiftLogoScroll(strip)
            elif mode ==2: #RGB Crossfade
                fadeStep +=1
                if fadeStep == 0:
                    crossFade(strip, 255, 0, 0, 0, 255, 0)
                elif fadeStep == 1:    
                    crossFade(strip, 0, 255, 0, 0, 0, 255)
                elif fadeStep == 2: 
                    crossFade(strip, 0, 0, 255, 255, 0, 0)
                else:
                    fadeStep = -1
                
            elif mode ==3: #Multicolor Wipe
                wipeStep +=1
                if wipeStep == 0:
                    colorWipe(strip, Color(255, 0, 0), 10)
                elif wipeStep == 1:    
                    colorWipe(strip, Color(255, 255, 0), 10)
                elif wipeStep == 2: 
                    colorWipe(strip, Color(0, 255, 0), 10)
                elif wipeStep == 3: 
                    colorWipe(strip, Color(0, 255, 255), 10)
                elif wipeStep == 4: 
                    colorWipe(strip, Color(0, 0, 255), 10)
                elif wipeStep == 5: 
                    colorWipe(strip, Color(255, 0, 255), 10)
                else:
                    wipeStep = -1
                
            elif mode ==4: #Single/Random Color Fill
                if singFillStep > 500 and singFillStep<=1000:
                    colorFill(strip, Color(0, 0, 0))
                    singFillStep +=1
                elif singFillStep > 1000:
                    singFillStep = 0
                else:
                    if colorVariant==8:
                        randColorFill(strip)
                    elif colorVariant == 0:
                        colorFill(strip, RED_COLOR)
                    elif colorVariant == 1:
                        colorFill(strip, GREEN_COLOR)
                    elif colorVariant == 2:
                        colorFill(strip, BLUE_COLOR)
                    elif colorVariant == 3:
                        colorFill(strip, ORANGE_COLOR)
                    elif colorVariant == 4:
                        colorFill(strip, YELLOW_COLOR)
                    elif colorVariant == 5:
                        colorFill(strip, PURPLE_COLOR)
                    elif colorVariant == 6:
                        colorFill(strip, MAGENTA_COLOR)
                    elif colorVariant == 7:
                        colorFill(strip, CYAN_COLOR)
                    singFillStep+=1
                        
            elif mode ==5:#Multicolor Color Fill
                fillStep +=1
                if fillStep == 0:
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(255, 0, 0))
                elif fillStep == 1:  
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(255, 255, 0))
                elif fillStep == 2: 
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(0, 255, 0))
                elif fillStep == 3: 
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(0, 255, 255))
                elif fillStep == 4: 
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(0, 0, 255))
                elif fillStep == 5:
                    for x in range(500):
                        if mode_change:
                            mode_change = False
                            break
                        colorFill(strip, Color(255, 0, 255))
                else:
                    fillStep = -1
            elif mode ==6: #Single Color Wipe
                if singWipeStep:
                    colorWipe(strip, Color(0, 0, 0), 10)
                    singWipeStep = False
                else:
                    if colorVariant==8:
                        rainbowCycle(strip)
                    elif colorVariant == 0:
                        colorWipe(strip, RED_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 1:
                        colorWipe(strip, GREEN_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 2:
                        colorWipe(strip, BLUE_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 3:
                        colorWipe(strip, ORANGE_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 4:
                        colorWipe(strip, YELLOW_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 5:
                        colorWipe(strip, PURPLE_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 6:
                        colorWipe(strip, MAGENTA_COLOR, 10)
                        singWipeStep = True
                    elif colorVariant == 7:
                        colorWipe(strip, CYAN_COLOR, 10)
                        singWipeStep = True
            elif mode ==7: #Theater Chase
                if colorVariant==8:
                    theaterChaseRainbow(strip)
                elif colorVariant == 0:
                    theaterChase(strip, RED_COLOR)
                elif colorVariant == 1:
                    theaterChase(strip, GREEN_COLOR)
                elif colorVariant == 2:
                    theaterChase(strip, BLUE_COLOR)
                elif colorVariant == 3:
                    theaterChase(strip, ORANGE_COLOR)
                elif colorVariant == 4:
                    theaterChase(strip, YELLOW_COLOR)
                elif colorVariant == 5:
                    theaterChase(strip, PURPLE_COLOR)
                elif colorVariant == 6:
                    theaterChase(strip, MAGENTA_COLOR)
                elif colorVariant == 7:
                    theaterChase(strip, CYAN_COLOR)
            elif mode==8: #Random LED
                randLED(strip)
            


    except KeyboardInterrupt: 
        GPIO.cleanup()
        clearStrip()
        strip.show()
        stopUpdate1 =True
