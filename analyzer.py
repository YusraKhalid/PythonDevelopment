class WeatherAnalyzer:
    """Extracts aggregate information from WeatherReading objects"""

    def average(self, readings, key):
        """Returns average of values for given key"""
        total = 0
        count = 0
        for reading in readings:
            value = getattr(reading, key)
            if value is not None:
                total = total + value
                count = count + 1
        return round(total/count) if count != 0 else 0

    def maximum(self, readings, key):
        """Returns reading with maximum value for key"""
        max_reading = readings[0]
        for reading in readings:
            value = getattr(reading, key)
            max_value = getattr(max_reading, key)
            if value is not None and value > max_value:
                max_reading = reading
        return max_reading

    def minimum(self, readings, key):
        """Returns reading with minimum value for key"""
        min_reading = readings[0]
        for reading in readings:
            value = getattr(reading, key)
            min_value = getattr(min_reading, key)
            if value is not None and value < min_value:
                min_reading = reading
        return min_reading

    def get_maximum_temperatures(self, readings):
        """Returns a list of maximum temperature in a month ordered by date"""
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.max_temperature for w in readings]

    def get_minimum_temperatures(self, readings):
        """Returns a list of minimum temperature in a month ordered by date"""
        readings = sorted(readings, key=lambda w: w.date.day)
        return [w.min_temperature for w in readings]
