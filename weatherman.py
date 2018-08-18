import argparse
import copy
import csv
import datetime
import glob
import os
import re
from time import strptime

COLOR_RED = '\033[91m'
COLOR_BLUE = '\033[94m'
COLOR_PURPLE = '\033[35m'
COLOR_DEFAULT = '\033[0m'


def is_valid_directory(dir_name):
    if os.path.isdir(dir_name):
        return dir_name

    error_message = '{} is not valid directory'.format(dir_name)
    raise argparse.ArgumentTypeError(error_message)


def is_valid_year_and_month(year_and_month):
    match = re.fullmatch('^(19|20)[0-9][0-9]/(1[0-2]|0[1-9]|\d)', year_and_month)
    if match:
        return year_and_month

    error_message = '{} is not valid year/month'.format(year_and_month)
    raise argparse.ArgumentTypeError(error_message)


def is_valid_year(year):
    match = re.fullmatch('^(19|20)[0-9][0-9]', year)
    if match:
        return year

    error_message = '{} is not valid year'.format(year)
    raise argparse.ArgumentTypeError(error_message)


def get_year_and_month(file_name):
    year = file_name[15:19]
    month = file_name[20:23]
    return year, strptime(month, '%b').tm_mon


class FileParser:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.year_data = {}

    def read_files_name(self, required_year, required_month=None):
        if self.year_data.get(required_year, {}).get(required_month):
            return

        if required_month:
            current_date = datetime.datetime.now()
            required_month = current_date.replace(month=int(required_month)).strftime("%b")
            required_files_path = '*{}_{}.txt'.format(required_year, required_month)
        else:
            required_files_path = '*{}*.txt'.format(required_year)

        required_files_path = os.path.join(self.dir_path, required_files_path)
        required_files_path = glob.glob(required_files_path)
        files_required = [os.path.basename(csv_file) for csv_file in required_files_path]

        return files_required

    def parse_month_data(self, file_data):
        month_data = {}
        index = 1
        for row in file_data:
            month_data[index] = {
                'Max TemperatureC': '0' if row['Max TemperatureC'] == '' else row['Max TemperatureC'],
                'Min TemperatureC': '0' if row['Min TemperatureC'] == '' else row['Min TemperatureC'],
                'Max Humidity': '0' if row['Max Humidity'] == '' else row['Max Humidity'],
                'PKT': row['PKT']
            }
            index += 1

        return month_data

    def read_files(self, files_list):
        for file_name in files_list:
            with open(os.path.join(self.dir_path, file_name), 'r') as csv_file:
                year, month = get_year_and_month(file_name)
                file_data = csv.DictReader(csv_file, skipinitialspace=True, delimiter=',')
                month_data = self.parse_month_data(file_data)

                if not self.year_data.get(year):
                    self.year_data[year] = {}

            self.year_data[year][month] = copy.deepcopy(month_data)


class ResultCalculator:

    def calculate_average_results(self, month_data):
        sum_highest = sum(int(day['Max TemperatureC']) for day in month_data.values())
        sum_lowest = sum(int(day['Min TemperatureC']) for day in month_data.values())
        sum_humidity = sum(int(day['Max Humidity']) for day in month_data.values())
        count = len(month_data)
        return {
            'Highest Average': sum_highest / count,
            'Lowest Average': sum_lowest / count,
            'Average Humidity': sum_humidity / count
        }

    def calculate_extreme_results(self, year_data):
        min_temp_list = []
        max_temp_list = []
        max_humidity_list = []

        for month in year_data.values():
            day_with_max_temperature = max(month.items(), key=lambda day: int(day[1]['Max TemperatureC']))
            max_temp_list.append((int(day_with_max_temperature[1]['Max TemperatureC']),
                                  day_with_max_temperature[1]['PKT']))

            day_with_min_temperature = min(month.items(), key=lambda day: int(day[1]['Min TemperatureC']))
            min_temp_list.append((int(day_with_min_temperature[1]['Min TemperatureC']),
                                  day_with_min_temperature[1]['PKT']))

            day_with_max_humidity = max(month.items(), key=lambda day: int(day[1]['Max Humidity']))
            max_humidity_list.append((int(day_with_max_humidity[1]['Max Humidity']),
                                      day_with_max_humidity[1]['PKT']))

        highest_temp_and_date = max(max_temp_list, key=lambda month: month[0])
        lowest_temp_and_date = min(min_temp_list, key=lambda month: month[0])
        highest_humidity_and_date = max(max_humidity_list, key=lambda month: month[0])

        return {
            'Highest Temp': highest_temp_and_date[0],
            'Highest Temp Date': highest_temp_and_date[1],
            'Lowest Temp': lowest_temp_and_date[0],
            'Lowest Temp Date': lowest_temp_and_date[1],
            'Highest Humidity': highest_humidity_and_date[0],
            'Highest Humidity Date': highest_humidity_and_date[1]
        }


