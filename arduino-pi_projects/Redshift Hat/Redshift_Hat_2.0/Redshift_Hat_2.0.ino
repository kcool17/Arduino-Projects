// Adafruit_NeoMatrix example for tiled NeoPixel matrices.  Scrolls
// 'Howdy' across three 10x8 NeoPixel grids that were created using
// NeoPixel 60 LEDs per meter flex strip.

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
#define PSTR // Make Arduino Due happy
#endif
#include "RGB.h"

#define PIN 3

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, 2, 2, PIN,
                            NEO_TILE_TOP   + NEO_TILE_LEFT   + NEO_TILE_COLUMNS   + NEO_TILE_PROGRESSIVE +
                            NEO_MATRIX_TOP + NEO_MATRIX_LEFT + NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
                            NEO_GRB + NEO_KHZ800);

/**************************************/

const uint16_t colors[] = {
  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255)
};

const RGB RGBColors[] = {
  {255, 0, 0}, {0, 255, 0}, {0, 0, 255}
};


const uint16_t redshiftLogo[] = {
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(233, 63, 63), matrix.Color(228, 45, 45), matrix.Color(255, 0, 0), matrix.Color(237, 36, 36), matrix.Color(214, 32, 32), matrix.Color(221, 34, 34), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(232, 36, 36), matrix.Color(234, 35, 35), matrix.Color(200, 27, 27), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(207, 32, 32), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(235, 71, 71), matrix.Color(228, 36, 36), matrix.Color(227, 36, 36), matrix.Color(229, 35, 35), matrix.Color(223, 34, 34), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(208, 32, 32), 
matrix.Color(255, 0, 0), matrix.Color(230, 36, 36), matrix.Color(238, 36, 36), matrix.Color(218, 29, 29), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(208, 32, 32), 
matrix.Color(255, 0, 0), matrix.Color(207, 31, 31), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(209, 32, 32), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(205, 31, 31), matrix.Color(255, 0, 0), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(253, 253, 253), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(206, 32, 32), matrix.Color(228, 35, 35), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(248, 247, 247), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(206, 32, 32), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(252, 253, 253), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(2, 2, 2), matrix.Color(8, 3, 3), matrix.Color(2, 2, 2), matrix.Color(14, 13, 13), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), 
matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(4, 4, 4), matrix.Color(255, 255, 255), matrix.Color(1, 2, 2), matrix.Color(255, 0, 0), 
matrix.Color(255, 0, 0), matrix.Color(230, 35, 35), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(8, 9, 9), matrix.Color(2, 2, 2), matrix.Color(4, 4, 4), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(4, 4, 4), matrix.Color(4, 4, 4), matrix.Color(0, 0, 0), matrix.Color(206, 32, 32), 
matrix.Color(0, 0, 0), matrix.Color(230, 52, 52), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(7, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(204, 32, 32), matrix.Color(255, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(226, 35, 35), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(4, 1, 1), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 4, 4), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 70, 70), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 71, 71), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(1, 1, 1), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 70, 70), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 72, 72), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(8, 9, 9), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(236, 73, 73), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 74, 74), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(7, 7, 7), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(243, 242, 242), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(231, 51, 51), matrix.Color(233, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(4, 4, 4), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(229, 36, 36), matrix.Color(201, 32, 32), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(3, 3, 3), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(10, 4, 4), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(225, 30, 30), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(2, 3, 3), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(9, 4, 4), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(232, 54, 54), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(229, 51, 51), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(3, 2, 2), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(230, 52, 52), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(1, 1, 1), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 2, 2), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(233, 66, 66), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(9, 9, 9), matrix.Color(0, 0, 0), matrix.Color(7, 6, 6), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(4, 4, 4), matrix.Color(2, 2, 2), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(19, 18, 18), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(3, 3, 3), matrix.Color(0, 1, 1), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(234, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(252, 251, 251), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(234, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(15, 15, 15), matrix.Color(0, 0, 0), matrix.Color(2, 1, 1), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(234, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 3, 3), matrix.Color(255, 0, 0), matrix.Color(233, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(235, 36, 36), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(3, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(253, 252, 252), matrix.Color(255, 255, 255), matrix.Color(0, 2, 2), matrix.Color(0, 0, 0), matrix.Color(235, 36, 36), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(204, 31, 31), matrix.Color(230, 35, 35), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(1, 4, 4), matrix.Color(255, 0, 0), matrix.Color(221, 34, 34), matrix.Color(227, 35, 35), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(234, 36, 36), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 3, 3), matrix.Color(255, 0, 0), matrix.Color(235, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(195, 30, 30), matrix.Color(232, 36, 36), matrix.Color(233, 67, 67), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(233, 36, 36), matrix.Color(231, 35, 35), matrix.Color(221, 34, 34), matrix.Color(209, 32, 32), matrix.Color(255, 0, 0), matrix.Color(222, 34, 34), matrix.Color(229, 36, 36), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(4, 10, 10), matrix.Color(0, 0, 0), matrix.Color(234, 36, 36), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(254, 254, 254), matrix.Color(255, 255, 255), matrix.Color(5, 6, 6), matrix.Color(0, 0, 0), matrix.Color(235, 36, 36), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 2, 2), matrix.Color(255, 0, 0), matrix.Color(230, 35, 35), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(234, 70, 70), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(229, 35, 35), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 69, 69), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(206, 32, 32), matrix.Color(221, 34, 34), matrix.Color(227, 35, 35), matrix.Color(228, 35, 35), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 70, 70), matrix.Color(255, 0, 0), matrix.Color(255, 255, 255), matrix.Color(255, 255, 255), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(236, 36, 36), matrix.Color(232, 57, 57), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 70, 70), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(230, 39, 39), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(235, 73, 73), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(238, 83, 83), matrix.Color(219, 34, 34), matrix.Color(212, 32, 32), matrix.Color(237, 36, 36), matrix.Color(230, 36, 36), matrix.Color(228, 46, 46), matrix.Color(235, 69, 69), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(234, 64, 64), matrix.Color(233, 61, 61), matrix.Color(255, 0, 0), matrix.Color(255, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), matrix.Color(0, 0, 0), 
};


