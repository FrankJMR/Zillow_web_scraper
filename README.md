# Zillow webscraper (Selenium and bs4)

## Description
I am building a zillow web scraper using selenium and beautiful soup for a future data-science project.This scraper will go through and click on each listing for a specified number of pages for the following information:

1. Basic house info
  * Sale Price
  * Address
  * Neighborhood
  * Building type
  * Year built
  * Lot size
2. Bed/Bathroom info
  * No. of bedrooms
  * No. of bathrooms
  * Full bathrooms
  * 1/2 Bathrooms
2. Kitchen info
  * Level
  * Area
  * Misc features
3. Family room info
  * Description
  * Area
  * Misc features
4. Dining room info
  * Level
  * Area
  * Misc features
5. Living room info
  * Description
  * Level
  * Area
6. House flooring info
  * Features
7. Heating systems
  * System
8. Cooling systems
  * System
9. Appliances
  * Appliances included

10. Interior 
   * Door  details
   * Interior details
  
11. Parking
   * Spaces
   * Parking features
   * Garage spaces
   * Covered spaces
   
12. Lot details
   * Lot size 2
   * Lot features
   
13. Property details
   * Property Levels
   * Patio/Porch features
   * Zoning
   
14. Construction 
   * Architectural style
   * Property sub-type
   * Construction material
   * Foundation
   * Property Condition
   * New Construction (Yes/No)

## Usage
When using this I recommend copy and pasting the link with your specified query instructions to determine in what location this scraper should extract data from.
I reccomend doing so by County, but it should work for different boundaries 
> site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"

Copy and paste the location of where your chromedriver is installed such as:
>driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

Please note that this scraper is significantly slower than traditional web-scrapers. This is for one of two reasons.
1. Captchas are frequent (yes, very annoying) and require manual input.
2. This script uses XPATH as selectors because zillow is java-script heavy and the DOM is quite complex.

## Software dependencies 
Made in Python 3.7.4
* Selenium
   * Web chrome driver
* Bs4 (Beautiful soup)
* Pandas
* Numpy
* alive_progress


## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/
