import os
import csv
import datetime
import argparse
import calendar


class WeatherMan:
    def __init__(self):
        return

    @staticmethod
    def clean_blank_from_records(temperature_records):
        temperature_records = \
            dict((k, v)
                 for k, v in temperature_records.iteritems() if v)
        return temperature_records

    @staticmethod
    def find_maximum_in_records(temperature_records):
        records_numeric_values = \
            list(map(int, temperature_records.values()))
        records_max_value = max(records_numeric_values)
        records_keys = [k for k, v in temperature_records.items()
                        if v == str(records_max_value)]
        records_max_key = max(records_keys)
        return [records_max_value, records_max_key]

    @staticmethod
    def find_minimum_in_records(temperature_records):
        records_numeric_values = \
            list(map(int, temperature_records.values()))
        records_min_value = min(records_numeric_values)
        records_keys = [k for k, v in temperature_records.items()
                        if v == str(records_min_value)]
        records_min_key = max(records_keys)
        return [records_min_value, records_min_key]

    @staticmethod
    def calculate_annual_report(temperature_records):
        daily_date_record = \
            [x['PKT'] for x in temperature_records]

        daily_max_temperature_record = \
            [x['Max TemperatureC'] for x in temperature_records]
        temperature_and_date = \
            dict(zip(daily_date_record, daily_max_temperature_record))
        temperature_and_date = \
            WeatherMan().clean_blank_from_records(temperature_and_date)
        max_temperature_record = \
            WeatherMan().find_maximum_in_records(temperature_and_date)

        daily_min_temp_record = [x['Min TemperatureC'] for x in temperature_records]
        minimum_temperature_records = \
            dict(zip(daily_date_record, daily_min_temp_record))
        minimum_temperature_records = \
            WeatherMan().clean_blank_from_records(minimum_temperature_records)
        min_temperature_record = \
            WeatherMan().find_minimum_in_records(minimum_temperature_records)

        humidity_record = [x['Max Humidity'] for x in temperature_records]
        humidity_date_records = \
            dict(zip(daily_date_record, humidity_record))
        humidity_date_records = \
            WeatherMan().clean_blank_from_records(humidity_date_records)
        max_humidity_record = \
            WeatherMan().find_maximum_in_records(humidity_date_records)

        annual_report = []
        annual_report.append(max_temperature_record)
        annual_report.append(min_temperature_record)
        annual_report.append(max_humidity_record)
        return annual_report

    @staticmethod
    def print_annual_report(annual_report):
        max_temperature_record = annual_report[0]
        max_temperature_day = max_temperature_record[1].day
        max_temperature_month = month_of_year[max_temperature_record[1].month - 1]
        print ("Highest : " +
               str(max_temperature_record[0]) +
               " on " +
               str(max_temperature_day) +
               " " +
               str(max_temperature_month)
               )
        min_temperature_record = annual_report[1]
        min_temperature_day = min_temperature_record[1].day
        min_temperature_month = month_of_year[min_temperature_record[1].month - 1]
        print ("Lowest  : " +
               str(min_temperature_record[0]) +
               " on " +
               str(min_temperature_day) +
               " " +
               str(min_temperature_month)
               )
        max_humidity_record = annual_report[2]
        most_humid_day = max_humidity_record[1].day
        most_humid_month = month_of_year[max_humidity_record[1].month - 1]
        print("Max Humidity : " +
              str(max_humidity_record[0]) +
              " on " +
              str(most_humid_day) +
              " " +
              str(most_humid_month)
              )

    @staticmethod
    def calculate_monthly_report(temperature_records):
        daily_maximum_temperature = \
            [x['Max TemperatureC'] for x in temperature_records if x['Max TemperatureC']]
        maximum_temperature_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_maximum_temperature)) / len(daily_maximum_temperature)

        daily_minimum_temperature = \
            [x['Min TemperatureC'] for x in temperature_records if x['Min TemperatureC']]
        mainimum_temperature_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_minimum_temperature)) / len(daily_minimum_temperature)

        daily_mean_humidity = \
            [x['Mean Humidity'] for x in temperature_records if x['Mean Humidity']]
        maximum_humidity_mean = reduce(
            lambda x, y: x + y,
            map(int, daily_mean_humidity)) / len(daily_mean_humidity)

        monthly_mean_calculations = []
        monthly_mean_calculations.append(maximum_temperature_mean)
        monthly_mean_calculations.append(mainimum_temperature_mean)
        monthly_mean_calculations.append(maximum_humidity_mean)
        return monthly_mean_calculations

    @staticmethod
    def print_monthly_calculation(monthly_mean_calculations):
        highest_average = monthly_mean_calculations[0]
        lowest_average = monthly_mean_calculations[1]
        average_mean_humidity = monthly_mean_calculations[2]
        print ("Highest Average : " +
               str(highest_average) + "C")
        print ("Lowest Average : " +
               str(lowest_average) + "C")
        print ("Average Mean Humidity : " +
               str(average_mean_humidity) + "%")

    @staticmethod
    def calculate_barchart_values(temperature_records):
        daily_calculation = []
        daily_maximum_temperatue = \
            [x['Max TemperatureC'] for x in temperature_records]
        daily_minimum_temperatue = \
            [x['Min TemperatureC'] for x in temperature_records]
        daily_calculation.append(daily_maximum_temperatue)
        daily_calculation.append(daily_minimum_temperatue)
        return daily_calculation

    @staticmethod
    def print_bar_chart(daily_calculation):
        column_to_be_read = [1, 3]
        color_start = ['\033[1;31m', '\033[1;34m']
        color_end = ['\033[1;m', '\033[1;m']
        for day in range(len(daily_calculation[0])):
            for iteration, column_number in enumerate(column_to_be_read):
                if daily_calculation[iteration][day]:
                    printline = '+' * int(daily_calculation[iteration][day])
                else:
                    printline = ""
                print (str(day + 1) +
                       color_start[iteration] +
                       printline +
                       color_end[iteration] +
                       daily_calculation[iteration][day]
                       )

    @staticmethod
    def calculate_oneline_chart_values(temperature_records):
        daily_maximum = \
            [x['Max TemperatureC'] for x in temperature_records]
        daily_minimum = \
            [x['Min TemperatureC'] for x in temperature_records]
        monthly_record = []
        monthly_record.append(daily_maximum)
        monthly_record.append(daily_minimum)
        return monthly_record

    @staticmethod
    def print_oneline_chart(monthly_record):
        daily_maximum = monthly_record[0]
        daily_minimum = monthly_record[1]
        red_color = ['\033[1;31m', '\033[1;m']
        blue_color = ['\033[1;34m', '\033[1;m']
        for day in range(len(daily_maximum)):
            if (daily_minimum[day]):
                bluebar = blue_color[0] + \
                          '+' * int(daily_minimum[day]) + \
                          blue_color[1]
            else:
                bluebar = ""
            if daily_maximum[day]:
                redbar = red_color[0] + \
                         '+' * int(daily_maximum[day]) \
                         + red_color[1]
            else:
                redbar = ""

            print (str(day + 1) +
                   bluebar + redbar +
                   daily_minimum[day] +
                   "-" +
                   daily_maximum[day])

    @staticmethod
    def parse_date(calculated_date):
        date = calculated_date.split("-")
        formated_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        return formated_date

    @staticmethod
    def fetch_records_from_files(path_to_files):
        files_in_directory = [target_file for target_file in os.listdir(path_to_files)]
        file_reader = ""
        temperature_records = []
        for file_for_processing in files_in_directory:
            file_for_processing = argument.path_to_file + "/" + file_for_processing
            if os.path.isfile(file_for_processing):
                with open(file_for_processing, 'r') as csvfile:
                    next(csvfile)
                    file_reader = csv.DictReader(
                        filter(lambda row: row[0] != '<', csvfile)
                    )
                    file_reader.fieldnames[0] = "PKT"
                    file_reader.fieldnames[1] = "Max TemperatureC"
                    file_reader.fieldnames[3] = "Min TemperatureC"
                    file_reader.fieldnames[7] = "Max Humidity"
                    file_reader.fieldnames[8] = "Mean Humidity"
            for line in file_reader:
                temperature_records.append(line)

        for record in temperature_records:
            record["PKT"] = WeatherMan.parse_date(str(record["PKT"]))
        return temperature_records

    @staticmethod
    def refine_data(temperature_records, date_argument):
        date_argument = date_argument.split("/")
        extracted_record = []
        year = int(date_argument[0])
        if (len(date_argument) == 2):
            month = int(date_argument[1])
            for record in temperature_records:
                if (record["PKT"].year == year and record["PKT"].month == month):
                    extracted_record.append(record)
        else:
            for record in temperature_records:
                if (record["PKT"].year == year):
                    extracted_record.append(record)
        return extracted_record

