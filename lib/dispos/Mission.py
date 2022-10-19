from selenium.webdriver.common.by import By
from lib.common import Product, price_to_float, weight_to_float

# TODO: fix dpb
# TODO: regex prices + weights
# TODO: clean names

# Scrapes URL and returns a list of products
def scrapeMission(driver, filter): #DONE: Add filter var

    # Connect to URL
    filterURL = "https://dutchie.com/dispensary/mission-brookline" + filter

    driver.get(filterURL)
    driver.implicitly_wait(1.5)
    #time.sleep(5)

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
    elements_products_prices = []
    ignored_products = 0
    for elem in prod_list:

        if (len(elem.find_elements(By.CLASS_NAME, "mobile-product-list-item__ProductInfoContainer-zxgt1n-5")) > 0):
        
            product_details_element = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductInfoContainer-zxgt1n-5")
            product_details_element = product_details_element.find_element(By.CLASS_NAME, "mobile-product-list-item__ProductDetails-zxgt1n-4")
            
            elements_products_info.append(product_details_element)

            if(len(product_details_element.find_elements(By.TAG_NAME, "button")) > 0 ): # 1 price/button
                price_element = product_details_element.find_element(By.TAG_NAME, "button")
                elements_products_prices.append([price_element])
            else:
                price_element_container = elem.find_element(By.CLASS_NAME, "mobile-product-list-item__MultipleOptionsContainer-zxgt1n-2")
                price_divs = price_element_container.find_elements(By.TAG_NAME, "div")
                price_elements = []
                for div in price_divs:
                    price_elements.append(div.find_element(By.TAG_NAME, "button"))
                
                elements_products_info.append(price_elements)
        
    # Parsing the product details elements
    parsed_products = []
    for info, price in zip(elements_products_info, elements_products_prices):
        parsed_products.append(parseProductElements(info, price))
    print(len(parsed_products), "products scraped from Mission!", "\n", str(ignored_products), "products not scraped")
  
    return parsed_products


# Takes in the details and prices elements and parses through to find the info
# Returned as a single product
def parseProductElements(details_element, price_element):

    _weight = ""
    _prices = []
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

    for elem in price_element:
        _price = {
            "weight" :  weight_to_float(elem.find_element(By.CLASS_NAME, "weight-tile__Label-otzu8j-4").text),
            "price" : price_to_float(elem.find_element(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5").text),
            "oldprice" : price_to_float(elem.find_element(By.CLASS_NAME, "weight-tile__PriceText-otzu8j-5").text),
            "discount" : "N/A" #TODO: Figure out mission dicounts
        }
        _prices.append(_price)

    product = Product(
        name=name_text,
        company=company_text,
        type=info_text,
        thc=info_text,
        prices = _prices,
        dispo="Mission Brookline",
        dpg=0
    )

    return product