# -*- coding: utf-8 -*-
import real_estate_scraper as zillow
from alive_progress import alive_bar
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"
driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

#initial webpage
zillow.navigate(driver,site)
page = 3

properties_list = []

#iterate pages
for i in range(page):
    
    listing = zillow.current_page_listings(driver)    
    print('page #{}'.format(i+1))

    #iterate through listings on current page
    for j in range(len(listing)):
        print('listing # {}'.format(j+1))
        
        try:
            #click webelement listings 
            listing[j].click()
        except (StaleElementReferenceException):
            print('stale element reference')
        else:
            listing_data = zillow.navigate_facts_features(driver)
            print(listing_data)
            #close listing page
            zillow.close_listing(driver)
            #Enter data into DataFrame
            property_df = pd.DataFrame([listing_data])
            properties_list.append(property_df)
            #refresh webelements in list
            listing = zillow.current_page_listings(driver)
            
    listing.clear()  
    zillow.turn_page(driver,i+2)
    
final_df = pd.concat(properties_list)
final_df = final_df.reset_index(drop = True)
final_df.to_csv('house-listings-page'+str(page)+'.csv')
"""with alive_bar(len(listing),bar='smooth',theme='ascii') as bar:"""
"""#time.sleep(0.002)
        #bar()"""