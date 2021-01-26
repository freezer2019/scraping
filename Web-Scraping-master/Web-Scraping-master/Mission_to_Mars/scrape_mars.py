#Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver

    # MAC Users:
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

    # Windows Users:
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

def scrape():
# NASA Mars News

    browser = init_browser()

    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Extract the latest News Title and Paragraph 
    news_title = browser.find_by_css('.grid_gallery.list_view .content_title a').text
    news_p = browser.find_by_css('.grid_gallery.list_view li.slide').text

# JPL Featured Space Image
# Use Splinter to navigate the following site and find the image

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)

    time.sleep(2)

# Retrieve background-image from style tag 

    browser.find_by_id('full_image').click()

    browser.click_link_by_partial_text('more info')

# Retrieve featured-image from style tag 
    featured_image = browser.find_by_css('img.main_image')['src']    

# NASA Mars Facts

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Mars Facts Table
    f_table = pd.read_html(facts_url)
    df = f_table[0] 
    mars_fact = df.to_html() 

# Mars Hemispheres

    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    browser.visit(astro_url)

    time.sleep(2)

    links = browser.find_by_css('a.product-item h3')

# Retreive all items that contain Mars hemispheres information

    hemi_img_urls = []

    for i in range(len(links)):
        hemi = {}
    
        browser.find_by_css('a.product-item h3')[i].click()
        hemi['img_url'] = browser.find_by_text('Sample')['href']
        hemi['title'] = browser.find_by_css('h2.title').text
    
        hemi_img_urls.append(hemi)
        browser.back()
    
    browser.quit()

# Store return values as a Python dictionary   
      
    mars_info = {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image': featured_image,
            'mars_fact': mars_fact,
            'hemi_img_urls': hemi_img_urls
        }
        
    return mars_info
