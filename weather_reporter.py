import calendar

from weather_analyzer import WeatherAnalyzer


class WeatherReporter:

    def __init__(self):
        self.red_color_code = '\033[31m'
        self.blue_color_code = '\033[34m'
        self.grey_color_code = '\033[37m'
        self.weather_analyzer = WeatherAnalyzer()

    def generate_annual_report(self, desired_report_year, dir_path):
        self.weather_analyzer.collect_weather_data_set(dir_path)
        temp_max_obj, temp_min_obj, \
            max_humid_obj = self.weather_analyzer.extract_year_data(
             desired_report_year)
        self.print_annual_report(temp_max_obj, temp_min_obj, max_humid_obj)

    def generate_monthly_report(self, report_year, dir_path):
        self.weather_analyzer.collect_weather_data_set(dir_path)
        month_weather_record = self.weather_analyzer.collect_month_data(
            report_year)
        max_temp_avg, min_temp_avg, \
            humidity_avg = self.weather_analyzer.compute_month_data_average(
                month_weather_record)
        self.print_monthly_report(round(max_temp_avg), round(min_temp_avg),
                                  round(humidity_avg))

    def generate_bar_chart_report(self, report_year, dir_path):
        self.weather_analyzer.collect_weather_data_set(dir_path)
        month_data_record = self.weather_analyzer.collect_month_data(
            report_year)
        bar_chart_data = self.calculate_bar_chart(month_data_record)
        self.print_monthly_bar_chart(bar_chart_data)
        print("\nBonus\n")
        bonus_bar_chart_data = self.calculate_bonus_chart(month_data_record)
        self.print_bonus_chart(bonus_bar_chart_data)

    def calculate_bar_chart(self, month_data_record):
        bar_chart_data = []
        day_num = 1
        for day_data in month_data_record:
            if day_data.max_temperature:
                bar_chart_data.append([int(day_data.max_temperature),
                                      self.red_color_code, day_num])
            if day_data.min_temperature:
                bar_chart_data.append([int(day_data.min_temperature),
                                      self.blue_color_code, day_num])
                day_num += 1
        return bar_chart_data

    def calculate_bonus_chart(self, month_data_record):
        bonus_bar_chart_data = []
        day_num = 1
        for day_weather_record in month_data_record:
            if day_weather_record.max_temperature:
                temp_max = int(day_weather_record.max_temperature)
                bar_chart_max_temp = self.red_color_code + ('+' * temp_max)
            if day_weather_record.min_temperature:
                temp_min = int(day_weather_record.min_temperature)
                bar_chart_min_temp = self.blue_color_code + ('+' * temp_min)
                bonus_bar_chart_data.append([day_num, bar_chart_min_temp,
                                            bar_chart_max_temp,
                                            temp_min, temp_max])
            day_num += 1
        return bonus_bar_chart_data

    def print_bonus_chart(self, bonus_bar_chart_data):
        for bar_chart_row in bonus_bar_chart_data:
            self.draw_bonus_bar_chart(bar_chart_row[0], bar_chart_row[1],
                                      bar_chart_row[2],
                                      bar_chart_row[3], bar_chart_row[4])
            print("")

    def print_monthly_bar_chart(self, bar_chart_data):
        for bar_chart_data in bar_chart_data:
            self.draw_bar_chart(bar_chart_data[0], bar_chart_data[1],
                                bar_chart_data[2])

    def draw_bar_chart(self, temp, temp_color_code, day_num):
        bar_chart_month = '+' * temp
        print(f"{self.grey_color_code}{day_num}{temp_color_code} "
              f"{bar_chart_month}{self.grey_color_code}{temp}C")

    def draw_bonus_bar_chart(self, day_num, bar_chart_min_temp,
                             bar_chart_max_temp,
                             temp_min, temp_max):
        print(f"{self.grey_color_code}{day_num}{bar_chart_min_temp}"
              f"{bar_chart_max_temp}{self.grey_color_code}"
              f"{temp_min}C-{self.grey_color_code}{temp_max}C")

    def print_annual_report(self, temp_max_obj, temp_min_obj,
                            max_humid_obj):
        print(f"Highest: {temp_max_obj.max_temperature}C on "
              f"{calendar.month_name[temp_max_obj.pkt.month]} "
              f"{temp_max_obj.pkt.day}")
        print(f"Lowest: {temp_min_obj.min_temperature}C on "
              f"{calendar.month_name[temp_min_obj.pkt.month]} "
              f"{temp_min_obj.pkt.day}")
        print(f"Humid: {max_humid_obj.max_humidity}% on "
              f"{calendar.month_name[max_humid_obj.pkt.month]} "
              f"{max_humid_obj.pkt.day}")
        print("")

    def print_monthly_report(self, max_temp_avg, min_temp_avg,
                             humidity_avg):
        print(f"Highest Average: {max_temp_avg}C")
        print(f"Lowest Average: {min_temp_avg}C")
        print(f"Average Mean Humidity: {humidity_avg}%")
        print("")
