import requests
import parsel

class UrlGenerator:

    # This method accepts city code and
    # returns then list of years for which weather hisory is available
    @staticmethod
    def get_year_range_from_dropdown(city_code):
        url = f"https://www.wunderground.com/history/airport/{city_code}/1996/1/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
        response = requests.get(url)
        parser_s = parsel.Selector(response.text)
        for option in parser_s.css('select.year > option::text').extract():
            yield option

    # The function accepts list of years with city code and returns a list of all URLs
    @staticmethod
    def get_dynamic_url_list(city_code):
        years_range = UrlGenerator.get_year_range_from_dropdown(city_code)
        for year in years_range:
            for month in range(1, 13):
                yield f"https://www.wunderground.com/history/airport/{city_code}/{year}/{month}/1/MonthlyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
