import sys
import smbus
import RPi.GPIO as GPIO
import time
bus = smbus.SMBus(1)    #make sure you are on the right bus with i2cdetect -y 0 or i2cdetect -y 1. it will return the device addres
GPIO.setmode(GPIO.BCM)

#cap1188 reset pin
resetPin = 24
GPIO.setup(resetPin, GPIO.OUT)

CAP1188_SENINPUTSTATUS= 0x3
CAP1188_MTBLK= 0x2A
CAP1188_LEDLINK= 0x72
CAP1188_PRODID= 0xFD
CAP1188_MANUID= 0xFE
CAP1188_STANDBYCFG= 0x41
CAP1188_REV= 0xFF
CAP1188_MAIN= 0x00
CAP1188_MAIN_INT =0x01
CCAP1188_LEDPOL= 0x73

CAP1188_I2CADDR =0x29


def begin():

        #reset board
        GPIO.output(resetPin, False);
        time.sleep(0.10);
        GPIO.output(resetPin, True);
        time.sleep(0.10);
        GPIO.output(resetPin, False);
        time.sleep(0.10);
 
        #check device id
        if (bus.read_byte_data(CAP1188_I2CADDR, CAP1188_PRODID) != 0x50) or (bus.read_byte_data(CAP1188_I2CADDR, CAP1188_MANUID)!=0x5d)or (bus.read_byte_data(CAP1188_I2CADDR, CAP1188_REV)!=0x83):
                return False

        #if correct setup device: multiple touch, led correspond to touches, speed up something or other (check datasheet) 
        print "device is correct"
        bus.write_byte_data(CAP1188_I2CADDR,CAP1188_MTBLK, 0);
        bus.write_byte_data(CAP1188_I2CADDR,CAP1188_LEDLINK, 0xFF);
        bus.write_byte_data(CAP1188_I2CADDR,CAP1188_STANDBYCFG, 0x30);


def touched():

        #read sensor input status
        t = bus.read_byte_data(CAP1188_I2CADDR, CAP1188_SENINPUTSTATUS);

        #if touch has been triggered. clear INT bit in main register to clear reading
        #if you do not this the trigger will stay high until powered off.
        if t > 0 :
                newMain = bus.write_byte_data(CAP1188_I2CADDR,CAP1188_MAIN, (bus.read_byte_data(CAP1188_I2CADDR,CAP1188_MAIN) & ~CAP1188_MAIN_INT) );
        return t;

#changes how leds are driven, i think. changes whether they are triggered high or low
def ledPolarity(x):
        bus.write_byte_data(CAP1188_I2CADDR,CCAP1188_LEDPOL, x);


#example use
'''

begin();

while 1:

        touch = touched();                              #setup sensor

        if touch > 0:                                   #if touched then unpack sensor input status byte (CAP1188_SENINPUTSTATUS) 
                for i in range (8):
                        if (touch & (1<<i)) :           #and check individual readings
                                print ("c",(i+1)),

                print

'''