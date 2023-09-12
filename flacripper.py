# Standard Libraries
import sys
import os
import argparse
from pathlib import Path
import re
import time


import urllib.request
import json
import urllib

# Web automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# SELENIUM CONFIGURATION 
# chrome_options = Options()
#chrome_options.add_argument("--headless") 

service = Service()
options = webdriver.ChromeOptions()
# comment this line to view the automation
#options.add_argument("--headless") 



# SOURCE 
source = "https://tuberipper.cc/36/save/flac"

# INSTANTIATE AND LOGIN
driver = webdriver.Chrome(service=service, options=options)



# Validating if the the command-line argument is indeed a url with regex
def validate_url(url):


    if re.findall(r"https://you.u.be/[A-Za-z0-9]+", url):

        return True
    
    else:
        return False


# This part of the code is lifted from Stackoverflow, USER - porto, https://stackoverflow.com/questions/1216029/get-title-from-youtube-videos
def fetch_details(url):

    stripped = url.split('/')
    VideoID = stripped[-1]


    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        #pprint.pprint(data)
        

        return data['title']



    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--url")


    args = parser.parse_args()
    validation = validate_url(args.url)


    # Automation Loop
    if validation:

        # wait = WebDriverWait(driver, 10)
        print('Initiating Download Sequence..')
        print(f'- {fetch_details(args.url)}')
        # Navigate to a webpage
        driver.get(source)

        # Wait for the password input field to be visible
        url_field = driver.find_element(By.XPATH,'''//*[@id="videoUrl"]''')
        url_field.send_keys(args.url)

        # Search button
        time.sleep(1.5) 
        driver.find_element(By.XPATH, '''//*[@id="videoBtn"]''').click()

        # audio_list
        wait = WebDriverWait(driver, 10)
        audio_list = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="output"]/div[3]/div[1]/button')))
        audio_list.click()

        flac_option = wait.until(EC.visibility_of_element_located((By.XPATH, '''//*[@id="output"]/div[3]/div[1]/ul/li[11]/a''')))
        flac_option.click()        
        

        print('Waiting for the response...')
        # to observe changes
        time.sleep(40)

        print('flac Downloaded.')
        


    else:
        raise "url error!"



   

# https://youtu.be/yblfMrUeiP4
