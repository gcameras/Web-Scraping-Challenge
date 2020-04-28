# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
import pandas as pd

def init_browser():
    # Set Executable Path & Initialize Chrome Browser
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # URL of page to be scraped, visit URL and set up BeautifulSoup parsing
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "lxml")

    # Find latest news title and paragraph text
    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').text
    news_p = article.find("div", class_ ="article_teaser_body").text

    # URL of page to be scraped, visit URL and set up BeautifulSoup parsing
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "lxml")

    # Navigate to the image URL by clicking the button using Splinter
    browser.click_link_by_partial_text('FULL IMAGE')

    # Parse the code to find the path and combine with base url consstruct the full image URL
    path = soup.find(class_='fancybox')['data-fancybox-href']
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + path

    # URL of page to be scraped, visit URL and set up BeautifulSoup parsing
    weather_url = 'https://twitter.com/marswxreport'
    browser.visit(weather_url)
    time.sleep(10)
    html = browser.html
    soup = bs(html, "lxml")

    # Find the Tweet in the source code
    results = soup.find('article')
    mars_results = results.find_all('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')

    # Isolate the text needed using list comprehension
    mars_weather = ""
    for item in mars_results:
        if "InSight" in item.text:
            mars_weather = item.text

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts 
    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)

    # Convert the table to a dataframe (rename columns, index to mars fact)
    mars_table = table[0]
    mars_table = mars_table.rename(columns = {0:'Mars Fact', 1:'Data'})
    mars_table.set_index('Mars Fact', inplace=True)
    mars_facts = mars_table.to_html(classes="table table-striped table-dark")

    # URL of page to be scraped, visit URL and set up BeautifulSoup parsing
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, 'lxml')

    # Find all elements containing titles and URLs
    items = soup.find_all('div', class_='item')

    # Create a list to hold information
    hemisphere_image_urls = []

    # Set main URL
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    #Loop through items
    for item in items: 
        #Exctact title
        title = item.find('h3').text
        #Find image URL
        image_url = item.find('a', class_='itemLink product-item')['href']
        #Visit image URL
        browser.visit(hemispheres_main_url + image_url)
        image_html = browser.html
        # Parse using BeautifulSoup
        soup = bs( image_html, 'lxml')
        # Locate image URL
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        #Append to list
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

    hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {
        "news_title" : news_title,
        "news_p": news_p,
        "mars_weather": mars_weather,
        "mars_facts" : mars_facts,
        "featured_image_url" : featured_image_url,
        "hemisphere_image_urls" : hemisphere_image_urls}
    print(mars_data)

    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data

if __name__ == "__main__":
    data = scrape()