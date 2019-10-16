"""This module give weather details
"""
    
import sys
from datetime import datetime, timedelta

class bcolors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'

CITY = "lahore"

def read_file_line(fp, path, date):
    if fp is None:
        filepath = "%s/%s_weather_%s_%s.txt" % (path,
                                                CITY, 
                                                date.strftime("%Y"),
                                                date.strftime("%b"))  
        fp = open(filepath)
        fp.readline()
        fp.readline()
    return [fp.readline() , fp]

def get_month_day(date):
    year, month, day = date.split("-")
    date = datetime(int(year), int(month), int(day))
    return "%s %s" % (date.strftime("%B"), date.strftime("%d"))

def year_details(year,path):
    start_year = datetime(int(year), 1, 1)
    end_year = datetime(int(year)+1, 1, 1)
    delta = timedelta(days=31)
    max_temperature_record = []
    lowest_temperature_record = []
    max_humidity_record = []

    fp = None
    while (start_year < end_year):
        try:
            line, fp = read_file_line(fp, path, start_year);
            while line:
                data = line.split(",")
                if len(data) == 23 and data[1] is not "":
                    if len(max_temperature_record) == 0 or int(data[1]) > int(max_temperature_record[1]):
                        max_temperature_record = data
                    
                    if len(lowest_temperature_record) == 0 or int(data[3]) < int(lowest_temperature_record[3]):
                        lowest_temperature_record = data
                    
                    if len(max_humidity_record) == 0 or int(data[7]) > int(max_humidity_record[7]):
                        max_humidity_record = data        
                line,fp = read_file_line(fp, path, start_year);
               
        except:
            pass    
        
        start_year += delta
        fp = None
    print ("Highest: %sC on %s" % (max_temperature_record[1], 
                                   get_month_day(max_temperature_record[0])))
    print ("Lowest: %sC on %s" % (lowest_temperature_record[3], 
                                  get_month_day(lowest_temperature_record[0])))
    print ("Humid: %s%% on %s" % (max_humidity_record[7], 
                                  get_month_day(max_humidity_record[0])))

def month_average_detail(date,path):
    year, month = date.split("/")
    date = datetime(int(year), int(month), 1)
    average_max_temperature_record = []
    average_lowest_temperature_record = []
    average_max_humidity_record = []
    fp = None
    try:
        line, fp = read_file_line(fp, path, date);
        while line:
            data = line.split(",")
            if len(data) == 23 and data[1] is not "":
                if len(average_max_temperature_record) == 0 or int(data[2]) > int(average_max_temperature_record[2]):
                    average_max_temperature_record = data
                
                if len(average_lowest_temperature_record) == 0 or int(data[2]) < int(average_lowest_temperature_record[3]):
                    average_lowest_temperature_record = data
                
                if len(average_max_humidity_record) == 0 or int(data[8]) > int(average_max_humidity_record[8]):
                    average_max_humidity_record = data        
            line, fp = read_file_line(fp, path, date);

        print ("%s %s" % (date.strftime("%B"), date.strftime("%Y")))

        print ("Highest Average: %sC" % (average_max_temperature_record[2]))
        print ("Lowest Average: %sC" % (average_lowest_temperature_record[2]))
        print ("Average Humid: %s%%" % (average_max_humidity_record[8]))

    except:
        pass  

    

def month_horizontal_chart(date, path):
    year, month = date.split("/")
    date = datetime(int(year), int(month), 1)
    delta = timedelta(days=1)
    mode = sys.argv[1]
    fp = None
    print ("%s %s" % (date.strftime("%B"), date.strftime("%Y")))

    try:
        line, fp = read_file_line(fp, path, date);
        while line:
            data = line.split(",")
            if len(data) == 23 and data[1] is not "":
                print "%s " %(date.strftime("%d")),
                for index in range(int(data[3])):
                    print "%s+%s" %(bcolors.BLUE, bcolors.ENDC),

                if mode == '-d':
                    print " %s\n%s " %(data[3], date.strftime("%d")),     
                
                for index in range(int(data[1])):
                    print "%s+%s" %(bcolors.RED, bcolors.ENDC),

                if mode == '-d':
                    print " %s" %(data[1]) 
                else:   
                    print "%sC - %sC " %(data[3], data[1])
            date += delta
            line = fp.readline()
                
    except:
        pass

if __name__ == "__main__" :

    tasks = {
        "-e":year_details,
        "-a":month_average_detail,
        "-c":month_horizontal_chart,
        "-d":month_horizontal_chart,
    }
    mode, date, path = sys.argv[1:]
    tasks[mode](date, path)

