#include <SPI.h>
#include<Wire.h>
#define sensor 0x28

float nbr;

char buf [100];
volatile byte pos;
volatile boolean process_it;

void setup (void)
{
  Serial.begin (9600);   // debugging
  Wire.begin();
  // turn on SPI in slave mode
  SPCR |= bit (SPE);

  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);
  
  // get ready for an interrupt 
  pos = 0;   // buffer empty
  process_it = false;

  // now turn on interrupts
  SPI.attachInterrupt();

}  // end of setup

void getdata(byte *a, byte *b)
{
  Wire.requestFrom(sensor, 2); //Sends content of first two registers
  *a = Wire.read(); //first byte recieved stored here
  *b = Wire.read(); //second byte recieved stored here
}

// SPI interrupt routine
ISR (SPI_STC_vect)
{
byte c = SPDR;  // grab byte from SPI Data Register
  
  // add to buffer if room
  if (pos < sizeof buf)
    {
    buf [pos++] = c;
    
    // example: newline means time to process buffer
    if (c == '\n')
      process_it = true;
      
    }  // end of room available
}  // end of interrupt routine SPI_STC_vect

// main loop - wait for flag set in interrupt routine
void loop (void)
{

  if (process_it)
    {
    byte aa, bb;
    getdata(&aa, &bb);
    nbr = aa * 256 + bb;
  
 
    buf [pos] = 0;
    Serial.print("_");
    Serial.print(nbr);
    Serial.print("--");
    Serial.print(buf);
    pos = 0;
    process_it = false;
    }  // end of flag set
    
}  // end of loop