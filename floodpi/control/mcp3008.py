# https://github.com/jerbly/tutorials/blob/master/moisture/mcp3008.py
# https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

import RPi.GPIO as GPIO
import spidev

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 25

class ADC():
    def __init__(self):
        self.spi = spidev.SpiDev()

    def open(self):
        self.spi.open(0,1)

    def close(self):
        self.spi.close()

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        r = self.spi.xfer2([1,(8+adcnum)<<4,0])
        adcout = ((r[1]&3) << 8) + r[2]
        return adcout

    def read_pct(self, adcnum):
        r = self.readadc(adcnum)
        return int(round((r/1023.0)*100))

    def read_3v3(self, adcnum):
        r = self.readadc(adcnum)
        v = (r/1023.0)*3.3
        return v

    def readadc_avg(self, adcnum):
        r = []
        for i in range (0,10):
            r.append(self.readadc(adcnum))
        return sum(r)/10.0

class ADC2():
    def __init__(self):
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)

    def open(self):
        pass

    def close(self):
        pass

    def readadc(self, adcnum):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(SPICS, True)
 
        GPIO.output(SPICLK, False)  # start clock low
        GPIO.output(SPICS, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(SPIMOSI, True)
            else:
                GPIO.output(SPIMOSI, False)
            commandout <<= 1
            GPIO.output(SPICLK, True)
            GPIO.output(SPICLK, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(SPICLK, True)
            GPIO.output(SPICLK, False)
            adcout <<= 1
            if (GPIO.input(SPIMISO)):
                adcout |= 0x1
 
        GPIO.output(SPICS, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout