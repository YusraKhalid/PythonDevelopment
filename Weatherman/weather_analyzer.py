class WeatherAnalyzer:

    @staticmethod
    def highest_avg_temp(weather_readings):
        return int(sum(r.highest_temp for r in weather_readings) / len(weather_readings))

    @staticmethod
    def lowest_avg_temp(weather_readings):
        return int(sum(r.lowest_temp for r in weather_readings) / len(weather_readings))

    @staticmethod
    def average_mean_humidity(weather_readings):
        return int(sum(r.mean_hum for r in weather_readings) / len(weather_readings))

    @staticmethod
    def highest_temperature(weather_readings):
        return max(weather_readings, key=lambda r: r.highest_temp)

    @staticmethod
    def lowest_temperature(weather_readings):
        return min(weather_readings, key=lambda r: r.lowest_temp)

    @staticmethod
    def highest_humidity(weather_readings):
        return max(weather_readings, key=lambda r: r.highest_hum)