import re


currency = {
    'R$': 'BRL',
    '€': 'EURO'
}


def clean_price(raw_price):
    regex = '\d+[\,\.]?[\d+]*[[\,\.]\d\d]?|$'
    raw_price = re.findall(regex, raw_price)[0]
    if re.search('[.]\d\d$', raw_price):
        return raw_price.replace(',', '')
    elif re.search('[,]\d\d$', raw_price):
        return raw_price.replace('.', '').replace(',', '.')
    return re.sub('[,.]', '', raw_price)


def currency_unit(price):
    return int(float(price) * 100)


def currency_information(amount):
    for symbol, name in currency.items():
        if symbol in amount:
            return name


def pricing(response, css):
    prices = response.css(css).extract()
    if prices:
        currency = currency_information(prices[0])
        prices = [clean_price(price) for price in prices if price.strip()]
        price_in_min_unit = sorted([currency_unit(price) for price in prices if price.strip()])
        return {
            'price': price_in_min_unit[0],
            'previous_price': price_in_min_unit[1:],
            'currency': currency
        }


def is_care(care, senetence):
    senetence_lower = senetence.lower()
    return any(c in senetence_lower for c in care)
