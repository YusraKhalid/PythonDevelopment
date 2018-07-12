from DataStructure import *

from argparse import ArgumentParser


def main():
    arg_parser = ArgumentParser(description='Process some integer')
    arg_parser.add_argument('path', type=str, nargs='+',
                            help='Collect the data from Directory')
    arg_parser.add_argument('-e', type=str, nargs='+',
                            help='Find the highest temperature and day, '
                                 'lowest temperature and day, most humid day '
                                 '(Single Month)')
    arg_parser.add_argument('-a', type=str, nargs='+',
                            help='Find the average highest temperature,'
                                 ' average lowest temperature, average mean '
                                 'humidity (Range of Months)')
    arg_parser.add_argument('-c', type=str, nargs='+',
                            help='Draws two horizontal bar charts for the'
                                 ' highest and lowest temperature on each  '
                                 'day. Highest in  red and lowest in blue. ('
                                 'Range of Months)')
    args = arg_parser.parse_args()
    try:
        if args.e:
            year_report = WeatherReport()
            year_report.file_read(args.path[0], args.e[0], '*')
            year_report.yearly_report()

        if args.a:
            year_month = args.a[0].split('/')
            year = year_month[0]

            month_report = WeatherReport()
            month = datetime.strptime(year_month[1], "%m").strftime('%b')
            month_report.file_read(args.path[0], year, month)
            month_report.monthly_report()

        if args.c:
            year_month = args.c[0].split('/')
            year = year_month[0]

            daily_report = WeatherReport()
            month = datetime.strptime(year_month[1], "%m").strftime('%b')
            daily_report.file_read(args.path[0], year, month)
            daily_report.daily_report()

    except ValueError:
        print("No Such File Exist | Invalid Input")


if __name__ == "__main__":
    main()
