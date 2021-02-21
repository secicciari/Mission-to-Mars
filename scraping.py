# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_images": {hemisphere_images(browser)},
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# ## Mars Facts

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
  
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# ## Hemisphere images
def hemisphere_images(browser):
    # Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Establish links to click to get to full images
    thumbnail_1 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[1]/a/img')
    thumbnail_2 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[2]/a/img')
    thumbnail_3 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[3]/a/img')
    thumbnail_4 = browser.find_by_xpath('//*[@id="product-section"]/div[2]/div[4]/a/img')
    thumbnails = [thumbnail_1, thumbnail_2, thumbnail_3, thumbnail_4]

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Retrieve the image urls and titles for each hemisphere.
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

    # Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())