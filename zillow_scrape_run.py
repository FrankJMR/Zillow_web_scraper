# -*- coding: utf-8 -*-
import real_estate_scraper as zillow
from alive_progress import alive_bar
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"
driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

#initial webpage
zillow.navigate(driver,site)
page = 8

#iterate through pages
for i in range(1,page):
    print('page #{}'.format(i))
    listing = zillow.current_page_listings(driver)
    """with alive_bar(len(listing),bar='smooth',theme='ascii') as bar:"""
    #iterate through listings on current page
    for j in range(len(listing)):
        print('listing # {}'.format(j+1))
        zillow.__pause__(3)
        
        #click through listings 
        try:
            listing[j].click()
        except (StaleElementReferenceException):
            continue
        else:
            #pause to allow content to load
            zillow.__pause__(1)
            
            listing_data = zillow.navigate_facts_features(driver)
            #captcha check, still needs manual input to continue
            zillow.captcha_check(driver)
            driver.back()
            print(listing_data)
        """#time.sleep(0.002)
        #bar()"""

    zillow.turn_page(driver,i+1)
    zillow.__pause__(1)

    




