from flask import Flask
tempCollectApp = Flask(__name__)

from classes.openweather import OpenWeather
firbeix = OpenWeather("Firbeix")
wattignies = OpenWeather("Wattignies")

from flaskapp import routes
