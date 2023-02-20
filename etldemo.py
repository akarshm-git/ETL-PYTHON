import os #os module for tools to interact with OS and file system
import configparser 
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