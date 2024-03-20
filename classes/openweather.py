import time
# print('openweather:', __name__)
if __name__ == "classes.openweather": from . import config
else: import config
if __name__ == "classes.openweather": from . import meteodataset
else: from meteodataset import MeteoDataSet
if __name__ == "classes.openweather": from . import meteoicon
else: from meteoicon import MeteoIcon
import requests

class OpenWeather:
    ZERO_TEMP = -273.15
    METEO_ICON = meteoicon.MeteoIcon()

    def __init__(self, cityName):
        self.cityName = cityName
        # api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cityName + '&appid=' + config.owApiKey
        self.meteoUrl = 'http://api.openweathermap.org/data/2.5/forecast?q=' + cityName + '&appid=' + config.owApiKey
        # Wattignies = id=6454427

    # Return the temp for cityName
    # in case of error return ZERO_TEMP = -237.15
    def getTemp(self):
        r = requests.get(self.url)
        if r.status_code != 200: return self.ZERO_TEMP
        response = r.json()
        if 'main' in response:
            if 'temp' in response['main']: return self.ZERO_TEMP + float(response['main']['temp'])

        return self.ZERO_TEMP

    def getMeteo(self):
        r = requests.get(self.meteoUrl)
        if r.status_code != 200: return self.ZERO_TEMP
        response = r.json()
        if __name__ == "classes.openweather": meteo = meteodataset.MeteoDataSet()
        else: meteo = MeteoDataSet()
        previousDate = '1900-01-01'
        dayCounter = 0
        recordCount = 0
        minTemp = 100
        maxTemp = -20
        if 'city' in response:
            if 'name' in response['city']:
                meteo.cityName = response['city']['name']
        if 'list' in response:
            for data in response['list']:
                # print(data)
                convertedDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['dt']))
                weekDay = time.strftime('%a', time.localtime(data['dt']))
                # print(convertedDate, weekDay)
                if previousDate != convertedDate[0:10]: # We moved to a new day
                    # print(weekDay)
                    meteo.weekDay += [weekDay]
                    meteo.dayStart += [recordCount]
                    if weekDay == 'Sat': meteo.weekEnd += [recordCount]
                    if weekDay == 'Mon': meteo.weekEnd += [recordCount]
                    previousDate = convertedDate[0:10]
                    dayCounter += 1;
                meteo.dayTime += [convertedDate[11:16]]
                # Temperature
                if 'main' in data:
                    if 'temp' in data['main']:
                        temp = round(self.ZERO_TEMP + float(data['main']['temp']), 1)
                        meteo.temp += [temp]
                        if temp < minTemp: minTemp = temp
                        if temp > maxTemp: maxTemp = temp
                    if 'pressure' in data['main']:
                        meteo.pressure += [data['main']['pressure']]
                # Rain
                if 'rain' in data:
                    if '3h' in data['rain']:
                        meteo.rain += [data['rain']['3h']]
                else: meteo.rain += [0]
                # Wind speed
                if 'wind' in data:
                    if 'speed' in data['wind']:
                        meteo.wind += [data['wind']['speed']*3.6]
                    if 'deg' in data['wind']:
                        windDirection = int((float(data['wind']['deg'])+22.5)/45 % 8)
                        meteo.windDirection += [{'y': 0, 'windDirection': str(data['wind']['deg'])+'°' , 'marker': {'symbol': 'url(/static/images/Wind' + str(windDirection) + '.png)'} }]

                # Weather icon
                if convertedDate[11:13] in ['07', '08', '09'] or convertedDate[11:13] in ['14', '15', '16']:
                    if 'weather' in data:
                        if 'id' in data['weather'][0]:
                            meteo.weatherIcon += [{'y': 0, 'weather': str(data['weather'][0]['main']) , 'marker': {'enabled': 1, 'symbol': 'url(/static/images/' + self.METEO_ICON.getIcon(data['weather'][0]['id']) +')'} }]
                else: meteo.weatherIcon += [{'y': 0, 'weather': str(data['weather'][0]['main'])}]

                recordCount += 1

            # Register last day to show a separation (plotLines)
            # print('dayCounter=', dayCounter)
            while dayCounter < 7:
                meteo.dayStart += [39]
                dayCounter += 1
            # End weekend if no end
            if len(meteo.weekEnd) == 1: meteo.weekEnd += [39]
            # Adjust the y position for wind direction
            for windDirection in meteo.windDirection:
                windDirection['y'] = minTemp - 2
            # Adjust y position for weather icon
            for weatherIcon in meteo.weatherIcon:
                weatherIcon['y'] = maxTemp + 1
            return meteo


# ow = OpenWeather("Firbeix")
# ow = OpenWeather("Wattignies")
# if ow.getTemp() == ow.ZERO_TEMP: print("error")
# else: print(ow.getTemp())
# if ow.getMeteo() == ow.ZERO_TEMP: print('error')
# else: print('Completed')