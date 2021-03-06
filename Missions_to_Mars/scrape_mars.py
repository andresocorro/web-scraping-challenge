# Import Dependencies

from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pprint import pprint
import time
    
def init_browser():    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# Empty Dictionary to store output

mars_page = {}

# run Browser



# Nasa Mars News
def scrape_news():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('li',class_='slide')
    results = results[0]

    news_title = results.find('div', class_ = "content_title").text
    news_p = results.find('div', class_='article_teaser_body').text

# Add to Dict
    mars_page["news_title"] = news_title
    mars_page["news_p"] = news_p

    return mars_page
    browser.quit()

# Featured Image Search

def scrape_img():
    browser = init_browser()

#Grab Featured Image
    basic_url = 'https://www.jpl.nasa.gov/'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(3)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)

    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    results_img = img_soup.find_all('img', class_ = "fancybox-image")
   

    img = results_img[0]['src']
    featured_image_url = basic_url + img

    mars_page["featured_image_url"] = featured_image_url

    browser.quit()
    return mars_page

# Scrape with Pandas
def scrape_facts():
    browser = init_browser()
    table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(table_url)

    main_table = tables[0]
    html_table = main_table.to_html()

    mars_page["html_table"] = html_table
    return mars_page

# Mars Hemispheres

def scrape_hemisphere():
    browser = init_browser()

    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    time.sleep(2)
    hemis_html = browser.html
    hemis_soup = BeautifulSoup(hemis_html, 'html.parser')
    results = hemis_soup.find_all('div', class_ = "item")


# Create Empty list and starter usl
    hemisphere_image_urls = []
    starter_url = 'https://astrogeology.usgs.gov'

    for i in results:
        #Find title from results
        titles = i.h3.text
        #visit url per hemisphere listed and parse through
        the_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(starter_url + the_url)
        time.sleep(3)
        hemis2_html = browser.html
        hemis2_soup = BeautifulSoup(hemis2_html, 'html.parser')
        #find the images within the page and save the full url
        img_url2 = hemis2_soup.find('img', class_= "wide-image")['src']
        img_url = starter_url + img_url2
        # format as requested with dictionary
        hemisphere_image_urls.append({"title": titles, "img_url": img_url})

    mars_page["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    return mars_page
 