import argparse
import csv
import os
from datetime import datetime

from weatherreading import WeatherReading


class Validator:
    @staticmethod
    def validate_date(date):
        try:
            date = date.split('/')
            date = '{}-{}-01'.format(date[0], int(date[1]))
            date = datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(date)
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def validate_year(year):
        try:
            return int(year)
        except ValueError:
            msg = "Not a valid year: '{0}'.".format(year)
            raise argparse.ArgumentTypeError(msg)


class WeatherParser:
    def __init__(self, path):
        os.chdir(os.getcwd() + '/' + path)
        self.weather_readings = []

    def read_readings(self):
        for readings_file in os.listdir():
            with open(readings_file, 'r') as readings_csv_file:
                for row in csv.DictReader(readings_csv_file, fieldnames=self.get_headers(readings_file)):
                    if not any(garbage in (row.get('PKT') or row.get('PKST'))
                               for garbage in ['PKT', 'PKST', '<!--']):
                        if row["Max TemperatureC"] and row["Min TemperatureC"] \
                                and row["Max Humidity"] and row[" Mean Humidity"]:
                            self.weather_readings.append(WeatherReading(row))
        return self.weather_readings

    def get_headers(self, data_file):
        headers = []
        with open(data_file) as csv_data:
            reader = csv.reader(csv_data)
            for row in reader:
                if row:
                    headers = row
                    break
        return headers


class WeatherAnalyzer:
    def __init__(self, path):
        self.report_reader = WeatherParser(path)

    def filter_monthly_reports(self, year, month):
        filter_readings = []
        for reading in self.report_reader.read_readings():
            if month == reading.date.month and reading.date.year == year:
                filter_readings.append(reading)
        return filter_readings

    def filter_yearly_reports(self, year):
        filter_readings = []
        for reading in self.report_reader.read_readings():
            if year == reading.date.year:
                filter_readings.append(reading)
        return filter_readings

    def analyze_monthly_report(self, date):
        monthly_records = self.filter_monthly_reports(date.year, date.month)
        avg_max_temp = self.calculate_average(monthly_records, 'max_temp')
        avg_min_temp = self.calculate_average(monthly_records, 'min_temp')
        avg_mean_humidity = self.calculate_average(monthly_records, 'mean_humidity')
        return {'avg_max_temp': avg_max_temp, 'avg_min_temp': avg_min_temp, 'avg_mean_humidity': avg_mean_humidity}

    def calculate_average(self, records, key):
        length = len(records)
        avg_record_value = round(sum(getattr(record, key) for record in records) / length)
        return avg_record_value

    def analyze_yearly_report(self, year):
        yearly_records = self.filter_yearly_reports(year)
        max_temp_record = max(yearly_records, key=lambda record: record.max_temp)
        min_temp_record = min(yearly_records, key=lambda record: record.min_temp)
        max_humidity_record = max(yearly_records, key=lambda record: record.mean_humidity)
        return {'max_temp_record': max_temp_record,
                'min_temp_record': min_temp_record,
                'max_humidity_record': max_humidity_record
                }

    def analyze_single_bar_chart_report(self, date):
        monthly_records = self.filter_monthly_reports(date.year, date.month)
        return monthly_records


class WeatherReporter:

    def report_monthly_analysis(self, monthly_reports):
        report_statements = [
            f"Highest Average: {monthly_reports['avg_max_temp']}C",
            f"Lowest Average: {monthly_reports['avg_min_temp']}C",
            f"Average Mean Humidity: {monthly_reports['avg_mean_humidity']}%"
        ]
        self.print_reports_statements(report_statements)

    @staticmethod
    def print_reports_statements(report_statements):
        for report_statement in report_statements:
            print(report_statement)

    def report_yearly_analysis(self, yearly_reports):
        reports_statements = [
            f"Highest: {yearly_reports['max_temp_record'].max_temp}C "
            f"on {yearly_reports['max_temp_record'].date.strftime('%B %d')}",
            f"Highest: {yearly_reports['min_temp_record'].min_temp}C "
            f"on {yearly_reports['min_temp_record'].date.strftime('%B %d')}",
            f"Highest: {yearly_reports['max_humidity_record'].max_humidity}C "
            f"on {yearly_reports['max_humidity_record'].date.strftime('%B %d')}",
        ]
        self.print_reports_statements(reports_statements)

    def display_single_bar_chart_report(self, daily_record):
        print(daily_record.date.strftime("%d")
              + '+' * daily_record.max_temp + ' '
              + '\033[91m {}C\033[00m'.format(daily_record.max_temp) + '\n' +
              daily_record.date.strftime("%d")
              + '+' * daily_record.min_temp + ' '
              + '\033[34m{}C\033[00m'.format(daily_record.min_temp))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument('-e', type=Validator.validate_year, nargs='*')
    parser.add_argument('-a', type=Validator.validate_date, nargs='*')
    parser.add_argument('-c', type=Validator.validate_date, nargs='*')
    args = parser.parse_args()
    return args


def main():
    arguments = parse_arguments()
    analyzer = WeatherAnalyzer(arguments.path)
    reporter = WeatherReporter()
    if arguments.e:
        for e in arguments.e:
            yearly_results = analyzer.analyze_yearly_report(e)
            reporter.report_yearly_analysis(yearly_results)
    if arguments.a:
        for a in arguments.a:
            monthly_results = analyzer.analyze_monthly_report(a)
            reporter.report_monthly_analysis(monthly_results)
    if arguments.c:
        for c in arguments.c:
            daily_results = analyzer.analyze_single_bar_chart_report(c)
            for daily_record in daily_results:
                reporter.display_single_bar_chart_report(daily_record)


if __name__ == "__main__":
    main()
