from .datastructures import WeatherReadingData
from .decorators import validate_input
from .design_patterns import Singleton
from .results_handler import ReportsHandler


class WeatherMan(metaclass=Singleton):
    """
    Contains complete flow required for working of weather man.
    """
    def __init__(self):
        self.data = None
        self.results = None

    @validate_input
    def year_result(self, *args, **kwargs):
        self.results = ReportsHandler(report_type='years')
        self.data = list()
        weather_data_holder = WeatherReadingData(
            file_path=kwargs.get('file_path'),
            year=kwargs.get('year_month')
        )
        for data in weather_data_holder.weather_data:
            self.data.append(data)

        self.data =
        for data in self.data:
            print(data)

    @validate_input
    def year_with_month_result(self, *args, **kwargs):
        print('get year result')
        return 1

    @validate_input
    def month_bar_chart_result(self, *args, **kwargs):
        print('get year result')
        return 1

    def show_result(self, file_path, option, year_month):
        return getattr(self, '{}_result'.format(option))(file_path=file_path, year_month=year_month)
