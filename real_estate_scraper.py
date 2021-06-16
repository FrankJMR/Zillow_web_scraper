# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import numpy as np
import time

def navigate(driver,website):
    """Function to briefly pause script execution"""
    try:
        driver.get(website)
    except (TimeoutException):
         print("Web page could not be reached\n"\
               "If there is a captcha complete it manually to continue\n"\
               "Web scraper will continue in ~15 seconds\n")

def close_listing(driver):
    close_path = "//button[contains(@class,'ds-close-lightbox-icon')]//div"
    WebDriverWait(driver,10).until(e_c.element_to_be_clickable((By.XPATH,close_path))).click()
    time.sleep(2)
    
def get_current_url(driver):
    return driver.current_url
    
def create_driver(PATH):
    """inits webdriver"""
    chop = ChromeOptions()
    chop.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path = PATH,chrome_options = chop)
    return driver

def close_scraper(driver):
    """Function closes driver execution"""
    time.sleep(5)
    driver.close()
    
def current_page_listings(driver):
    """function that iterates through all listings in one page"""
    while True:
        try:
            listings = WebDriverWait(driver, 20).until(
            e_c.visibility_of_all_elements_located((By.XPATH,"//div[@class = 'list-card-info']/../../../li[not(descendant-or-self::node()/@class[contains(.,'nav-ad')])]")))
        except (NoSuchElementException,TimeoutException):            
            print("No element found. If there is a captcha on screen\n"\
                  "Complete it manually to continue\n"\
                  "Web scraper will continue in ~15 seconds\n")
            time.sleep(15)
        else:
            break
        
    return listings
                
def is_web_element_displayed(driver,element):
    try:
        web_element_displayed = driver.find_element_by_class_name(element).is_displayed()
    except:
        web_element_displayed = False
    return web_element_displayed
    
def turn_page(driver,i):
    driver.refresh()
    time.sleep(2)
    while True:
        try:
            WebDriverWait(driver,10).until(e_c.element_to_be_clickable((By.LINK_TEXT,str(i)))).click()
        except (TimeoutException):
             print("No element found. If there is a captcha on screen\n"\
                  "Complete it manually to continue\n"\
                  "Web scraper will continue in ~15 seconds\n")
        else:
            time.sleep(2)
            break

def navigate_facts_features(driver,element):
    time.sleep(5)
    while True:
        try:          
            WebDriverWait(driver,10).until(e_c.element_to_be_clickable((By.LINK_TEXT,'Facts and features'))).click()
        except (NoSuchElementException,TimeoutException):             
            print("\n\nCAPTCHA!\n"\
              "Manually complete the captcha requirements.\n"\
              "Once that's done, if the program was in the middle of scraping \n"\
              "(and is still running), it should resume scraping after ~15 seconds.")
            print('\nThis is the current url: {}\n'.format(driver.current_url))
            time.sleep(15)
    
        else:
            time.sleep(3)
            house = get_basic_info(driver)
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
            parking = get_parking(driver)
            second_lot = get_secondary_lot(driver)
            prop = get_property_details(driver)
            construction = get_construction(driver)
            
            
            super_dict = {**url,**house,
                          **bed_bath,**kitchen,
                          **family_room,**dining_room,
                          **living_room,**basement,
                          **flooring,**heat,
                          **cool,**appliances,
                          **interior,**parking,
                          **second_lot,**prop,
                          **construction}
            
            return super_dict
        
def get_url(driver):
    return {"url":driver.current_url}

