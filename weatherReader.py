""" This file contains the WeatherReader, Calculator
    and result classes, which are used to store data,
    calculate results, and store those results respectively

    Owner: Muhammad Abdullah Zafar -- Arbisoft
"""

import csv
import sys
from os import listdir
from os.path import isfile, join, exists
from datetime import datetime

month_trans_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                    4: 'Apr', 5: 'May', 6: 'Jun',
                    7: 'Jul', 8: 'Aug', 9: 'Sep',
                    10: 'Oct', 11: 'Nov', 12: 'Dec'}


def mk_int(string_int, t):
    string_int = string_int.strip()

    if not string_int and t == 'min':
        return sys.maxsize
    elif not string_int and t == 'max':
        return (-sys.maxsize - 1)
    else:
        return int(string_int)


def mk_int_zero(string_int):
    string_int = string_int.strip()
    return int(string_int) if string_int else 0


def date_translation(date):
    if date:
        date_object = datetime.strptime(date, '%Y-%m-%d')
    else:
        return None
    if date_object:
        return datetime.strftime(date_object, '%B %d')
    else:
        return None


class ResultContainer:
    result_list = []

    def add_result(self, result_type, value, date):
        self.result_list.append({'type': result_type,
                                 'value': value,
                                 'date': date})

    def clear_results(self):
        self.result_list.clear()

    def print_results(self):
        for result in self.result_list:
            character = 'C'
            if 'Humidity' in result['type']:
                character = '%'

            if result['date']:
                print(result['type'], ': ',
                      result['value'], character, ' on ',
                      date_translation(result['date']),
                      sep='')
            else:
                print(result['type'], ': ',
                      result['value'], character,
                      sep='')


class Calculator:
    result = ResultContainer()

    def calculate_highest(self, weather_data):
        highest_temp = {'value': (-sys.maxsize - 1), 'date': ''}
        lowest_temp = {'value': (sys.maxsize), 'date': ''}
        highest_humid = {'value': (-sys.maxsize - 1), 'date': ''}

        for day in weather_data:
            date = day.data.get('PKT')

            day_max_temp = {'date': date,
                            'value': mk_int(day.data.get('MaxTemp'),
                                            'max')
                            }

            day_min_temp = {'date': date,
                            'value': mk_int(day.data.get('MinTemp'),
                                            'min')
                            }

            day_max_humid = {'date': date,
                             'value': mk_int(day.data.get('MaxHumidity'),
                                             'max')
                             }

            if day_max_temp['value'] > highest_temp['value']:
                highest_temp['value'] = day_max_temp['value']
                highest_temp['date'] = date

            if day_min_temp['value'] < lowest_temp['value']:
                lowest_temp['value'] = day_min_temp['value']
                lowest_temp['date'] = date

            if day_max_humid['value'] > highest_humid['value']:
                highest_humid['value'] = day_max_humid['value']
                highest_humid['date'] = date

        self.result.clear_results()

        self.result.add_result('Highest',
                               highest_temp['value'],
                               highest_temp['date'])

        self.result.add_result('Lowest',
                               lowest_temp['value'],
                               lowest_temp['date'])

        self.result.add_result('Humidity',
                               highest_humid['value'],
                               highest_humid['date'])

        return self.result

    def calculate_average(self, weather_data):
        avg_highest_temp = 0
        avg_lowest_temp = 0
        avg_mean_humid = 0
        skip_days_min = 0
        skip_days_max = 0
        skip_days_mean = 0

        for day in weather_data:
            init_max_temp = mk_int_zero(day.data.get('MaxTemp'))
            init_min_temp = mk_int_zero(day.data.get('MinTemp'))
            init_mean_humid = mk_int_zero(day.data.get('MeanHumidity'))

            if not init_max_temp:
                skip_days_max += 1
            else:
                avg_highest_temp += init_max_temp

            if not init_min_temp:
                skip_days_min += 1
            else:
                avg_lowest_temp += init_min_temp

            if not init_mean_humid:
                skip_days_mean += 1
            else:
                avg_mean_humid += init_mean_humid

        avg_highest_temp /= len(weather_data) - skip_days_max
        avg_lowest_temp /= len(weather_data) - skip_days_min
        avg_mean_humid /= len(weather_data) - skip_days_mean

        self.result.clear_results()
        self.result.add_result('Highest Average', int(avg_highest_temp), '')
        self.result.add_result('Lowest Average', int(avg_lowest_temp), '')
        self.result.add_result('Avg Mean Humidity', int(avg_mean_humid), '')

        return self.result

    def calculate_bar_charts(self, weather_data):

        self.result.clear_results()
        purple = "\033[0;35;40m"
        red = "\033[0;31;40m+"
        blue = "\033[0;34;40m+"

        for day in weather_data:
            day_max_temp = day.data.get('MaxTemp')
            day_min_temp = day.data.get('MinTemp')

            date = day.data.get('PKT')
            if date:
                date = datetime.strptime(date, '%Y-%m-%d')
                date = datetime.strftime(date, '%d') + ' '

                range_max_temp = range(abs(mk_int_zero(day_max_temp)))
                range_min_temp = range(abs(mk_int_zero(day_min_temp)))

                final_string = ''
                final_string = purple + date
                final_string += ''.join([blue for x in range_min_temp])
                final_string += ''.join([red for x in range_max_temp])
                final_string += ' ' + purple + day_min_temp + 'C'
                final_string += ' - ' + purple + day_max_temp + 'C'

                print(final_string.replace(purple + 'C', 'No Value Available'))

        print("\033[0;0;40m")

    def compute(self, weather_data, calculation_type, req):
        color = "\033[1;30;47m"
        color_reset = "\033[0;37;40m"
        dialouge = 'Report for ' + req + ' for option ' + calculation_type
        if calculation_type == '-e':
            if len(req.split('/')) != 1:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            return self.calculate_highest(weather_data)

        elif calculation_type == '-a':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            return self.calculate_average(weather_data)

        elif calculation_type == '-c':
            if len(req.split('/')) != 2:
                print("Wrong format. Exiting!")
                exit()

            print(color + dialouge + color_reset)
            print(datetime.strftime(datetime.strptime(req, '%Y/%m'), '%B %Y'))
            return self.calculate_bar_charts(weather_data)


class SingleReading:
    data = {}

    def __init__(self, reading):
        self.data = {'PKT': reading.get('PKT'),
                     'MaxTemp': reading.get('Max TemperatureC'),
                     'MinTemp': reading.get('Min TemperatureC'),
                     'MaxHumidity': reading.get('Max Humidity'),
                     'MeanHumidity': reading.get('Mean Humidity')}


class WeatherReader:
    data = []

    def __init__(self, directory, request):
        self.data = []
        if exists(directory):
            all_files = [f for f in listdir(directory)]
        else:
            print("Directory does not exists!")
            return None

        year_month = request.split('/')
        year = request.split('/')[0]
        month = 0
        month_files = []
        if int(year) > 1000 and int(year) < 9999:
            files = [x for x in all_files if year in x]
        else:
            self.data.append('year_error')
            return None

        if len(year_month) > 1:
            if request.split('/')[1]:
                month = int(request.split('/')[1])

        if month and month > 0 and month < 13:
            month_files = [x for x in files
                           if month_trans_dict.get(month) in x]
            files = month_files
        else:
            self.data.append('month_error')
            return None

        for file in files:
            with open(directory + '/' + file) as csvfile:
                readCSV = csv.DictReader(csvfile,
                                         delimiter=',',
                                         skipinitialspace=True)
                for row in readCSV:
                    day_reading = SingleReading(row)
                    self.data.append(day_reading)
