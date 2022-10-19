from selenium.webdriver.common.by import By
from lib.common import Product, price_to_float, weight_to_float

# TODO: fix dpb
# TODO: regex prices + weights [DONE]
# TODO: clean names

# Scrapes URL and returns a list of products
def scrapeBerkshire(driver, filter): #DONE: Add filter var

    # Connect to URL
    filterURL = "https://dutchie.com/dispensary/berkshire-roots-east-boston"+ filter

    driver.get(filterURL)
    driver.implicitly_wait(1.5)

    # Age verification
    try:
        driver.find_element(By.CLASS_NAME, "age-confirmation-modal__StyledButton-di8wrk-0").click()
    except:
        print("")

    # Smooth scroll to scrub ALL data
    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .0075

    # Main element with all products
    main_element = driver.find_element(By.TAG_NAME, "main")
    
    # Searching for the product lists
    element_products = main_element.find_element(By.CLASS_NAME, "product-list__Container-sc-1arkwfu-1")
    element_div = element_products.find_element(By.TAG_NAME, "div")
    element_prod_list = element_div.find_elements(By.CLASS_NAME, "mobile-product-list-item__Container-zxgt1n-0")
    prod_list = element_prod_list[1:len(element_prod_list)-1]

    # Scraping the product details elements
    elements_products_info = []
    ignored_products = 0
    for elem in prod_list:

        # #if zxgt1n-4 exists
        if (len(elem.find_elements(By.CLASS_NAME, "mobile-product-list-item__ProductDetails-zxgt1n-4")) > 0): 
            details_element = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductDetails-zxgt1n-4")
            # Scraping prices (weights, prices, discounts)
            if ( len(elem.find_elements(By.CLASS_NAME, "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2")) > 0): # product has multiple options/prices
                prices_element = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2") 
                elements_products_info.append((details_element, prices_element))
            else:
                prices_element = elem.find_element(By.CLASS_NAME, "clickable__StyledButton-uqcx8d-0")
                elements_products_info.append((details_element, prices_element))
       
        elif (len(elem.find_elements(By.CLASS_NAME, "mobile-product-list-item__ProductInfoContainer-zxgt1n-5")) > 0): #if zxgt1n-5 exists (inner container) && outside product details container
            temp = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductInfoContainer-zxgt1n-5")
            details_element = temp.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductDetails-zxgt1n-4")
            # Scraping prices (weights, prices, discounts)

            if ( len(details_element.find_elements(By.CLASS_NAME, "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2")) > 0): # product has multiple options/prices
                prices_element = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2") 
                elements_products_info.append((details_element, prices_element))
            elif ( len(details_element.find_elements(By.CLASS_NAME, "clickable__StyledButton-uqcx8d-0")) > 0):
                prices_element = elem.find_element(By.CLASS_NAME, "clickable__StyledButton-uqcx8d-0")
                elements_products_info.append((details_element, prices_element))
        
                

        else:
            print("Product scrape failed from Berkshire")
            ignored_products+=1
        
        
    # Parsing the product details elements
    products = []
    for elem in elements_products_info:
        products.append(parseProductElements(elem[0], elem[1]))
    print(len(products), "products scraped from Berkshire!", "\n", str(ignored_products), "products not scraped")
  
    return products


# Takes in the details and prices elements and parses through to find the info
# Returned as a single product
def parseProductElements(details_element, price_element):

    _weight = ""
    _price = ""
    _oldprice = ""
    _discount = ""
        
    name_element = details_element.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductName-zxgt1n-6")
    name_text = name_element.text 

    try:
        company_element = details_element.find_element(By.CLASS_NAME, "mobile-product-list-item__Brand-zxgt1n-3")
        company_text = company_element.text
    except:
        company_text = "Company Info Not Found"

    try:
        info_element = details_element.find_element(By.CLASS_NAME, "mobile-product-list-item__DetailsContainer-zxgt1n-1")
        info_text = info_element.text
    except:
        info_text = "Info Not Found"
    
    if (price_element.get_attribute("class") == "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2"): #Multiple Prices
        # prices and weight elements contained inside button inside div container
        div_elements = price_element.find_elements(By.TAG_NAME, "div")
        for div in div_elements:
            button_element = div.find_element(By.CLASS_NAME, "clickable__StyledButton-uqcx8d-0")
            _weight = button_element.find_element(By.CLASS_NAME, "weight-tile__Label-otzu8j-4").text
            prices = button_element.find_elements(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5")
            if (len(prices) > 1): #product is dicounted
                _discount = button_element.find_element(By.CLASS_NAME, "weight-tile__DiscountLabel-otzu8j-0").text
                for price in prices:
                    element_class = price.get_attribute("class")
                    for c in element_class.split(" "):
                        if (c == "weight-tile__StrikedOutPrice-otzu8j-6"): # discounted element
                            _oldprice = price.text
                        else:
                            _price = price.text
            else: # product not discounted
                _price = price_element.find_element(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5").text
                _oldprice = _price

    else: # Only one option/price
        _weight = price_element.find_element(By.CLASS_NAME, "weight-tile__Label-otzu8j-4").text
        prices = price_element.find_elements(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5")
        if (len(prices) > 1): #product is discounted (new price and old price share the same class)
            _discount = price_element.find_element(By.CLASS_NAME, "weight-tile__DiscountLabel-otzu8j-0").text
            for price in prices:
                element_class = price.get_attribute("class")
                for c in element_class.split(" "):
                    if (c == "weight-tile__StrikedOutPrice-otzu8j-6"): # discounted element
                        _oldprice = price.text
                    else:
                        _price = price.text
        else: # product not discounted
            _price = price_element.find_element(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5").text
            _oldprice = _price

    product = Product(
        name=name_text,
        company=company_text,
        type=info_text,
        thc=info_text,
        prices = [
            {
                "weight" : weight_to_float(_weight),
                "price" : price_to_float(_price),
                "oldprice" : price_to_float(_oldprice),
                "discount" : _discount
            }
        ],
        dispo="Berkshire Roots",
        dpg=0
    )

    return product