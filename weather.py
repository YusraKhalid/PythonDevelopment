import sys
import datetime
import csv


# The class responsible for reading and organizing the data
class Parser:
    # Read all files line by line and return them
    @staticmethod
    def read(files_input):
        collection = []

        for path in files_input:
            with open(path, 'r') as f:
                data = csv.DictReader(f)

                for line in data:
                    collection.append(dict(line))

        return collection

    # Read all the previously read lines and filter headers and useless rows
    def clean(self, dict_array):
        clean_data = []

        for data in dict_array:
            keys = data.keys()

            if 'PKST' in keys:
                data['PKT'] = data['PKST']
                del data['PKST']

            for key in keys:
                if key != key.strip():
                    data[key.strip()] = data[key]
                    del data[key]

            if self.includes_relevant_data(data):
                clean_data.append(data)

        return clean_data

    # Check if the tuple contains at least one of the required attributes
    @staticmethod
    def includes_relevant_data(entry):
        if entry['Max TemperatureC'] or \
                entry['Mean TemperatureC'] or \
                entry['Min TemperatureC'] or \
                entry['Max Humidity'] or \
                entry['Mean Humidity'] or \
                entry['Min Humidity']:
            return True

        return False


# The class responsible for performing calculations
class Calculator:
    def calculate_annual_result(self, organized_data, year):
        result = {'Lowest Annual Temp': self.find_annual_lowest_temp(organized_data, f"{year}-"),
                  'Highest Annual Temp': self.find_annual_highest_temp(organized_data, f"{year}-"),
                  'Highest Annual Humidity': self.find_annual_highest_humidity(organized_data, f"{year}-")}

        return result

    @staticmethod
    def find_annual_highest_temp(organized_data, year):
        temps = []
        dates = []

        for data in organized_data:
            if year in data['PKT']:
                if data['Max TemperatureC']:
                    temps.append(int(data['Max TemperatureC']))
                    dates.append(data['PKT'])

        if len(temps):
            highest = max(temps)
            return [highest, dates[temps.index(highest)]]
        else:
            return [-sys.maxsize, '1990-1-1']

    @staticmethod
    def find_annual_highest_humidity(organized_data, year):
        temps = []
        dates = []

        for data in organized_data:
            if year in data['PKT']:
                if data['Max Humidity']:
                    temps.append(int(data['Max Humidity']))
                    dates.append(data['PKT'])

        if len(temps):
            highest = max(temps)
            return [highest, dates[temps.index(highest)]]
        else:
            return [-sys.maxsize, '1990-1-1']

    @staticmethod
    def find_annual_lowest_temp(organized_data, year):
        temps = []
        dates = []

        for data in organized_data:
            if year in data['PKT']:
                if data['Min TemperatureC']:
                    temps.append(int(data['Min TemperatureC']))
                    dates.append(data['PKT'])

        if len(temps):
            lowest = min(temps)
            return [lowest, dates[temps.index(lowest)]]
        else:
            return [sys.maxsize, '1990-1-1']

    @staticmethod
    def calculate_monthly_average_report(organized_data, year, month):
        result = {}
        date = f"{year}-{month}"

        high_temps = []
        low_temps = []
        mean_humidity_val = []

        for data in organized_data:
            if date in data['PKT']:
                if data['Max TemperatureC']:
                    high_temps.append(int(data['Max TemperatureC']))
                if data['Min TemperatureC']:
                    low_temps.append(int(data['Min TemperatureC']))
                if data['Max Humidity']:
                    mean_humidity_val.append(int(data['Mean Humidity']))

        if len(high_temps) == 0 or len(low_temps) == 0 or \
                len(mean_humidity_val) == 0:
            return {}

        result['Average Highest Temp'] = sum(high_temps) / len(high_temps)
        result['Average Lowest Temp'] = sum(low_temps) / len(low_temps)
        result['Average Mean Humidity'] = sum(
            mean_humidity_val) / len(mean_humidity_val)

        return result

    @staticmethod
    def calculate_daily_extremes_report(organized_data, year, month):
        result = {}
        date = f"{year}-{month}-"

        dates = []
        min_temps = []
        max_temps = []

        for data in organized_data:
            if date in data['PKT']:
                if data['Max TemperatureC'] and data['Min TemperatureC']:
                    dates.append(data['PKT'])
                    min_temps.append(data['Min TemperatureC'])
                    max_temps.append(data['Max TemperatureC'])

        result['Dates'] = dates
        result['Min Temps'] = min_temps
        result['Max Temps'] = max_temps
        return result


# The class responsible for presenter the calculations
class Presenter:
    @staticmethod
    def str_to_date(string):
        date = string.split('-')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

    def present_annual_report(self, report):
        high = report['Highest Annual Temp']
        low = report['Lowest Annual Temp']
        humid = report['Highest Annual Humidity']

        if humid[0] == -sys.maxsize or low[0] == sys.maxsize or \
                high[0] == -sys.maxsize:
            print('Invalid data or input')
            return

        date = self.str_to_date(high[1])
        print("Highest: {0}C on {1}".format(high[0], date.strftime("%d %B")))

        date = self.str_to_date(low[1])
        print("Lowest: {0}C on {1}".format(low[0], date.strftime("%d %B")))

        date = self.str_to_date(humid[1])
        print("Humidity: {0}% on {1}\n".format(
            humid[0], date.strftime("%d %B")))

    @staticmethod
    def present_monthly_average_report(report):

        if 'Average Highest Temp' not in report or \
                'Average Lowest Temp' not in report or \
                'Average Mean Humidity' not in report:
            print('Invalid data or input')
            return

        print('Highest Average: {0}C'.format(
            round(report['Average Highest Temp'])))
        print('Lowest Average: {0}C'.format(
            round(report['Average Lowest Temp'])))
        print('Average Mean Humidity: {0}%\n'.format(
            round(report['Average Mean Humidity'])))

    def present_daily_extremes_report(self, report, horizontal=False):
        dates = report['Dates']
        min_temps = report['Min Temps']
        max_temps = report['Max Temps']

        if len(dates) == 0 or len(dates) != len(min_temps) or \
                len(dates) != len(max_temps):
            print('Invalid data or input')
            return

        date = self.str_to_date(dates[0])
        print(date.strftime('%B %Y'))

        for i in range(0, len(dates)):
            day = dates[i].split(
                '-')[2] if len(dates[i].split('-')[2]) == 2 else f"0{dates[i].split('-')[2]}"

            low = '+' * abs(int(min_temps[i]))
            high = '+' * abs(int(max_temps[i]))

            if not horizontal:
                print(u"{0} \u001b[34m{1}\u001b[0m {2}C".format(
                    day, high, int(max_temps[i])))
                print(u"{0} \u001b[31m{1}\u001b[0m {2}C".format(
                    day, low, int(min_temps[i])))
            else:

                print((("{0} \u001b[31m{1}\u001b[0m\u001b[34m{2}"
                        "\u001b[0m {3}C-{4}C")).format(
                    day, low, high, int(min_temps[i]), int(max_temps[i])))

        print()
