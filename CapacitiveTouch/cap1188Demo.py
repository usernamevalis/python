#!/usr/bin/env python

""" audio trigger test using cap1188 lib i wrote"""

"""pygame doesn't like mp3's stick to wav and ogg"""


import pygame.mixer
import cap1188 as cap

# User pygame for sounds

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

one = pygame.mixer.Sound("sample/one.wav")
one.set_volume(.65);
two = pygame.mixer.Sound("sample/two.wav")
two.set_volume(.65);
three = pygame.mixer.Sound("sample/three.wav")
three.set_volume(.65);
four = pygame.mixer.Sound("sample/four.wav")
four.set_volume(.65);
five = pygame.mixer.Sound("sample/five.wav")
five.set_volume(.65);
six = pygame.mixer.Sound("sample/six.wav")
six.set_volume(.65);
seven = pygame.mixer.Sound("sample/seven.wav")
seven.set_volume(.65);
eight = pygame.mixer.Sound("sample/WilhelmScream.wav")
eight.set_volume(.65);

# setup cap1188
cap.begin();

touchedPins = [0,0,0,0,0,0,0,0];

while True:

        touchedData = cap.touched();                   #unpack sensor input status byte (CAP1188_SENINPUT$
                      
        for i in range (8):
            if (touchedData & (1<<i)) :               #and check individual readings
                #print ("c",(i+1)),                   #debug, prints sensors to cmd line            
        # print                                       #new line for debug statements                                   
                if (touchedPins[i] == 0):

                    print( 'Pin ' + str(i) + ' was just touched')

                    if (i == 0):
                        one.play() 
                    elif (i == 1):
                        two.play()
                    elif (i == 2):
                        three.play()
                    elif (i == 3):
                        four.play()
                    elif (i == 4):
                        five.play()
                    elif (i == 5):
                        six.play()
                    elif (i == 6):
                        seven.play()
                    elif (i == 7):
                        eight.play()

                touchedPins[i] = 1;
            else:
                if (touchedPins[i] == 1):
                     print( 'Pin ' + str(i) + ' was just released')
                touchedPins[i] = 0;
GPIO.cleanup();
