#!/usr/bin/python3
import calendar
from datetime import datetime
from data_holder import *


class FactsCalculation:
    def __init__(self, monthly_records=[], yearly_records=[]):
        self.monthly_records = monthly_records
        self.yearly_records = yearly_records

    def get_yearly_temperature_peaks(self):
        if (self.yearly_records):
            result = WeatherResults()
            result.max_temprature = self.yearly_records[0][0]
            result.min_temprature = self.yearly_records[0][0]
            result.max_humidity = self.yearly_records[0][0]
            for monthly_record in self.yearly_records:
                for daily_record in monthly_record:
                    if hasattr(daily_record,'max_temprature') and result.max_temprature.max_temprature < daily_record.max_temprature:
                        result.max_temprature = daily_record
                    if hasattr(daily_record,'min_temprature') and result.min_temprature.min_temprature > daily_record.min_temprature:
                        result.min_temprature = daily_record
                    if hasattr(daily_record,'max_humidity') and result.max_humidity.max_humidity < daily_record.max_humidity:
                        result.max_humidity = daily_record
            return result

    def get_monthly_avg_results(self):
        if (self.monthly_records):
            result = WeatherResults()
            result.max_avg_temperature = 0
            result.min_avg_temperature = 0
            result.mean_humidity_avg = 0

            for daily_record in self.monthly_records:
                if hasattr(daily_record,'max_temprature'):
                    result.max_avg_temperature += daily_record.max_temprature
                if hasattr(daily_record,'min_temprature'):
                    result.min_avg_temperature += daily_record.min_temprature
                if hasattr(daily_record,'mean_humidity'):
                    result.mean_humidity_avg += daily_record.mean_humidity
            if (len(self.monthly_records) > 0):
                row_count = len(self.monthly_records)
                result.max_avg_temperature /= row_count
                result.min_avg_temperature /= row_count
                result.mean_humidity_avg /= row_count
            return result
