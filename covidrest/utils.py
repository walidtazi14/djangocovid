from pymongo import *
from datetime import datetime,timedelta
from bson.json_util import dumps
#function definition
def getConfirmedDay(date,country):
    #connect to mongo and db and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1

    #get the value of document with the specified
    number1 = confirmed.find_one({"Date" : date, "Country/Region":country},{"Value":1})
    numbr1 = number1["Value"]

    #get the value of document with day before
    date2 = datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)
    date2 = date2.strftime('%Y-%m-%d')
    number2 = confirmed.find_one({"Date": date2, "Country/Region":country }, {"Value": 1})
    numbr2 = number2["Value"]

    #get the result value
    res = numbr1-numbr2

    #print the result
    return res

def getConfirmedDayCummilated(date,country):
    #connect to mongo and db and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    
    confirmed = db.confirmed1

    #get the value of document with the specified
    number1 = confirmed.find_one({"Date" : date, "Country/Region":country},{"Value":1})
    numbr1 = number1["Value"]

    #get the result value
    res = numbr1

    #print the result
    return res

def getConfirmedDaySum(date):
    # connect to mongo and db and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1
    result = 0
    numbers = confirmed.find({"Date": date}, {"Value": 1,"Country/Region":1,"Province/State":1})
    date2 = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
    date2 = date2.strftime('%Y-%m-%d')
    for number in numbers:

        number2 = confirmed.find_one({"Date": date2, "Country/Region": number["Country/Region"],"Province/State":number["Province/State"]}, {"Value": 1})
        

        result = result + (number["Value"]-number2["Value"])

    return result

def getConfirmedDayAll(date):
    # connect to mongo and db and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1
    result =[]
    numbers = confirmed.find({"Date": date , "Province/State":"" }, {"Value": 1,"Country/Region":1,"Province/State":1})
    date2 = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
    date2 = date2.strftime('%Y-%m-%d')
    for number in numbers:
        number2 = confirmed.find_one({"Date": date2, "Country/Region": number["Country/Region"],"Province/State":number["Province/State"]}, {"Value": 1})
        
        resultmin = {"Country/Region": number["Country/Region"], "Value": number["Value"]-number2["Value"]}
        

        result.append(resultmin)
    return result
def getConfirmedDayAllCummilated(date):
    # connect to mongo and db and collection
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1
    result =[]
    numbers = confirmed.find({"Date": date , "Province/State":"" }, {"Value": 1,"Country/Region":1,"Province/State":1})
    date2 = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
    date2 = date2.strftime('%Y-%m-%d')
    for number in numbers:
        resultmin = {"Country/Region": number["Country/Region"], "Value": number["Value"]}
        

        result.append(resultmin)
    return result
def updateExistingConfirmed(date,country,province,value):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1
    if confirmed.find_one({"Date": date, "Country/Region": country,"Province/State":province}) is not None :
        date2 = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
        date2_str = date2.strftime('%Y-%m-%d')
        old_confirmed = confirmed.find_one({"Date": date, "Country/Region": country,"Province/State":province}, {"Value": 1})["Value"]
        confirmed_barh = confirmed.find_one({"Date": date2_str, "Country/Region": country,"Province/State":province}, {"Value": 1})["Value"]
        old_value_diff = old_confirmed - confirmed_barh
        date_iterator = date
        while confirmed.find_one({"Date": date_iterator, "Country/Region": country,"Province/State":province}) is not None:
            val =confirmed.find_one({"Date": date_iterator, "Country/Region": country,"Province/State":province}, {"Value": 1})["Value"]
            myquery = {"Date": date_iterator, "Country/Region": country,"Province/State":province}
            

            newvalues = {"$set": {"Value": val-old_value_diff+value}}
            confirmed.update_one(myquery, newvalues)
            val_new = confirmed.find_one({"Date": date_iterator, "Country/Region": country, "Province/State": province},
                                     {"Value": 1})["Value"]
            
            date_iterator = datetime.strptime(date_iterator, "%Y-%m-%d") + timedelta(days=1)
            date_iterator =date_iterator.strftime('%Y-%m-%d')

def DeleteExistingConfirmed(date,country,province,value):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.coviddb
    confirmed = db.confirmed1

    print("delete in progress")








#function call
