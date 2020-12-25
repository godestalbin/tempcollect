import platform
from flask import Flask
tempCollectApp = Flask(__name__)

from classes.openweather import OpenWeather
from classes.datacollect import DataCollect
from classes.mongodb import MongoDb

firbeix = OpenWeather("Firbeix")
wattignies = OpenWeather("Wattignies")
mongo = MongoDb()

if platform.system() == 'Linux': dataCollect = DataCollect()

from flaskapp import routes
