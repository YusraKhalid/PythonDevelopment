from termcolor import colored

from weather_readings_calculator import WeatherReadingsCalculator


class WeatherResultReportGenerator:
    """
    Takes calculated_weather_results from  WeatherReadingsCalculator
    then print report according data got from calculated_weather_results
    """

    def __init__(self):
        """
        store calculated_weather_results from WeatherReadingsCalculator in self.results
        """
        self.results = WeatherReadingsCalculator.calculated_weather_results

    @staticmethod
    def readable_date(date):
        """
        use month_with_num from WeatherReadingsCalculator
        :param date: 2015-06-19
        :return Jun 19:
        """
        split_date = date.split('-')
        return WeatherReadingsCalculator.month_with_num(split_date[1]) + " " + split_date[2]

    def print_report(self):
        """
        prints report according to type
        type -e
            Highest: 0.0 on Date
            Lowest: 0.0 on Date
            Humidity: 0.0% on Date
        type -a
            Highest Average 55.5
            Lowest Average 55.5
            Average Mean Humidity 55.5%
        type -c
            Year Month
            1       +++++++++++++++++++++++++++  27.0C
            1       ++++++++++++++++++++  20.0C
        type-d
            Year Month
            1       ++++++++++++++++++++++++++++++++++++++++++  17.0C -  25.0C
        :return:
        """
        for entry in self.results:
            print()
            if 'type' in entry and 'data' in entry:
                if entry['type'] == "-e":
                    for each_entry in entry['data']:
                        print(f"{each_entry['text']} "
                              f"{each_entry['value']}{each_entry['ending']} on "
                              f"{colored(self.readable_date(each_entry['date']), 'red')}")

                elif entry['type'] == "-a":
                    for each_entry in entry['data']:
                        print(f"{each_entry['text']} {each_entry['value']}{each_entry['ending']}")

                elif entry['type'] == "-c":
                    for each_entry in entry['data']:
                        print(each_entry['text'])
                        calculated_data_list = each_entry['value']

                        for each_day in calculated_data_list:
                            print(colored(each_day['pkt'].split('-')[-1] + "\t", 'red'), end='')

                            for i in range(0, int(each_day['max_temperature_c'])):
                                print(colored("+", 'red'), end='')
                            print(colored(f"  {each_day['max_temperature_c']}C", 'red'))

                            print(colored(f"{each_day['pkt'].split('-')[-1]} \t", 'blue'), end='')

                            for i in range(0, int(each_day['min_temperature_c'])):
                                print(colored("+", 'blue'), end='')
                            print(colored(f"  {each_day['min_temperature_c']}C", 'blue'))
                        print()

                elif entry['type'] == '-d':
                    for each_entry in entry['data']:
                        print(each_entry['text'])
                        calculated_data_list = each_entry['value']

                        for each_day in calculated_data_list:
                            print(f"{each_day['pkt'].split('-')[-1]} \t", end='')
                            # print(colored(each_day['pkt'].split('-')[-1] + "\t", 'red'), end='')

                            for i in range(0, (int(each_day['min_temperature_c'] +
                                                   each_day['max_temperature_c']))):
                                if i < each_day['min_temperature_c']:
                                    print(colored("+", 'blue'), end='')
                                else:
                                    print(colored("+", 'red'), end='')
                            print(colored(f"  {each_day['min_temperature_c']}C ", 'blue'), end='-')
                            print(colored(f"  {each_day['max_temperature_c']}C", 'red'))
                        print()
