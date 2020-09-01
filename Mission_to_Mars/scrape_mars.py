# Declare Dependencies 
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    # Choose the executable path to driver 
    executable_path = {"executable_path": "/Users/keana/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}
    
def scrape_news():
    browser = init_browser()
## Mars News

    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    articles = soup.find_all("div", class_='list_text')

    news_date = articles[0].find('div', class_='list_date').text
    news_title = articles[0].find("div", class_="content_title").text
    news_p = articles[0].find('div', class_='article_teaser_body').text

    # Dictionary entry from news
    mars_data['news_date'] = news_date
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

def scrape_images():
    browser = init_browser()
## Mars Images

    # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)
    time.sleep(1)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    featured_image_url
    
    # Dictionary entry from images
    mars_data['featured_image_url'] = featured_image_url  

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

def scrape_facts():
    browser = init_browser()
## Mars Facts

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(1)

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns 
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code
    mars_df.to_html('mars_facts.html')

    # Dictionary entry from facts
    mars_data['mars_facts'] = mars_facts  

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

def scrape_hemispheres():
    browser = init_browser() 
## Mars Hemispheres

    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(1)

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

    # Dictionary entry from facts
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls  

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data