#include <SPI.h>
#include<Wire.h>
#define sensor 0x28

float nbr;

void setup (void)
{
  Serial.begin (9600);
  Wire.begin();
  digitalWrite(SS, HIGH);  // ensure SS stays high for now

  // Put SCK, MOSI, SS pins into output mode
  // also put SCK, MOSI into LOW state, and SS into HIGH state.
  // Then put SPI hardware into Master mode and turn SPI on
  SPI.begin ();

  // Slow down the master a bit
  SPI.setClockDivider(SPI_CLOCK_DIV8);
  
}  // end of setup

void getdata(byte *a, byte *b)
{
  Wire.requestFrom(sensor, 2); //Sends content of first two registers
  *a = Wire.read(); //first byte recieved stored here
  *b = Wire.read(); //second byte recieved stored here
}

char * floatToString(char * outstr, double val, byte precision, byte widthp){
 char temp[16];
 byte i;

 // compute the rounding factor and fractional multiplier
 double roundingFactor = 0.5;
 unsigned long mult = 1;
 for (i = 0; i < precision; i++)
 {
   roundingFactor /= 10.0;
   mult *= 10;
 }
 
 temp[0]='\0';
 outstr[0]='\0';

 if(val < 0.0){
   strcpy(outstr,"-\0");
   val = -val;
 }

 val += roundingFactor;

 strcat(outstr, itoa(int(val),temp,10));  //prints the int part
 if( precision > 0) {
   strcat(outstr, ".\0"); // print the decimal point
   unsigned long frac;
   unsigned long mult = 1;
   byte padding = precision -1;
   while(precision--)
     mult *=10;

   if(val >= 0)
     frac = (val - int(val)) * mult;
   else
     frac = (int(val)- val ) * mult;
   unsigned long frac1 = frac;

   while(frac1 /= 10)
     padding--;

   while(padding--)
     strcat(outstr,"0\0");

   strcat(outstr,itoa(frac,temp,10));
 }

 // generate space padding
 if ((widthp != 0)&&(widthp >= strlen(outstr))){
   byte J=0;
   J = widthp - strlen(outstr);
   
   for (i=0; i< J; i++) {
     temp[i] = ' ';
   }

   temp[i++] = '\0';
   strcat(temp,outstr);
   strcpy(outstr,temp);
 }
 
 return outstr;
}

void loop (void)
{
  byte aa, bb;
  getdata(&aa, &bb);
  nbr = aa * 256 + bb;
  //Serial.println (nbr);
  char test[20];
  floatToString(test, nbr, 3, 12);
  char test2[9] = {test[4], test[5], test[6], test[7], test[8], test[9], test[10], test[11], '\n' };

  Serial.println (test2);

  
  char c;

  // enable Slave Select
  digitalWrite(SS, LOW);    // SS is pin 10

  // send test string
  for (const char * p = test2 ; c = *p; p++)
    SPI.transfer (c);

  // disable Slave Select
  digitalWrite(SS, HIGH);

  delay (1000);  // 1 seconds delay 
}  // end of loop