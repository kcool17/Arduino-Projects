// Adafruit_NeoMatrix example for single NeoPixel Shield.
// Scrolls 'Howdy' across the matrix in a portrait (vertical) orientation.

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
 #define PSTR // Make Arduino Due happy
#endif

#define PIN 6

// MATRIX DECLARATION:
// Parameter 1 = width of NeoPixel matrix
// Parameter 2 = height of matrix
// Parameter 3 = pin number (most are valid)
// Parameter 4 = matrix layout flags, add together as needed:
//   NEO_MATRIX_TOP, NEO_MATRIX_BOTTOM, NEO_MATRIX_LEFT, NEO_MATRIX_RIGHT:
//     Position of the FIRST LED in the matrix; pick two, e.g.
//     NEO_MATRIX_TOP + NEO_MATRIX_LEFT for the top-left corner.
//   NEO_MATRIX_ROWS, NEO_MATRIX_COLUMNS: LEDs are arranged in horizontal
//     rows or in vertical columns, respectively; pick one or the other.
//   NEO_MATRIX_PROGRESSIVE, NEO_MATRIX_ZIGZAG: all rows/columns proceed
//     in the same order, or alternate lines reverse direction; pick one.
//   See example below for these values in action.
// Parameter 5 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_GRBW    Pixels are wired for GRBW bitstream (RGB+W NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)


// Example for NeoPixel Shield.  In this application we'd like to use it
// as a 5x8 tall matrix, with the USB port positioned at the top of the
// Arduino.  When held that way, the first pixel is at the top right, and
// lines are arranged in columns, progressive order.  The shield uses
// 800 KHz (v2) pixels that expect GRB color data.
Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, PIN,
NEO_MATRIX_TOP + NEO_MATRIX_LEFT +
NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
NEO_GRB + NEO_KHZ800);

const int OUTDOOR_BRIGHTNESS= 60;
const int INDOOR_BRIGHTNESS = 30;
const int LOW_BRIGHTNESS = 10;
const int VERY_LOW_BRIGHTNESS = 5;

//Change these if you want the image to scroll forward, backward, or not at all. Can also be changed in program
bool SCROLLING_IMAGE_FORWARD =  0;
bool SCROLLING_IMAGE_BACKWARD = 1;

const uint16_t colors[] = {
  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };

//8x32 Redshift Logo #1 declaration; put Python output inside array
int logoMatrix1[]={
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), 

  
};
//8x32 Test Image #1 
int testMatrix1[]={
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(254, 127, 0), matrix.Color(254, 127, 0), matrix.Color(254, 127, 0), matrix.Color(254, 127, 0), matrix.Color(254, 127, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(254, 127, 0), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(254, 254, 254), matrix.Color(0, 0, 0), matrix.Color(254, 127, 0), matrix.Color(0, 0, 0), matrix.Color(254, 254, 254), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), 
matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 127, 0), matrix.Color(254, 245, 2), matrix.Color(254, 127, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(0, 254, 254), matrix.Color(254, 245, 2), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), matrix.Color(254, 245, 2), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(254, 127, 0), matrix.Color(254, 245, 2), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 254, 254), matrix.Color(0, 254, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 245, 2), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(99, 161, 247), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(254, 254, 254), matrix.Color(254, 254, 254), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 


};





void setup() {
  Serial.begin(9600);
  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setBrightness(INDOOR_BRIGHTNESS);
  matrix.setTextColor(colors[0]);
}
int Wh=matrix.Color(255,255,255);
int Re=colors[0];
int Bl=matrix.Color(0,0,0);
int x;//    = matrix.width();
int y;
int z;
int scrollVar = 31;
int testVar1;
int newX;
int pass = 0;


void loop() {
  matrix.fillScreen(0);
  if(SCROLLING_IMAGE_BACKWARD){
    if(scrollVar<0){
      scrollVar=31;
    }
  }else if(SCROLLING_IMAGE_FORWARD){
    if(scrollVar>31){
      scrollVar=0;
    }
  }else{
    scrollVar=0;
  }
  z=0;
  for(y=0; y<=7; y++) {
    for(x=0; x<=31; x++) {
      //testVar1=((y*32)+(x-32));
      newX= x+scrollVar;
      if(newX<=31){
        matrix.drawPixel(newX,y, logoMatrix1[z]);
      }else{
        matrix.drawPixel((newX-32),y, logoMatrix1[z]);
      }
      //Serial.print(x);
      z=z+1;
    }
  }
  matrix.show();
//  matrix.setCursor(x, 0);
//  matrix.print(F("Howdy"));
//  if(--x < -36) {
//    x = matrix.width();
//    if(++pass >= 3) pass = 0;
//    matrix.setTextColor(colors[pass]);
//  }
//  matrix.show();
if(SCROLLING_IMAGE_BACKWARD){
    scrollVar=scrollVar-1;
  }else if(SCROLLING_IMAGE_FORWARD){
    scrollVar=scrollVar+1;
  }else{
    scrollVar=0;
  }
  
  delay(100);
}
