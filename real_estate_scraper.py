# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from bs4 import BeautifulSoup
import time

def navigate(driver,website):
    """Function to briefly pause script execution"""
    driver.get(website)

def create_driver(PATH):
    """inits webdriver"""
    driver = webdriver.Chrome(PATH)
    return driver

def close_scraper(driver):
    """Function closes driver execution"""
    time.sleep(5)
    driver.close()

def __pause__(seconds):
    """Function to briefly pause script execution"""
    time.sleep(seconds)
    
def current_page_listings(driver):
    """function that iterates through all listings in one page"""
    while True:
        try:
            listings = WebDriverWait(driver, 20).until(
            e_c.presence_of_all_elements_located((By.XPATH,"//div[@Id = 'search-page-list-container']//div[@class = 'list-card-info']")))
            #listings = WebDriverWait(driver, 10).until(
            #e_c.element_to_be_clickable((By.XPATH,"//div[@Id = 'search-page-list-container']//div[@class = 'list-card-info']")))
            #listings = driver.find_elements_by_xpath("//div[@Id = 'search-page-list-container']//div[@class = 'list-card-info']")
            #main = driver.find_element_by_id("search-page-list-container")
            #listing = main.find_elements_by_class_name('list-card-info')
        except (NoSuchElementException):
            print("No element found. If there is a captcha on screen\n"\
                  "Complete it manually to continue\n"\
                  "Web scraper will continue in ~15 seconds")
            time.sleep(15)
        else:
            break
    
    return listings
        
def captcha_check(driver):
    """Identifies captcha container and pauses script execution until 
    captcha is manually completed"""
    if is_web_element_displayed(driver, "captcha-container"):
        print("\nCAPTCHA!\n"\
              "Manually complete the captcha requirements.\n"\
              "Once that's done, if the program was in the middle of scraping "\
              "(and is still running), it should resume scraping after ~30 seconds.")
        captcha_pause_(driver)
        
def is_web_element_displayed(driver,element):
    try:
        web_element_displayed = driver.find_element_by_class_name(element).is_displayed()
    except:
        web_element_displayed = False
    return web_element_displayed
    
def captcha_pause_(driver):
    while True:
        time.sleep(30)
        if not is_web_element_displayed(driver, "captcha-container"):
            break

def turn_page(driver,i):
    driver.refresh()
    time.sleep(2)
    nav_bar = driver.find_element_by_class_name('search-pagination')
    WebDriverWait(nav_bar,10).until(e_c.element_to_be_clickable((By.LINK_TEXT,str(i)))).click()

def navigate_facts_features(driver):
    time.sleep(2)
    while True:
        try:
            house = get_basic_info(driver)
            WebDriverWait(driver,10).until(e_c.element_to_be_clickable((By.LINK_TEXT,'Facts and features'))).click()
        except (NoSuchElementException,TimeoutException):
             print("\nCAPTCHA!\n"\
              "Manually complete the captcha requirements.\n"\
              "Once that's done, if the program was in the middle of scraping "\
              "(and is still running), it should resume scraping after ~15 seconds.")
             time.sleep(15)
        else:
            url = get_url(driver)
            bed_bath = get_bed_bath(driver)   
            kitchen = get_kitchen(driver)
            family_room = get_family(driver)
            dining_room = get_dining(driver)
            living_room = get_living(driver)
            basement = get_basement(driver)
            flooring = get_flooring(driver)
            heat = get_heating(driver)
            cool = get_cooling(driver)
            appliances = get_appliances(driver)
            interior = get_interior(driver)
            
            super_dict = {**url,**house,
                          **bed_bath,**kitchen,
                          **family_room,**dining_room,
                          **living_room,**basement,
                          **flooring,**heat,
                          **cool,**appliances,
                          **interior}
            
            return super_dict
        
def get_url(driver):
    url = "//link[@rel = 'canonical']"
    search_xpath = driver.find_element_by_xpath(url)
    elementHTML = search_xpath.get_attribute('href')
    elementSoup = BeautifulSoup(elementHTML,'html.parser')
    
    return {"url": elementSoup.text}

def get_basic_info(driver):
    common_path = "//div[@class = 'ds-home-details-chip']"
    extra_path = "//div[@class='ds-home-facts-and-features reso-facts-features sheety-facts-features']"
    
    price = common_path+"//span[contains(text(),'$')]"
    address = common_path+"//h1[@id='ds-chip-property-address']/span"
    neighborhood = common_path+"//h1[@id='ds-chip-property-address']/span[2]"
    
    bldg = "//span[contains(text(),'Type')]/../span[2]"
    year = extra_path+"//span[contains(text(),'Year built')]/../span[2]"
    lot = extra_path+"//span[contains(text(),'Lot')]/../span[2]"
    #lot_secondary = 
    
    features = [price,address,neighborhood,bldg,year,lot]
    
    return parse_html(driver,features,['SalePrice','Address','Neighborhood','Type','YearBlt','LotSize'])
        
