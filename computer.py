from statistics import mean


def result_for_e(data):
    yearly_max_temperature = max([wr for wr in data if wr.max_temperature], key=lambda wr: wr.max_temperature)
    yearly_min_temperature = min([wr for wr in data if wr.min_temperature], key=lambda wr: wr.max_temperature)
    yearly_max_humidity = max([wr for wr in data if wr.max_humidity], key=lambda wr: wr.max_humidity)
    return [yearly_max_temperature, yearly_min_temperature, yearly_max_humidity]


def result_for_a(data):
    max_avg_temperature = max([wr for wr in data if wr.mean_temperature], key=lambda wr: wr.mean_temperature)
    min_avg_temperature = min([wr for wr in data if wr.mean_temperature], key=lambda wr: wr.mean_temperature)
    avg_mean_humidity = int(mean(wr.mean_humidity for wr in data if wr.mean_humidity))
    avg_mean_humidity = next((wr for wr in data if wr.mean_humidity == avg_mean_humidity), None)
    return [max_avg_temperature, min_avg_temperature, avg_mean_humidity]
