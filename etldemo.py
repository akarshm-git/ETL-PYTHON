import os #os module for tools to interact with OS and file system
import configparser
import sys 
import petl
import requests
import datetime
import json
import decimal
import pymssql

#get data from configuration file
config = configparser.ConfigParser()
try:
    config.read('ETLDemo.ini')
except Exception as e:
    print("Could not read config file:" +str(e))
    sys.exit()

#read settings from configuration file
startDate = config['CONFIG']['startDate']
url = config['CONFIG']['url']
destServer = config['CONFIG']['server']
destDatabase = config['CONFIG']['database']

#request data from URL
try:
    BOCResponse = requests.get(url+startDate)
except Exception as e:
    print("could not make request:"+str(e))
    sys.exit()

BOCDates = []
BOCRates = []

#check response status and if valid turn raw text to json from response
if BOCResponse.status_code == 200:
    BOCRaw = json.loads(BOCResponse.text)

    #extract observation data into column arrays
    for row in BOCRaw['observations']:
        # later going to compare data from the dates column in BOS source data with another data source.(they have  to be in same data type for that)
        BOCDates.append(datetime.datetime.strptime(row['d'],'%Y-%m-%d'))
        BOCRates.append(decimal.Decimal(row['FXUSDCAD']['v']))

print(BOCRates)












