# -*- coding: utf-8 -*-
import real_estate_scraper as zillow
from alive_progress import alive_bar
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException
import pandas as pd

site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"
driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

#initial webpage
zillow.navigate(driver,site)
page = 20

properties_list = []

#iterate pages
for i in range(page):
    listing = zillow.current_page_listings(driver)    
    page_url = zillow.get_current_url(driver)
    with alive_bar(len(listing),bar ='smooth',theme ='ascii',title ='Page:'+str(i+1)) as bar:
        #iterate through listings on current page
        for j in range(len(listing)):
            try:
                #click webelement listings
                while True:
                    listing[j].click()
                    list_url = zillow.get_current_url(driver)
                    if page_url != list_url:
                        break
                    
            except (StaleElementReferenceException):
                print('stale element reference')
            except (NoSuchElementException):
                print('that element does not exit')
            else:
                listing_data = zillow.navigate_facts_features(driver,listing[j])            
                #close listing page
                zillow.navigate(driver,page_url)
                #Enter data into DataFrame
                property_df = pd.DataFrame([listing_data])
                properties_list.append(property_df)
                #refresh webelements in list
                listing = zillow.current_page_listings(driver)
            
                bar()
    
    listing.clear()
    if i+1 != page:
        zillow.turn_page(driver,i+2)
    
zillow.close_scraper(driver)   
final_df = pd.concat(properties_list)
final_df = final_df.reset_index(drop = True)
final_df.to_csv('house-listings-pages-'+str(page)+'.csv')