# -*- coding: utf-8 -*-

# Define here the models for your scraped items


import scrapy


class EnergymadeeasyItem(scrapy.Item):
    id = scrapy.Field()
    timestamp = scrapy.Field()
    db = scrapy.Field()
    db_zone = scrapy.Field()
    meter_type = scrapy.Field()
    effective_from = scrapy.Field()
    solar = scrapy.Field()
    restricted_eligibility = scrapy.Field()
    solar_meter_fee = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    supply = scrapy.Field()
    single_or_peak_rate = scrapy.Field()
    # Same as above field
    peak_rate_1 = scrapy.Field()
    block_type = scrapy.Field()
    peak_step_1 = scrapy.Field()
    peak_rate_2 = scrapy.Field()
    peak_step_2 = scrapy.Field()
    peak_rate_3 = scrapy.Field()
    peak_step_3 = scrapy.Field()
    peak_rate_4 = scrapy.Field()
    seasonal_off_peak_rate = scrapy.Field()
    off_peak_rate = scrapy.Field()
    off_peak_step_1 = scrapy.Field()
    off_peak_rate_2 = scrapy.Field()
    off_peak_step_2 = scrapy.Field()
    off_peak_rate_3 = scrapy.Field()
    off_peak_step_3 = scrapy.Field()
    off_peak_rate_4 = scrapy.Field()
    off_peak_season_off_peak_rate = scrapy.Field()
    controlled_off_peak_rate = scrapy.Field()
    shoulder = scrapy.Field()
    split_week_tariff = scrapy.Field()
    shoulder_rate_off_peak_season = scrapy.Field()
    minimum_monthly_demand_charged = scrapy.Field()
    capacity_charge = scrapy.Field()
    time_structure_code = scrapy.Field()
    seasonal = scrapy.Field()
    peak_season = scrapy.Field()
    season_duration = scrapy.Field()
    limited_solar_capacity = scrapy.Field()
    fit = scrapy.Field()
    tou_based_fit_peak = scrapy.Field()
    tou_based_fit_off_peak = scrapy.Field()
    tou_based_fit_shoulder = scrapy.Field()
    green = scrapy.Field()
    green_note = scrapy.Field()

    guaranteed_discount_off_usage = scrapy.Field()
    guaranteed_discount_off_bill = scrapy.Field()
    pot_discount_off_usage = scrapy.Field()
    pot_discount_off_bill = scrapy.Field()
    dd_discount_off_bill = scrapy.Field()
    dd_discount_off_usage = scrapy.Field()
    e_bill_discount_off_bill = scrapy.Field()
    e_bill_discount_off_usage = scrapy.Field()
    online_signup_discount_off_bill = scrapy.Field()
    online_signup_discount_off_usage = scrapy.Field()
    dual_fuel_discount_off_bill = scrapy.Field()
    dual_fuel_discount_off_usage = scrapy.Field()

    contract_length = scrapy.Field()
    etf = scrapy.Field()
    limited_benefit_period = scrapy.Field()
    other_dd_incentive = scrapy.Field()
    service_fee = scrapy.Field()
    home_product = scrapy.Field()
    price_fix_days = scrapy.Field()
    price_fix_month = scrapy.Field()
    update_status = scrapy.Field()
    connection_fee = scrapy.Field()
    reconnection_fee = scrapy.Field()
    disconnection_fee = scrapy.Field()
    cheque_dishonour_fee = scrapy.Field()
    dd_dishonour_fee = scrapy.Field()
    late_payment_fee = scrapy.Field()
    paper_bill_fee = scrapy.Field()
    payment_processing_fee = scrapy.Field()
    credit_card_processing_fee = scrapy.Field()
    other_fee = scrapy.Field()
    green_charge_10_charge = scrapy.Field()
    green_charge_10_description = scrapy.Field()
    green_charge_20_charge = scrapy.Field()
    green_charge_20_description = scrapy.Field()
    green_charge_100_charge = scrapy.Field()
    green_charge_100_description = scrapy.Field()
    cooling_off_period = scrapy.Field()
    payment_options = scrapy.Field()
    other_incentives = scrapy.Field()
    incentive_type = scrapy.Field()
    approx_incentive_value = scrapy.Field()
    eme_url = scrapy.Field()
    vec_offer_code = scrapy.Field()
    offer_end_date = scrapy.Field()

    # ADDED LATER

    single_rate = scrapy.Field()
    controlled_load_1 = scrapy.Field()
    controlled_load_2 = scrapy.Field()
    demand_usage_rate = scrapy.Field()
    eme_offer_code = scrapy.Field()
    terms_and_conditions = scrapy.Field()
    billing_period = scrapy.Field()
    contract_expiry = scrapy.Field()
    meter_restrictions = scrapy.Field()
    link_to_offer = scrapy.Field()
    pricing_zone = scrapy.Field()

    # SELF INSERTED

    raw_controlled_loads = scrapy.Field()
    energy_plan = scrapy.Field()
    raw_usage_rates = scrapy.Field()
    raw_restrictions = scrapy.Field()
    raw_discount_and_incentives = scrapy.Field()
    source = scrapy.Field()