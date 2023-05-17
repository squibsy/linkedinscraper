from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.parse as urlparse
from urllib.parse import urlencode
import pytest
import time
import json
import csv
import random 
from scraperconfig import * # set the variables linkedin_username linkedin_password searchterm 

# set the path to the Chrome webdriver
chrome_driver_path = "/path/to/chromedriver"



# set the name of the output CSV file
output_file = searchterm + ".csv"

# start the Chrome webdriver
chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.maximize_window()

# navigate to LinkedIn and log in
driver.get("https://www.linkedin.com/")
time.sleep(5)

login_field = driver.find_element("name", "session_key")
login_field.send_keys(linkedin_username)

password_field = driver.find_element("name", "session_password")
password_field.send_keys(linkedin_password)
password_field.send_keys(Keys.RETURN)
time.sleep(10)

# Enter search term
mydiv = driver.find_element(By.CSS_SELECTOR, "#global-nav-typeahead")
mydiv.click()
driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input").send_keys(searchterm)
driver.find_element(By.CSS_SELECTOR, ".search-global-typeahead__input").send_keys(Keys.ENTER)
driver.implicitly_wait(20)

# get the search results
more_results = driver.find_element(By.LINK_TEXT, "See all people results").click()

# create a CSV file and write the headers
with open(output_file, "w",  encoding="utf-8", newline="") as f:
    count = 1
    writer = csv.writer(f)
    charcount = writer.writerow(["Name", "LinkedIn Profile", "Position", "Company"])
    while count<50:
        try:
            search_results = driver.find_elements(By.CSS_SELECTOR, '.entity-result__item')
        except:
            continue #skip the page and tray again
        # for each search result, write the name, LinkedIn profile, position, business
        for result in search_results:
            try:
                person = result.find_element(By.CSS_SELECTOR, '.entity-result__title-text')
                name = person.find_element("xpath", './/a/span/span').text
                profile = person.find_element("xpath", './/a').get_attribute("href")
                positionCompany = result.find_element(By.CSS_SELECTOR, '.entity-result__primary-subtitle').text
                position, company = positionCompany.split(" at ")
            except:
                continue #skip the record

            # write the data to the CSV file
            charcount =  writer.writerow([name, profile, position, company])
        #retrieve the url and set the page number in the url query string
        get_url = driver.current_url
        parsed_url = urlparse.urlparse(get_url)
        dict_result = urlparse.parse_qs(parsed_url.query)
        count += 1
        dict_result["page"]=count
        newquery = urlencode(dict_result)
        parsed_url = parsed_url._replace(query=newquery)
        get_url = urlparse.urlunparse(parsed_url)
        get_url = get_url.replace("%27%5D","")
        get_url = get_url.replace("%5D%27","")
        get_url = get_url.replace("%5B%27","")
        driver.get(get_url)
        time.sleep(random.randint(2, 9))
# close the browser
driver.quit()