# from . import config
# print('openweather:', __name__)
if __name__ == "classes.openweather": from . import config
else: import config
import requests

class OpenWeather:
    ZERO_TEMP = -273.15

    def __init__(self, cityName):
        self.cityName = cityName
        # api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
        self.url = 'https://api.openweathermap.org/data/2.5/weather?q=' + cityName + '&appid=' + config.owApiKey

    # Return the temp for cityName
    # in case of error return ZERO_TEMP = -237.15
    def getTemp(self):
        r = requests.get(self.url)
        if r.status_code != 200: return self.ZERO_TEMP
        response = r.json()
        if 'main' in response:
            if 'temp' in response['main']: return self.ZERO_TEMP + float(response['main']['temp'])

        return self.ZERO_TEMP

# ow = OpenWeather("Firbeix")
# ow = OpenWeather("Wattignies")
# if ow.getTemp() == ow.ZERO_TEMP: print("error")
# else: print(ow.getTemp())