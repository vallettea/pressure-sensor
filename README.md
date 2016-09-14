## A low cost differential pressure sensor base on arduino

#### Context

This sensor was made for the pHd thesis of Alix Vallette who wanted to measure the permeability of the cochlear canaliculus. Profesionnal sensors are unaffordable (30k€) and they only display the pressure on a screen making post-analysis difficult. This sensors is a fast and dirty DIY solution for 100€. 

#### Material needed

Discalimer: here is what I used. It is not the optimum but it is what I had in my spare parts available the night I designed the sensor. 

- two pressure sensors ([HONEYWELL  ASDXRRX015PG2A5](http://fr.farnell.com/webapp/wcs/stores/servlet/ProductDisplay?catalogId=15001&langId=-2&urlRequestType=Base&partNumber=1784702&storeId=10160))
- one arduino mini pro
- one arduino pro
- an ftdi connection to communicate between the arduinos and a pc
- a breadboard or a soldering board
- wires

#### Soldering 

I used two arduinos because the pressure sensors communicate in I2C and have teh same address. So each arduino communicates with one pressure sensor via I2C and they communicate between them via SPI. (the proper solution would be to change the I2C address of one sensor and use only one arduino).

Here is the way things are wired up:

![Electronic scheme](/doc/electronics.png)

#### The code

You need to upload the code `master.c` to the big arduino (pro) using arduino software and specifying a setup of 5V/ 16Mhz. `slave.c` should go in the small arduino (pro mini) with 3.3V/ 8Mhz.

#### Measure

Once the arduinos are flashed, connect to the big arduino (pro) and on the computer launch the script `measure.py` which will start the measurements and plot in real time.

![Electronic scheme](/doc/plot_6.png)

## References

https://learn.sparkfun.com/tutorials/i2c
http://www.farnell.com/datasheets/1676926.pdf
http://sensing.honeywell.com/index.php/ci_id/45841/la_id/1/document/1/re_id/0
http://www.instructables.com/id/Raspberry-Pi-I2C-Python/?ALLSTEPS
http://gammon.com.au/i2c

http://www.gammon.com.au/forum/?id=10892
http://forum.arduino.cc/index.php?topic=154707.0
http://forum.arduino.cc/index.php?topic=122039.0
https://github.com/mchobby/I2C_Intro