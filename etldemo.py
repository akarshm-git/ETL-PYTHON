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

print(url)
print(startDate)
print(destServer)
print(destDatabase)