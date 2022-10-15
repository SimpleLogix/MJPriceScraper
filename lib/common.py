
class Product:
  def __init__(self, name, company, type, thc, prices, dispo, dpg):
    self.name = name
    self.company = company
    self.type = type
    self.thc = thc
    self.prices = prices
    self.dispo = dispo
    self.dpg = dpg

def oz_to_g(oz):
    if (oz == "1/8"):
        return "3.5"
    elif (oz == "1/4"):
        return "7.0"
    elif (oz == "1/2"):
        return "14.0"
    elif (oz == "1"):
        return "28.0"
    else:
        return "0.01" #N/A