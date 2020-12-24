print(__name__)
import threading
import time
from datetime import datetime # Tmp for printing time
if __name__ == "classes.datacollect":
    from . import openweather
    from . import mongodb
else:
    from openweather import OpenWeather
    from mongodb import MongoDb

class DataCollect():
    def __init__(self):
        self.mongo = mongodb.MongoDb()
        self.firbeix = openweather.OpenWeather("Firbeix")
        self.wattignies = openweather.OpenWeather("Wattignies")
        self.collectData()

    def collectData(self):
        if datetime.today().second == 0:
            currentTime = datetime(datetime.today().year, datetime.today().month, datetime.today().day, datetime.today().hour, datetime.today().minute, datetime.today().second)
            self.mongo.add({'date': currentTime, 'city': 'Firbeix', 'temp': round(self.firbeix.getTemp(), 1)})
            self.mongo.add({'date': currentTime, 'city': 'Wattignies', 'temp': round(self.wattignies.getTemp(), 1)})
        sleepSeconds = 3600 - int(time.time() % 3600) #Replace 60 by 3600 to run every hour
        t = threading.Timer(sleepSeconds, self.collectData)
        t.start()
        
    # def printIt():
    #     threading.Timer(5.0, printIt()).start()
    #     print ("Hello, World!")


# dataCollect = DataCollect() 