class ResultGenerator:

    def generate_extreme_results(self, data):
        date = datetime.datetime.strptime(data['Highest Temp Date'], '%Y-%m-%d')
        month = date.strftime("%b")
        print('Highest: {}C on {} {}'.format(data['Highest Temp'], month, date.day))

        date = datetime.datetime.strptime(data['Lowest Temp Date'], '%Y-%m-%d')
        month = date.strftime("%b")
        print('Lowest: {}C on {} {}'.format(data['Lowest Temp'], month, date.day))

        date = datetime.datetime.strptime(data['Highest Humidity Date'], '%Y-%m-%d')
        month = date.strftime("%b")
        print('Humidity: {}% on {} {}\n'.format(data['Highest Humidity'], month, date.day))

    def generate_average_results(self, data):
        print('Highest Average: {}C'.format(round(data['Highest Average'], 2)))
        print('Lowest Average: {}C'.format(round(data['Lowest Average'], 2)))
        print('Average Mean Humidity: {}%\n'.format(round(data['Average Humidity'], 2)))

    def generate_chart_results(self, year, month, month_data):
        current_date = datetime.datetime.now()
        month = current_date.replace(month=int(month)).strftime("%B")
        print('{} {}{}'.format(month, year, COLOR_PURPLE))

        for day_number, day in month_data.items():
            print('{:0>2d} {} {}C\n{:0>2d} {} {}C'.format(day_number,
                                                          COLOR_RED + '+' * int(day['Max TemperatureC']),
                                                          COLOR_PURPLE + day['Max TemperatureC'],
                                                          day_number,
                                                          COLOR_BLUE + '+' * int(day['Min TemperatureC']),
                                                          COLOR_PURPLE + day['Min TemperatureC']))

        print(COLOR_DEFAULT)

    def generate_bonus_results(self, year, month, month_data):
        current_date = datetime.datetime.now()
        month = current_date.replace(month=int(month)).strftime("%B")
        print('{} {}{}'.format(month, year, COLOR_PURPLE))

        for day_number, day_data in month_data.items():
            print('{:0>2d} {}{} {}C - {}C'.format(day_number,
                                                  COLOR_BLUE + '+' * int(day_data['Min TemperatureC']),
                                                  COLOR_RED + '+' * int(day_data['Max TemperatureC']),
                                                  COLOR_PURPLE + day_data['Min TemperatureC'],
                                                  day_data['Max TemperatureC']))

        print(COLOR_DEFAULT)


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('dir_path',
                                 type=is_valid_directory,
                                 help='Directory path of weather files')
    argument_parser.add_argument('-e', '--extreme-report',
                                 type=is_valid_year,
                                 help='Generates extreme weather report, taking year as input')
    argument_parser.add_argument('-a', '--average-report',
                                 type=is_valid_year_and_month,
                                 help='Generates average weather report, taking year and month as input')
    argument_parser.add_argument('-c', '--chart-report',
                                 type=is_valid_year_and_month,
                                 help='Generates two line reports, taking year and month as input')
    argument_parser.add_argument('-b', '--bonus',
                                 type=is_valid_year_and_month,
                                 help='Generates single line reports, taking year and month as input')

    args = argument_parser.parse_args()

    file_parser = FileParser(args.dir_path)
    result_calculator = ResultCalculator()
    result_generator = ResultGenerator()

    if args.extreme_report:
        files_name = file_parser.read_files_name(args.extreme_report)
        if files_name:
            file_parser.read_files(files_name)
        else:
            print('Sorry! data is not available of required year provided with -e')

        if file_parser.year_data.get(args.extreme_report):
            year_data = file_parser.year_data[args.extreme_report]
            year_result = result_calculator.calculate_extreme_results(year_data)
            result_generator.generate_extreme_results(year_result)

    if args.average_report:
        year, month = args.average_report.split('/')
        month = int(month)
        files_name = file_parser.read_files_name(year, month)
        if files_name:
            file_parser.read_files(files_name)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            month_result = result_calculator.calculate_average_results(month_data)
            result_generator.generate_average_results(month_result)
        else:
            print('Sorry! data is not available of required year and month provided with -a')

    if args.chart_report:
        year, month = args.chart_report.split('/')
        month = int(month)
        files_name = file_parser.read_files_name(year, month)
        if files_name:
            file_parser.read_files(files_name)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            result_generator.generate_chart_results(year, month, month_data)
        else:
            print('Sorry! data is not available of required year and month provided with -c')

    if args.bonus:
        year, month = args.bonus.split('/')
        month = int(month)
        files_name = file_parser.read_files_name(year, month)
        if files_name:
            file_parser.read_files(files_name)

        if file_parser.year_data.get(year, {}).get(month):
            month_data = file_parser.year_data[year][month]
            result_generator.generate_bonus_results(year, month, month_data)
        else:
            print('Sorry! data is not available of required year and month provided with -b')


if __name__ == '__main__':
    main()