/***************************************/

void crossFade(RGB startColor, RGB endColor, int steps, int wait) {
  for (int i = 0; i <= steps; i++)
  {
    int newR = startColor.r + (endColor.r - startColor.r) * i / steps;
    int newG = startColor.g + (endColor.g - startColor.g) * i / steps;
    int newB = startColor.b + (endColor.b - startColor.b) * i / steps;

    matrix.fillScreen(matrix.Color(newR, newG, newB));
    matrix.show();
    delay(wait);
  }
}

void snekColor(uint16_t color){
  for (int x = 0; x < 64; x++) {
    for (int y = 0; y < 16; y++) {
      if (x % 2 == 0){
        matrix.drawPixel(x, y, color);
      }else{
        matrix.drawPixel(x, 15-y, color);
      }
        matrix.show();
        delay(1); 
    }
  }
}


/****************************/

void mainCrossFade(){
  crossFade(RGBColors[0], RGBColors[1], 20, 10);
  crossFade(RGBColors[1], RGBColors[2], 20, 10);
  crossFade(RGBColors[2], RGBColors[0], 20, 10);
}

int scrollVar = 0;
void scrollLogo(){
  if(scrollVar < 0){
    scrollVar = 63;
  } else {
    scrollVar -= 1;
  }
  int z = 0;
  int newX = 0;
  for (int x = 0; x < 64; x++) {
      for (int y = 0; y < 16; y++) {
        newX= x+scrollVar;
        if(newX<=63){
          matrix.drawPixel(newX,y, redshiftLogo[z]);
        }else{
          matrix.drawPixel((newX-64),y, redshiftLogo[z]);
        }
        z++;
    }
  }
  matrix.show();
  delay(100);
}

void mainSnek(){
  snekColor(matrix.Color(255, 0, 0));
  snekColor(matrix.Color(255, 255, 0));
  snekColor(matrix.Color(0, 0, 0));
  snekColor(matrix.Color(0, 255, 0));
  snekColor(matrix.Color(0, 255, 255));
  snekColor(matrix.Color(0, 0, 0));
  snekColor(matrix.Color(0, 0, 255));
  snekColor(matrix.Color(255, 0, 255));
  snekColor(matrix.Color(0, 0, 0));
}
/*****************************/

void setup() {
  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setBrightness(40);
  matrix.setTextColor(colors[0]);
}

int x    = matrix.width();
int pass = 0;

void loop() {
  for(int x = 0; x < 32*16; x++){
    scrollLogo();
  }
  /*
  snekColor(matrix.Color(255, 0, 0));
  for(int x = 0; x < 128; x++){
    mainCrossFade();
  }
  snekColor(matrix.Color(0, 0, 0));
  mainSnek();
  */
}
