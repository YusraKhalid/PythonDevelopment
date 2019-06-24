import datetime

from ds import YearResults, MonthResults, ChartResults

def year_report(year_results):
    print(year_results.year)
    max_temp_date = datetime.datetime.strptime(year_results.max_temp_date, "%Y-%m-%d")
    print("Highest:", end=" ")
    print(f"{year_results.max_temp}C on", end=" ")
    print(f"{max_temp_date:%B} {max_temp_date:%d}")

    min_temp_date = datetime.datetime.strptime(year_results.min_temp_date, "%Y-%m-%d")
    print("Lowest:", end=" ")
    print(f"{year_results.min_temp}C on", end=" ")
    print(f"{min_temp_date:%B} {min_temp_date:%d}")

    max_humid_date = datetime.datetime.strptime(year_results.max_humidity_date, "%Y-%m-%d")
    print("Humidity:", end=" ")
    print(f"{year_results.max_humidity}% on", end=" ")
    print(f"{max_humid_date:%B} {max_humid_date:%d}")

def month_report(month_results):
    print(month_results.month, month_results.year)
    print(f"Highest Average: {month_results.avg_high_temp}C")
    print(f"Lowest Average: {month_results.avg_low_temp}C")
    print(f"Average Mean Humidity: {month_results.avg_mean_humidity}%")
    
def chart_report(chart_results):
    print(chart_results.month, chart_results.year)
    for day in chart_results.results:
        date = datetime.datetime.strptime(day[0], "%Y-%m-%d")
        
        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[1]):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[1], "C", '\x1b[0m', sep="")

        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[2]):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[2], "C", '\x1b[0m', sep="")

def chart_bonus_report(chart_results):
    print(chart_results.month, chart_results.year)
    for day in chart_results.results:
        date = datetime.datetime.strptime(day[0], "%Y-%m-%d")
        print('\x1b[3;35m', date.strftime("%d"), '\x1b[0m', sep="", end = " ")
        for _ in range(day[2]):
            print('\x1b[0;34m', "+", '\x1b[0m', sep="", end="")
        for _ in range(day[1]):
            print('\x1b[0;31m', "+", '\x1b[0m', sep="", end="")
        print(" ", '\x1b[3;35m', day[2], "C - ", day[1], "C", '\x1b[0m', sep="")
