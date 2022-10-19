import re

class Product:
  def __init__(self, name, company, type, strain, thc, prices, dispo, dpg):
    self.name = name
    self.company = company
    self.type = type
    self.strain = strain
    self.thc = thc
    self.prices = prices
    self.dispo = dispo
    self.dpg = dpg

def oz_to_g(oz):
    if (oz == "1/8"):
        return float(3.5)
    elif (oz == "1/4"):
        return float(7.0)
    elif (oz == "1/2"):
        return float(14.0)
    elif (oz == "1"):
        return float(28.0)
    else:
        return float(0.01) #N/A flag

def price_to_float(str_price):
    return re.sub("\$", "", str_price)

def weight_to_float(str_weight):
    if "oz" in str_weight: # fraction (oz)
        return oz_to_g(re.sub("[-oz ]", "", str_weight))
    else:
        return float(re.sub("[-/g ]", "", str_weight))

