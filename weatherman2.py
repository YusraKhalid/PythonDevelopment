import os
import sys
import re
import csv

weatherman_report_data = {}   # Initializing dictionary to store data. 


def is_key_present(x):
    if x in weatherman_report_data.keys():
        return True


def is_empty(lis):
    if not lis:
        return False
    else:
        return True


def basic_weather_report_of_every_year():      # For report 1 each key value has four values in list.
    for filename in os.listdir(dir):           # weatherdata[year1][0] = Maximum temperature ,
        with open(filename) as csvfile:        # weatherdata[year1][1] = Minimum temperature ,
            name = csvfile.name                # weatherdata[year1][2] = Maximum humidity ,
            year = (re.split('_', name))       # weatherdata[year1][3] = Minimum humidity
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            minimum_temperatures = []  # To store 'Min TemperatureC' key values of a file.
            minimum_humidities = []  # To store 'Min Temperature' key values of a file.

            if is_key_present(year1):  # Updating values of existing key
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')

                    if maximum_temperature:  # Calculating maximum temperature
                        x = int(maximum_temperature)
                        if weatherman_report_data[year1][0] < x:
                            weatherman_report_data[year1][0] = x

                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

                    if maximum_humidity:  # Calculating maximum humidity
                        x = int(maximum_humidity)
                        if weatherman_report_data[year1][2] < x:
                            weatherman_report_data[year1][2] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)
            else:
                weatherman_report_data[year1] = [0, 0, 0, 0]  # Adding a new key
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    minimum_temperature = row.get('Min TemperatureC')
                    maximum_humidity = row.get('Max Humidity')
                    minimum_humidity = row.get(' Min Humidity')

                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[year1][0] < x:
                            weatherman_report_data[year1][0] = x

                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

                    if maximum_humidity:
                        x = int(maximum_humidity)
                        if weatherman_report_data[year1][2] < x:
                            weatherman_report_data[year1][2] = x

                    if minimum_humidity:
                        minimum_humidities.append(minimum_humidity)

            if is_empty(minimum_temperatures):
                min1 = min(minimum_temperatures)
                x = int(min1)
            if weatherman_report_data[year1][1] == 0:
                weatherman_report_data[year1][1] = x
            else:
                if weatherman_report_data[year1][1] > x:
                    weatherman_report_data[year1][1] = x

            if is_empty(minimum_humidities):
                min1 = min(minimum_humidities)
                x = int(min1)
            if weatherman_report_data[year1][3] == 0:
                weatherman_report_data[year1][3] = x
            else:
                if weatherman_report_data[year1][3] > x:
                    weatherman_report_data[year1][3] = x

    print("This is report# 1")
    print(
        "Year" + "  " + "Maximum Temprature " + "  " + "Minimum Temprature" + "   " + "Maximum Humidity" + "   " + "Minimum Humidity")
    print("-----------------------------------------------------------------------------------")

    for key in weatherman_report_data:
        print(key, "          ", weatherman_report_data.get(key)[0], "                ",
              weatherman_report_data.get(key)[1], "              ",
              weatherman_report_data.get(key)[2], "               ", weatherman_report_data.get(key)[3])


def find_hottest_day_of_every_year_report2():  # It will report the Hottest day of each year
    for filename in os.listdir(dir):  # For report 2, each dictioanry has two values in list i.e
        with open(filename) as csvfile:  # weather_data_report[year1][0] represents date of hottest
            name = csvfile.name  # day, while weatherman_data_report[year1][1] stores temperature
            year = (re.split('_', name))  # on that day.
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if (is_key_present(year1)):
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[year1][0] < x:
                            weatherman_report_data[year1][0] = x

            else:
                weatherman_report_data[year1] = [0, 0, 0, 0, '', '']
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if weatherman_report_data[year1][0] < x:
                            weatherman_report_data[year1][0] = x

    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if (is_key_present(year1)):
                for row in reader:
                    maximum_temperature = row.get('Max TemperatureC')
                    if maximum_temperature:
                        x = int(maximum_temperature)
                        if x == weatherman_report_data[year1][0]:
                            if 'PKT' in HeaderList:
                                weatherman_report_data[year1][4] = row.get('PKT')
                            if 'PKST' in HeaderList:
                                weatherman_report_data[year1][4] = row.get('PKST')

    print("This is report# 2")
    print("year" + "             " + "Date" + "              " + "Temp")
    print("--------------------------------------------")
    for keys in weatherman_report_data:
        print(keys, "          ", (weatherman_report_data[keys][4]), "        ", weatherman_report_data[keys][0])


def find_coolest_day_of_every_year_report3():  # It will report the coolest day of each year.
    for filename in os.listdir(dir):           # For report 3, each dictioanry has two values in list i.e
        with open(filename) as csvfile:        # weather_data_report[year1][0] represents date of coolest
            name = csvfile.name                # day & weatherman_data_report[year1][1] stores temperature on that day.
            minimum_temperatures = []  # To store 'Min TemperatureC' key values of a file
            year = (re.split('_', name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            if is_key_present(year1):
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)
            else:
                weatherman_report_data[year1] = [0, '']
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        minimum_temperatures.append(minimum_temperature)

        if is_empty(minimum_temperatures) is False:
            pass
        else:
            min1 = min(minimum_temperatures)
            x = int(min1)

        if weatherman_report_data[year1][0] == 0:
            weatherman_report_data[year1][0] = x
        else:
            if weatherman_report_data[year1][0] > x:
                weatherman_report_data[year1][0] = x

    for filename in os.listdir(dir):
        with open(filename) as csvfile:
            name = csvfile.name
            year = (re.split('_', name))
            year1 = int(year[2])
            next(csvfile)
            reader = csv.DictReader(csvfile)
            HeaderList = reader.fieldnames
            if (is_key_present(year1)):
                for row in reader:
                    minimum_temperature = row.get('Min TemperatureC')
                    if minimum_temperature:
                        x = int(minimum_temperature)
                        if x == weatherman_report_data[year1][0]:
                            if 'PKT' in HeaderList:
                                weatherman_report_data[year1][1] = row.get('PKT')
                            if 'PKST' in HeaderList:
                                weatherman_report_data[year1][1] = row.get('PKST')

    print("This is report#3 showing coolest day of each year")
    print("year" + "             " + "Date" + "              " + "Temp")
    print("--------------------------------------------")
    for keys in weatherman_report_data:
        print(keys, "          ", weatherman_report_data[keys][1], "        ", weatherman_report_data[keys][0])


if __name__ == '__main__':
    Report_no = sys.argv[1]  # Type of report you want to see.
    data_dir = sys.argv[2]  # Directory in which data to be processed is placed.
    Report_no = int(Report_no)
    os.chdir("..")
    os.chdir(data_dir)
    dir = os.getcwd()

    if Report_no == 1:
        basic_weather_report_of_every_year()
    elif Report_no == 2:
        find_hottest_day_of_every_year_report2()
    elif Report_no == 3:
        find_coolest_day_of_every_year_report3()
    else:
        print("No such report found /n"
              "select correct report number")

