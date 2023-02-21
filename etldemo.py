import configparser
import datetime
import decimal
import json
import os  # os module for tools to interact with OS and file system
import sys
import openpyxl
import petl
import pymssql
import requests

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

    #create petl table  from column  arrays  and  rename columns
    exchangeRates = petl.fromcolumns([BOCDates,BOCRates],header = ['date','rate'])

    try:
        expenses = petl.io.xlsx.fromxlsx('Expenses.xlsx',sheet='Github')
    except Exception as e:
        print("could  not open  expenses.xlsx: "+str(e))
        sys.exit()
#Crucial steps in transforming the data we require intracking exchange rates.
    #join tables
    expenses = petl.outerjoin(exchangeRates,expenses,key="date")
    
    #fill down missing values
    expenses = petl.filldown(expenses,'rate')

    #remove dates with no expenses
    expenses = petl.select(expenses,lambda rec: rec.USD != None)

#Add canadian daat column, populate database as 4 columns exchange rate, USD, CAD
    
    #add CAD column
    expenses = petl.addfield(expenses,'CAD', lambda rec: decimal.Decimal(rec.USD) * rec.rate)

    