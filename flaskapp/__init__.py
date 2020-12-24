from flask import Flask
tempCollectApp = Flask(__name__)

from classes.openweather import OpenWeather
from classes.datacollect import DataCollect

firbeix = OpenWeather("Firbeix")
wattignies = OpenWeather("Wattignies")
dataCollect = DataCollect() 

from flaskapp import routes