if __name__ == '__main__':
    month_of_year = [month for month in calendar.month_abbr]
    month_of_year.pop(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--annual", nargs="?", type=str)
    parser.add_argument("-a", "--monthly", nargs="?", type=str)
    parser.add_argument("-c", "--bar_chart", nargs="?", type=str)
    parser.add_argument("-z", "--oneline", nargs="?", type=str)
    parser.add_argument("path_to_file", help="Path of folder")
    argument = parser.parse_args()
    temperature_records = WeatherMan().fetch_records_from_files(argument.path_to_file)

    if argument.annual:
        extracted_record = \
            WeatherMan().refine_data(temperature_records, format(argument.annual))
        annual_report = \
            WeatherMan().calculate_annual_report(extracted_record)
        WeatherMan().print_annual_report(annual_report)
    if argument.monthly:
        extracted_record = \
            WeatherMan().refine_data(temperature_records, format(argument.monthly))
        monthly_calculations = \
            WeatherMan().calculate_monthly_report(extracted_record)
        WeatherMan().print_monthly_calculation(monthly_calculations)
    if argument.bar_chart:
        extracted_record = \
            WeatherMan().refine_data(temperature_records, format(argument.bar_chart))
        monthly_barchart_values = \
            WeatherMan().calculate_barchart_values(extracted_record)
        WeatherMan.print_bar_chart(monthly_barchart_values)
    if argument.oneline:
        extracted_record = \
            WeatherMan().refine_data(temperature_records, format(argument.oneline))
        monthly_barchart_values = \
            WeatherMan().calculate_oneline_chart_values(extracted_record)
        WeatherMan().print_oneline_chart(monthly_barchart_values)
