# Zillow webscraper (Selenium and bs4)

## Description
I am building a zillow web scraper using selenium and beautiful soup for a future data-science project. This will output information to a spreadsheet in the near future. ​This scraper will go through and click on each listing for a specified number of pages for the following information:

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

## Usage
When using this I recommend copy and pasting the link with your specified query instructions to determine in what location this scraper should extract data from.
> site = "https://www.zillow.com/homes/Cook-County,-IL_rb/"

Copy and paste the location of where your chromedriver is installed such as:
>driver = zillow.create_driver("C:\Program Files (x86)\chromedriver.exe")

Note that this will not output to a spreadsheet quite yet, I'm tinkering with making this more consistent with scraping data and managing exceptions in failed cases. Outputting to a spreadsheet will be a fairly easily implementation with pandas.
Also note that Captchas are frequent (yes, very annoying), with the current code it fails to pause searching for web elements on page and fails. This will be fixed but manual input will still be needed to complete captchas. 
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
