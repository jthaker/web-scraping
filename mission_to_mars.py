#!/usr/bin/env python
# coding: utf-8


#import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import time


def init_browser(): 

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
# Scraping the NASA Mars News Site and collecting the latest News Title and Paragraph Text. Assigning text to variables for reference later.

def scrape_mars_news():
    try: 

#URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #retrieve page with requests module
    response = requests.get(url)


    # In[5]:


    #create Beautiful Soup object
    soup = bs(response.text, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# ## JPL Mars Space Images - Featured Image

# Using splinter to navigate the site and find the image url for the current Featured Mars Image and assigning the url string to a variable.



url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
time.sleep(1)
browser.visit(url_image)


from urllib.parse import urlsplit
featured_image_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(featured_image_url)



#Design an xpath selector to grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"



#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()



#get URL with BeautifulSoup
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_ = "fancybox-image")["src"]
full_url = featured_image_url + img_url
print(full_url)


# ## Mars Weather

# Visiting the Mars Weather Twitter account and scraping the latest Mars weather tweet from the page. Saving the tweet text for the weather report as a variable.


url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)



html_weather = browser.html
soup = bs(html_weather, "html.parser")
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# ## Mars Facts

# Visiting the Mars Facts webpage and using Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. Additionally, using Pandas to convert the data to a HTML table string.


url_facts = "https://space-facts.com/mars/"


table = pd.read_html(url_facts)
mars_df = table[0]
mars_df.columns = ['Description','Value']

mars_df



mars_html_table = mars_df.to_html()
mars_html_table = mars_html_table.replace("\n", "")
mars_html_table


# ## Mars Hemispheres
# 
# 
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# 
# 
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# 
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# 
# 
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# 
# 


hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)


# HTML Object
html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_hemispheres, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in items: 
    # Store title
    title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
hemisphere_image_urls

