# -*- coding: utf-8 -*-
import real_estate_scraper as zillow
from alive_progress import alive_bar
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
import pandas as pd
import time
#search
site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"
driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

#initial webpage
zillow.navigate(driver,site)
page = 20

df_list = []

#iterate pages
for i in range(page):
    listing = zillow.current_page_listings(driver)    
    print('page #{}'.format(i+1))
    print('\n\n\n number of listings: ',len(listing))
    #iterate through listings on current page
    for j in range(len(listing)):
        time.sleep(2)
        print('listing # {}'.format(j+1))
        
        try:
            #click through listings 
            listing[j].click()
        except (StaleElementReferenceException):
            print('stale element reference')
        else:
            time.sleep(3)
            listing_data = zillow.navigate_facts_features(driver)
            print(listing_data)
            
            driver.back()
            
            listing_info_df = pd.DataFrame([listing_data])
            df_list.append(listing_info_df)
            
            listing = zillow.current_page_listings(driver)
        
    zillow.turn_page(driver,i+2)
    
final_df = pd.concat(df_list)

print(final_df)




"""with alive_bar(len(listing),bar='smooth',theme='ascii') as bar:"""
"""#time.sleep(0.002)
        #bar()"""