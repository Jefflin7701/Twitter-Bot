import sys
import twitter_functions
import requests
import json
import random


def main():
    api = twitter_functions.create_api()
    twitter_functions.version()

    name = "JeffLWeatherBot"
    twitter_functions.get_user(api, name)

    key = "f80a3666b091f671da0edd5bdf4477df"
    lat = 40.7128
    lon = -74.0060
    weatherAPI = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, key)
    response = requests.get(weatherAPI)
    data = json.loads(response.text)

    cities = ["New York", "London", "Paris", "Moscow", "Tokyo", "Dubai", "Singapore", "Rome", "Los Angeles", "Madrid"]

    for x in cities:
        if (x == "New York"):
            lat = 40.7128
            lon = -74.0060
        elif (x == "London"):
            lat = 51.5074
            lon = -0.1278
        elif (x == "Paris"):
            lat = 48.8566
            lon = 2.3522
        elif (x == "Moscow"):
            lat = 55.7558
            lon = 37.6173
        elif (x == "Tokyo"):
            lat = 35.6804
            lon = 139.7690
        elif (x == "Dubai"):
            lat = 25.2048
            lon = 55.2708
        elif (x == "Singapore"):
            lat = 1.3521
            lon = 103.8198
        elif (x == "Rome"):
            lat = 41.9028
            lon = 12.4964
        elif (x == "Los Angeles"):
            lat = 34.0522
            lon = -118.2437
        elif (x == "Madrid"):
            lat = 40.4168
            lon = 3.7038
        weatherAPI = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, key)
        response = requests.get(weatherAPI)
        data = json.loads(response.text)

        #timezone
        timezone = data["timezone"]
        timezone = timezone + "\n"
        #temperature
        celsius = data["current"]["temp"]
        fahrenheit = (celsius * 1.8) + 32
        fahrenheit = str(fahrenheit)

        #feels like
        feels_like_celsius = data["current"]["feels_like"]
        feels_like_fahrenheit = (feels_like_celsius * 1.8) + 32
        feels_like_fahrenheit = str(feels_like_fahrenheit)

        #pressure
        pressure = data["current"]["pressure"]
        pressure = str(pressure)

        #humidity
        humidity = data["current"]["humidity"]
        humidity = str(humidity)

        #dew point
        dew_point_celsius = data["current"]["dew_point"]
        dew_point_fahrenheit = (dew_point_celsius * 1.8) + 32
        dew_point_fahrenheit = str(dew_point_fahrenheit)

        #wind speed
        wind_speed = data["current"]["wind_speed"]
        wind_speed = str(wind_speed)

        #descriptions
        main = data["current"]["weather"][0]["main"]
        description = data["current"]["weather"][0]["description"]

        timezone_msg = "Timezone: " + timezone
        temp_msg = "Temperature: " + fahrenheit + " °F"
        feels_like_msg = "Feels Like: " + feels_like_fahrenheit + " °F"
        pressure_msg = "Pressure: " + pressure + " millibars"
        humidity_msg = "Humidity: " + humidity + " g/kg-1"
        dew_point_msg = "Dew Point: " + dew_point_fahrenheit + " °F"
        wind_speed_msg = "Wind Speed: " + wind_speed + " mph"
        main_msg = "Main: " + main
        description_msg = "Description: " + description

        message = timezone_msg + '\n' + temp_msg + '\n' + feels_like_msg + '\n' + pressure_msg + '\n' + humidity_msg + '\n' + dew_point_msg + '\n' + wind_speed_msg + '\n' + main_msg + '\n' + description_msg

        twitter_functions.post_tweet(api, message)



if __name__ == "__main__":
       main()