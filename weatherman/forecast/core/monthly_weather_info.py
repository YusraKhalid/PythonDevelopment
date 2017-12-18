from forecast.core.daily_weather_info import DailyWeatherInfo

from forecast.core.date_utils import DateUtils


class MonthlyWeatherInfo:
    def __init__(self, weather_info_list):
        del (weather_info_list[0])
        self.month = weather_info_list[0].split(',')[0]
        self.daily_weathers_info = [DailyWeatherInfo(weather_info) for weather_info in weather_info_list]

    def get_display_month(self):
        return DateUtils.get_month_with_year(self.month)