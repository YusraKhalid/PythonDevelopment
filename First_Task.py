import csv
import glob
from datetime import date
flag_month = False

temp_matrix = {
                'PKT':[],
                'Max TemperatureC':[],
                'Min TemperatureC':[],
                'Max Humidity':[],
                'Mean Humidity':[]
                }

def simplify_dates(temp_date):
    temp_date=temp_date.split('-')
    for x in temp_date:
        year = int(temp_date[0])
        month = int(temp_date[1])
        day = int(temp_date[2])
    return date(day=day, month=month, year=year).strftime('%A %d %B %Y')

def main():
    '''
    Main function to handle all the other function

    '''
    y = user_input_for_year()
    m = user_input_for_month()
    file_path = make_the_files_paths(m,y)
    file_reading_directory(file_path)
    find_the_max_min_temp()
    if m != '':
        histogram_charts_for_month()

def user_input_for_year():
    """
        Take the user input and for the year
        Inputs:
                name of the year
        Output:
                returns the year
    """
    #global flag_month
    year =  input ("Please Enter the year :")
    return year

def user_input_for_month():
    """
        Take the user input and for the month

        Output:
                returns the month
    """
    month = raw_input("Please Enter the Month :")
    return month

def make_the_files_paths(month , year):
    """
        Make the file path for the local directory

        Inputs:
                file_name: name and year
        Output:
                returns the path dict for further process
    """
    path_list = []
    if not month :
         path_list.extend(glob.glob("/home/yasir/Task_Programs/weatherfiles/Murree_weather_%s_*.txt" %year))
    else:
         path_list.extend(glob.glob("/home/yasir/Task_Programs/weatherfiles/Murree_weather_%s_%s.txt" %(year,month[:3])))
    return path_list

def file_reading_directory(path_name):
    """
        Get data from  weather files for max , min and humidity

        and append this data in global dictionary(temp_matrix)
        Inputs:
                file_name: path list dictionary
        Output:
                append the data in global dict.
    """
    for path in path_name:
        with open(path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_matrix['PKT'].append(row['PKT'])
                temp_matrix['Max TemperatureC'].append(row['Max TemperatureC'])
                temp_matrix['Min TemperatureC'].append(row['Min TemperatureC'])
                temp_matrix['Max Humidity'].append(row['Max Humidity'])
                temp_matrix['Mean Humidity'].append(row[' Mean Humidity'])

def find_the_max_min_temp():

    """
        Calculate the highest and lowest temperature with date of the
        day


    """
    print '1. Given year display the highest temperature and day,\n' \
          'lowest temperature and day, most humid day and humidity.'
    print '<--------------------------------------------------------->'
    mean_hum_list =[]
    max_hum_date = []
    min_date_list =[]
    max_date_list =[]
    max_temp_list = []
    min_temp_list = []
    max_hum_list = []
    for mx_index,mx_data in enumerate(zip(temp_matrix['Max TemperatureC'],temp_matrix['PKT'])):
        if temp_matrix['Max TemperatureC'][mx_index] != '':
            max_temp_list.append(int(mx_data[0]))
            max_date_list.append(temp_matrix['PKT'][mx_index])

    for min_index,min_data in enumerate(zip(temp_matrix['Min TemperatureC'],temp_matrix['PKT'])) :
        if temp_matrix['Min TemperatureC'][min_index] != '':
            min_temp_list.append(int(min_data[0]))
            min_date_list.append(temp_matrix['PKT'][min_index])

    for max_index,mx_data in enumerate(zip(temp_matrix['Max Humidity'],temp_matrix['PKT'])) :
        if temp_matrix['Max Humidity'][max_index] != '':
            max_hum_list.append(int(mx_data[0]))
            max_hum_date.append(temp_matrix['PKT'][max_index])

    for mean_index,mean_data in enumerate(zip(temp_matrix['Mean Humidity'],temp_matrix['PKT'])) :
        if temp_matrix['Mean Humidity'][mean_index] != '':
            mean_hum_list.append(int(mean_data[0]))


    max_temperature = max(max_temp_list)
    min_temperature = min(min_temp_list)
    max_humidity = max(max_hum_list)
    max_temp_date = max_date_list[max_temp_list.index(max_temperature)]
    min_temp_date = min_date_list[min_temp_list.index(min_temperature)]
    mx_hum_date = max_hum_date[max_hum_list.index(max_humidity)]


    print 'Highest: %s C On %s' %(max_temperature,simplify_dates(max_temp_date))
    print 'Lowest :%s C On %s' %(min_temperature,simplify_dates(min_temp_date))
    print 'Highest :%s C On %s' %(max_humidity,simplify_dates(mx_hum_date))
    print '<----------------------------------------------------->'

    print '2. Given month display the average highest temperatur,\n' \
          'average lowest temperature, average mean humidity.'

    print '<----------------------------------------------------->'

    print 'Highest Average :%s C' %(sum(max_temp_list)/len(max_temp_list))
    print 'Lowest Average :%s C'%(sum(min_temp_list)/len(min_temp_list))
    print 'Average Mean Humidity :%s C' %(sum(mean_hum_list)/len(mean_hum_list))

def histogram_charts_for_month():

    """
        Make the histogram for the highest and lowest temperature

    """
    print '<-------------------------------------------------------------->'

    print '3. For a given month draw two horizontal bar charts on the console \n' \
          'for the highest and lowest temperature on each day. Highest in red and lowest in blue.'
    min_date_list =[]
    max_date_list =[]
    max_temp_list = []
    min_temp_list = []
    for mx_index,mx_data in enumerate(zip(temp_matrix['Max TemperatureC'],temp_matrix['PKT'])):
        if temp_matrix['Max TemperatureC'][mx_index] != '':
            max_temp_list.append(int(mx_data[0]))
            max_date_list.append(temp_matrix['PKT'][mx_index])
    for min_index,min_data in enumerate(zip(temp_matrix['Min TemperatureC'],temp_matrix['PKT'])) :
        if temp_matrix['Min TemperatureC'][min_index] != '':
            min_temp_list.append(int(min_data[0]))
            min_date_list.append(temp_matrix['PKT'][min_index])
    for max_d,min_d,max_v,min_v in (zip(max_date_list,min_date_list,max_temp_list,min_temp_list)):
        print max_d,'+ '*max_v,'%sC'%max_v,'\n',min_d,'- '*min_v,'%sC'%min_v
    print '<----------------------------------------------------------------->'
    print '5. BONUS TASK. For a given month draw one horizontal bar chart on the console for \n' \
          'the highest and lowest temperature on each day. Highest in red and lowest in blue.'
    for t_date,max_v,min_v in (zip(max_date_list,max_temp_list,min_temp_list)):
        print t_date,'- '*min_v,'+ '*max_v,'%sC--%sC'%(max_v,min_v)

if __name__ == '__main__':
    main()
