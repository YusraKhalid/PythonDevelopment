import csv
import glob
from datetime import datetime
import calendar


class FileParsing:
    """
    Class for parsing the file given the command line arguments.
    It also reads the files and returns the data.
    """

    files = []
    record = {}

    def __init__(self):
        pass

    def parse_file_yearly(self, file_path, year):
        """Parse the file on the basis on year only"""

        self.files = glob.glob(
            file_path + "/Murree_weather_" 
            + year + "_*.txt")

    def parse_file_monthly(self, file_path, year, n):
        """Parse the file on the basis on year and month"""

        self.files = glob.glob(
            file_path + "/Murree_weather_" 
            + year + "_" + calendar.month_abbr[int(n)] + ".txt")
       
    def read_file(self):
        """Function for reading the files (using csv DictReader)"""
        
        if self.files:
            for path in self.files:
                with open(path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if 'PKT' in row.keys():
                            date = datetime.strptime(
                                row['PKT'],
                                "%Y-%m-%d"
                                )
                        else:
                            date = datetime.strptime(
                                row['PKST'],
                                "%Y-%m-%d"
                                )
                        data = {
                            'Max TemperatureC': row['Max TemperatureC'],
                            'Min TemperatureC': row['Min TemperatureC'],
                            'Max Humidity': row['Max Humidity'],
                            'Min Humidity': row[' Min Humidity'],
                            'Mean Humidity': row[' Mean Humidity']
                        }
                        self.record[date] = data
        else:
            return False
        
        return self.record
