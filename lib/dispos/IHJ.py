from selenium.webdriver.common.by import By
from lib.common import Product, price_to_float, weight_to_float

def scrapeIHJ(driver, url, filter):
    
    filterURL = url + filter

    driver.get(filterURL)
    driver.implicitly_wait(1.5)
    
    # Smooth scroll to scrub ALL data
    scheight = .1
    while scheight < 9.9:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
        scheight += .0075

    # This is the "load more" btn (unclickable b/c reactModal) not important rn but TODO: fix to load more products
    # btn = driver.find_element(By.CSS_SELECTOR, ".css-1vpb7ta")
    
    # Card elements that contain all of the product details
    product_card_elements = driver.find_elements(By.CSS_SELECTOR, ".css-1o21u79")

    products = []

    for elem in product_card_elements:
        prod = parse_product(elem)
        products.append(prod)

    print("\n", len(products), "products scraped")

    return products


def parse_product(element):

    # Extract prod info text from element
    prod_name = element.find_element(By.CLASS_NAME, "css-4qmyxz").text
    prod_company = element.find_element(By.CLASS_NAME, "css-1ketu3n").text
    prod_type = element.find_element(By.CLASS_NAME, "css-m6dbny").text
    prod_strain = element.find_element(By.CLASS_NAME, "css-1lekzkb").text
    prod_thc = element.find_element(By.CLASS_NAME, "css-g89h0y").text
    prod_prices_element = element.find_element(By.CLASS_NAME, "css-14enic0").find_element(By.CLASS_NAME, "css-1sv1nr7")
    prod_price_element = prod_prices_element.find_element(By.CLASS_NAME, "css-pevxb0")
    prod_price = prod_price_element.text
    
    # product weight
    if(len(prod_price_element.find_elements(By.TAG_NAME, "span")) > 0):
        prod_weight = weight_to_float(prod_price_element.find_element(By.TAG_NAME, "span").text)
    else:
        prod_weight = 100 #TODO: Figure out how to handle no weight products (extract from name??)

    # TODO: set dispo and dpg
    prod_dispo = ""
    prod_dpg = 0

    product = Product(
        name=prod_name,
        company=prod_company,
        type=prod_type,
        strain=prod_strain,
        thc=prod_thc,
        prices = [
            {
                "weight" : prod_weight,
                "price" : price_to_float(prod_price)
            }
        ],
        dispo=prod_dispo,
        dpg=prod_dpg
    )

    return product