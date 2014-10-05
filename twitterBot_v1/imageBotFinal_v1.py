#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from twython import Twython
import os
import os.path
import random
import csv
import time

#add any hash tags or mentions here and include in api call
hashTag = '#SentimentsForAllOccasions'
tweetStatus = ''
mentions = ''

imageFilePath = 'SentimentsForAllOcassions_1/'
csvFilePath = 'db.csv'

FoundImage = True
imageToStoreToCsv =-1


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

# go through files in folder and return how many there are
# exclude any file beginiing with '.' - ie hidden files
def chooseRandomImage():
	path = imageFilePath
	numFiles = len([name for name in os.listdir(path) if not name.startswith('.')])
	randomCeiling = numFiles+1
	randomImage = random.randrange(1, randomCeiling,1)
	print ("random chosen image: ",randomImage)
	return	randomImage

#take random file number and check against previously choosen
#if not previously chosen right to csv file and return true, else return false
def csvReadCheck(randomValue):
	checkValue = str(randomValue)
	inputFile = open(csvFilePath, 'rt')
	global imageToStoreToCsv
	print checkValue 

	if (os.stat(csvFilePath)[6]==0):
			print "file empty"
			imageToStoreToCsv = checkValue
			return True

	if (os.stat(csvFilePath)[6]==0) == False:
		try:
				
			with inputFile as f:
				data = list(rec for rec in csv.reader(f, delimiter=','))
			if any(checkValue in sublist for sublist in data):
				print " found" 
				return False
			else:
				print "not found"
				imageToStoreToCsv = checkValue
				print ("check value: ",imageToStoreToCsv)
				return True
		finally:
			inputFile.close()      # closing
			print "closinf file"
		

def csvWrite(imageIndexToWriteToCSV):
	value = imageIndexToWriteToCSV
	
	try:
	    outputFile  = open(csvFilePath, 'a')
	    writer = csv.writer(outputFile, delimiter=',')
	    writer.writerow((value,))	
	    print ("writing ",value ," to file")
	finally:
	    outputFile.close()
	    	
def tweetImage(imageNumberToTweet):
	indexValue = imageNumberToTweet
	dirlist = os.listdir(imageFilePath)
	image = dirlist[int(indexValue)]

	print ("tweeting: ", dirlist[int(indexValue)])	

	
	photo = open(imageFilePath+image, 'rb')
	api.update_status_with_media(status=hashTag, media=photo)
	print "Image Posted"

	photo.close()

while True:
	if(csvReadCheck(chooseRandomImage())):	
		#print "write to file, post to twitter and exit"
		csvWrite(imageToStoreToCsv)
		tweetImage(imageToStoreToCsv)
		sys.exit()
		#time.sleep(120)
		

		#dirlist = os.listdir(imageFilePath)
		#print("posting image", dirlist[int(imageToStoreToCsv)])
		#sys.exit()
		
# with open('database/test.csv', 'rt') as f:
#     data = list(rec for rec in csv.reader(f, delimiter=','))
# if any('0' in sublist for sublist in data):
# 	print " found" 
# else:
# 	print "not found"


#tweet an image
#photo = open('pics/testOne.png', 'rb')
#api.update_status_with_media(status='api image test', media=photo)

#nathanogates deets
#CONSUMER_KEY = 'jhLn32ulZz1ANIk3JuOZ18LFJ'
#CONSUMER_SECRET = 'iWfJhJIE5E2oxeXI0QFSqSzlEiSKIDO2xCwIwmXoaHfvpgSjYx'
#ACCESS_KEY = '464776373-XOKN8lv23QHCFsFFVZs795N2TzVw6ePvSUDWLhVm'
#ACCESS_SECRET = 'db2GQZAayhiCSGGMBcwLOPRQDeFA9DLdkjLoqFwIv8S8G'
