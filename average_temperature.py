"""
this module calculate and display average tempaerature of
a given month
"""
from calendar import month_abbr, month_name
import glob
import constants
from csv_hanlder import WeatherCsvHandler
from utils import weather_data


class AverageTemperatue:
    """ Class for storing Average Temperatures """

    def __init__(self):
        self.average_high = constants.ZERO
        self.average_low = constants.ZERO
        self.average_humidity = constants.ZERO

    def find_average_temperature(self, file_path):
        """
        This function take file path and return the
        AverageTemperature object
        """
        high_count = constants.ZERO
        low_count = constants.ZERO
        humid_count = constants.ZERO
        if not weather_data:
            csv_handler = WeatherCsvHandler(file_path)
            csv_handler.read_csv_and_fill_data()

        for daily_weather in weather_data:
            if daily_weather.max_temperature:
                self.average_high += int(daily_weather.max_temperature)
                high_count += 1
            if daily_weather.min_temperature:
                self.average_low += int(daily_weather.min_temperature)
                low_count += 1
            if daily_weather.mean_humidity:
                self.average_humidity += int(daily_weather.mean_humidity)
                humid_count += 1

        if high_count is not constants.ZERO:
            self.average_high = self.average_high / high_count
        if low_count is not constants.ZERO:
            self.average_low = self.average_low / low_count
        if humid_count is not constants.ZERO:
            self.average_humidity = self.average_humidity / humid_count

    def show_average_temperature(self, date_str, dir_path):
        """
        this function is for displaying average temperature
        :param date_str:
        :param dir_path:
        :return: none
        """
        (year, month) = date_str.split('/')
        month = int(month)
        file_path = glob.glob(dir_path + "/*_" + year + "_" + month_abbr[month] + "*")
        if file_path:
            file_path = file_path[0]
            self.find_average_temperature(file_path)

            print("%s %s" % (month_name[month], year))
            if self.average_high is not constants.ZERO:
                print("Highest Average: %dC" % self.average_high)
            else:
                print("Highest Temperatures for this month are not present")
            if self.average_low is not constants.ZERO:
                print("Lowest Average: %dC" % self.average_low)
            else:
                print("Lowest Temperatures for this month are not present")
            if self.average_humidity is not constants.ZERO:
                print("Average Humidity: %d%%" % self.average_humidity)
            else:
                print("Average Humidity for this month are not present")
        else:
            print("No Data Found for the Specified Month")