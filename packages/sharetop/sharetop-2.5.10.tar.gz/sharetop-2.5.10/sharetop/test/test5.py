from sharetop.core.country.country_base_info import get_country_base_info
from sharetop.core.oil.oil_detail import get_oil_reserves, get_oil_products, get_oil_consumption, \
    get_oil_refinerythroughput, get_oil_refinerycapacity, get_oil_crudeoilpricehistory
from sharetop.core.pig.pig_detail import get_fcr
from sharetop.core.stock.bill_monitor import get_stock_history_capital


d = get_country_base_info("f109298d079b5f60")
# d = get_oil_crudeoilpricehistory("f109298d079b5f60")
# d = get_fcr('2023-05-01', '2023-05-16')
# d = get_country_base_info(10)
# d = get_oil_crudeoilpricehistory(20)
print(d)

# d = get_history_bill('002714')

# print(d.to_dict("records"))

