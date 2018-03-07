//www.elegoo.com
//2016.12.8

// Define Pins
#define BLUE 2
#define GREEN 3
#define RED 4

void setup()
{
pinMode(RED, OUTPUT);
pinMode(GREEN, OUTPUT);
pinMode(BLUE, OUTPUT);
}


// main loop
void loop()
{
analogWrite(RED, 255);
analogWrite(GREEN, 0);
}

