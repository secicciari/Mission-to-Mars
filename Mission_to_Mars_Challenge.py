# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['Description', 'Value']
df.set_index('Description', inplace=True)

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Establish links to click to get to full images
thumbnail_1 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[1]/a/img')
thumbnail_2 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[2]/a/img')
thumbnail_3 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[3]/a/img')
thumbnail_4 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[4]/a/img')

thumbnails = [thumbnail_1, thumbnail_2, thumbnail_3, thumbnail_4]

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(len(thumbnails)):
    # Establish links to click to get to full images
    thumbnail_1 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[1]/a/img')
    thumbnail_2 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[2]/a/img')
    thumbnail_3 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[3]/a/img')
    thumbnail_4 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[4]/a/img')

    thumbnails = [thumbnail_1, thumbnail_2, thumbnail_3, thumbnail_4]
    
    hemispheres_dict = {}
    
    #get to the hemisphere page
    thumbnails[i].click()
        
    # Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    #get image URL
    image_URL = hemi_soup.find('img', class_="wide-image").get('src')
    full_URL = (f'https://astrogeology.usgs.gov/{image_URL}')
    
    #get image title
    image_title = hemi_soup.find('h2', class_="title").get_text()
    
    browser.visit(url)
    
    #add values to dictionary
    hemispheres_dict['img_URL'] = full_URL
    hemispheres_dict['title'] = image_title
    
    #add dictionary to list
    hemisphere_image_urls.append(dict(hemispheres_dict))

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