def get_basic_info(driver):
    common_path = "//div[@class = 'ds-home-details-chip']"
    extra_path = "//div[@class='ds-home-facts-and-features reso-facts-features sheety-facts-features']"
    
    price = common_path+"//span[contains(text(),'$')]"
    address = common_path+"//h1[@id='ds-chip-property-address']/span"
    neighborhood = common_path+"//h1[@id='ds-chip-property-address']/span[2]"
    
    bldg = "//span[contains(text(),'Type')]/../span[2]"
    year = extra_path+"//span[contains(text(),'Year built')]/../span[2]"
    lot = extra_path+"//span[contains(text(),'Lot')]/../span[2]"
    int_lot = "(//div[@class = 'ds-bed-bath-living-area-header'])[last()]//span[text()='sqft']/../span[1]"
    
    features = [price,address,neighborhood,bldg,year,lot,int_lot]
    
    return parse_html(driver,features,['SalePrice','Address','Neighborhood','Type','YearBlt','LotSize','int_lot'])
        
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
    
    return parse_html(driver,features,['flooring_desc'])

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

def get_parking(driver):
    common_path = "//h6[contains(text(),'Parking')]"
    
    spaces = common_path+"/..//span[contains(text(),'Total spaces')]"
    parking_feature = common_path+"/..//span[contains(text(),'Parking features')]"
    garage_spaces = common_path+"]/..//span[contains(text(),'Garage spaces:')]"
    covered_spaces = common_path+"/..//span[contains(text(),'Covered spaces:')]"
    
    features = [spaces,parking_feature,garage_spaces,covered_spaces]
    
    return parse_html(driver,features,['Total_spaces','Parking_features','Garage_spaces','Covered_spaces'])

def get_secondary_lot(driver):
    common_path = "//h6[contains(text(),'Lot')]"
    
    secondary_size = common_path+"/..//span[contains(text(),'Lot size:')]"
    lot_feature = common_path+"/..//span[contains(text(),'Lot features:')]"
    
    features = [secondary_size,lot_feature]
    
    return parse_html(driver,features,['Lot_size2','Lot_features'])

def get_property_details(driver):
    common_path = "//h6[contains(text(),'Property')]"
    zoning_common_path = "//h6[contains(text(),'Other property information')]"
    
    prop_levels = common_path+"/..//span[contains(text(),'Levels:')]"
    patio_porch = common_path+"/..//span[contains(text(),'Patio and porch details:')]"
    zoning = zoning_common_path+"/..//span[contains(text(),'Zoning:')]"
    
    features = [prop_levels,patio_porch,zoning]
    
    return parse_html(driver,features,['Property_levels','patio/porch_feature','Zoning'])

def get_construction(driver):
    style_common_path = "//h6[contains(text(),'Type and style')]"
    material_common_path = "//h6[contains(text(),'Material information')]"
    condition_common_path = "//h6[contains(text(),'Condition')]"
    
    arch = style_common_path+"/..//span[contains(text(),'Architectural style:')]"
    sub_type = style_common_path+"/..//span[contains(text(),'Property subType:')]"
    construction_mat = material_common_path+"/..//span[contains(text(),'Construction materials:')]"
    foundation = material_common_path+"/..//span[contains(text(),'Foundation:')]"
    prop_condition = condition_common_path+"/..//span[contains(text(),'Property condition:')]"
    new_construction = condition_common_path+"/..//span[contains(text(),'New construction:')]"
    
    features = [arch,sub_type,construction_mat,foundation,prop_condition,new_construction]
    
    return parse_html(driver,features,['Structure_style','Property_SubType','Construction_material','Foundation','Property_condition','New_construction'])
    
def parse_html(driver,features_paths,feature_names):
    col_names = dict.fromkeys(feature_names)
    
    for idx,element in enumerate(features_paths):
        try:
            search_xpath = driver.find_element_by_xpath(element)
        except (NoSuchElementException,ValueError):
            col_names[feature_names[idx]] = np.nan
        else:
            elementHTML = search_xpath.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML,'html.parser')
            
            if ':' in elementSoup.get_text():
                col_names[feature_names[idx]] = elementSoup.get_text().split(":")[1]
            elif '$' in elementSoup.get_text():
                col_names[feature_names[idx]] = elementSoup.get_text().split("$")[1]
            else:
                col_names[feature_names[idx]] = elementSoup.get_text()
    
    return col_names

    