def get_bed_bath(driver):  
    common_path = "//h6[contains(text(),'Bedrooms and bathrooms')]"
    
    bedroom = common_path+"/..//span[contains(text(),'Bedrooms')]"
    bathroom = common_path+"/..//span[contains(text(),'Bathrooms')]"
    full_bathroom = common_path+"/..//span[contains(text(),'Full bathrooms')]"
    half_bathroom = common_path+"/..//span[contains(text(),'1/2 bathrooms')]"
    
    features = [bedroom,bathroom,full_bathroom,half_bathroom]
    
    return parse_html(driver,features,['bedrooms','bathrooms','full_brs','1/2_brs'])
    
def get_kitchen(driver):
    common_path = "//h6[contains(text(),'Kitchen')]"
    
    level = common_path+"/..//span[contains(text(),'Level')]"
    area = common_path+"/..//span[contains(text(),'Area')]"
    misc = common_path+"/..//span[contains(text(),'Features')]"
    
    features = [level,area,misc]
    
    return parse_html(driver,features,['kitchen_level','kitchen_area','kitchen_misc'])

def get_family(driver):
    common_path = "//h6[contains(text(),'FamilyRoom')]"
    
    description = common_path+"/..//span[contains(text(),'Description')]"
    level = common_path+"/..//span[contains(text(),'Level')]"
    area = common_path+"/..//span[contains(text(),'Area')]" 
    misc = common_path+"/..//span[contains(text(),'Features')]"
    
    features = [description,level,area,misc]
    
    return parse_html(driver,features,['family_desc','family_level','family_area','famly_misc'])

def get_dining(driver):
    common_path = "//h6[contains(text(),'DiningRoom')]"
    
    description = common_path+"/..//span[contains(text(),'Description')]"
    level = common_path+"/..//span[contains(text(),'Level')]"
    area = common_path+"/..//span[contains(text(),'Area')]"
    misc = common_path+"/..//span[contains(text(),'Features')]"
    
    features = [description,level,area,misc]
    
    return parse_html(driver,features,['dining_desc','dining_level','dining_area','dining_misc'])

def get_living(driver):
    common_path = "//h6[contains(text(),'LivingRoom')]"
    
    description = common_path+"/..//span[contains(text(),'Description')]"
    level = common_path+"/..//span[contains(text(),'Level')]"
    area = common_path+"/..//span[contains(text(),'Area')]"
    #misc = common_path+""
    
    features = [description,level,area]
    
    return parse_html(driver,features,['living_desc','living_level','dining_area'])

def get_basement(driver):
    common_path = "//h6[contains(text(),'Basement')]"
    
    area = common_path+"/..//span[contains(text(),'Area')]"
    qual = common_path+"/..//span[contains(text(),'Basement')]"
    
    features = [area,qual]
    
    return parse_html(driver,features,['basement_area','basement_qual'])

def get_flooring(driver):
    common_path ="//h6[contains(text(),'Flooring')]"
    flooring = common_path+"/..//span[contains(text(),'Flooring')]"
    
    features = [flooring]
    
    return parse_html(driver,features,['fooring_desc'])

def get_heating(driver):
    common_path = "//h6[contains(text(),'Heating')]"
    heat = common_path+"/..//span[contains(text(),'Heating features')]"
    
    features = [heat]
    
    return parse_html(driver,features,['heat_desc'])

def get_cooling(driver):
    cool = "//h6[contains(text(),'Cooling')]/..//span[contains(text(),'Cooling features')]"
    
    features = [cool]
    
    return parse_html(driver,features,['cooling_desc'])

def get_appliances(driver):
    appliance = "//h6[contains(text(),'Appliances')]/..//span[contains(text(),'Appliances included')]"
    
    features = [appliance]
    
    return parse_html(driver,features,['appliances'])

def get_interior(driver):
    common_path = "//h6[contains(text(),'Interior Features')]"
    
    interior = common_path+"/..//span[contains(text(),'Interior features')]"
    door = common_path+"/..//span[contains(text(),'Door features')]"
    
    features = [interior,door]
    
    return parse_html(driver,features,['interior_desc','interior_door'])

def parse_html(driver,features_paths,feature_names):
    col_names = dict.fromkeys(feature_names)
    
    for idx,element in enumerate(features_paths):
        try:
            search_xpath = driver.find_element_by_xpath(element)
        except (NoSuchElementException,ValueError):
            col_names[feature_names[idx]] = None
        else:
            elementHTML = search_xpath.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML,'html.parser')
            print(elementSoup.prettify())
            if ':' in elementSoup.get_text():
                col_names[feature_names[idx]] = elementSoup.get_text().split(":")[1]
            elif '$' in elementSoup.get_text():
                col_names[feature_names[idx]] = elementSoup.get_text().split("$")[1]
            else:
                col_names[feature_names[idx]] = elementSoup.get_text()
    
    return col_names

    