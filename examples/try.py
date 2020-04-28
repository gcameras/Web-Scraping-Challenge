import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape_info():
    browser = init_browser()
    # Visit visitcostarica.herokuapp.com
    url = "https://visitcostarica.herokuapp.com/"
    browser.visit(url)
    # time.sleep(1)
    browser.is_element_present_by_id('weather', wait_time=1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")
    # Get the average temps
    # @TODO: YOUR CODE HERE!
    weather_element = soup.find("div", id="weather")
    # Get the min avg temp
    # @TODO: YOUR CODE HERE!
    min_max_temp = weather_element.find("p").find_all("strong")
    min_temp = min_max_temp[0].text.split("°")[0]
    # Get the max avg temp
    # @TODO: YOUR CODE HERE!
    max_temp = min_max_temp[1].text.split("°")[0]
    # BONUS: Find the src for the sloth image
    # @TODO: YOUR CODE HERE!
    animals_element = soup.find_all("img", class_="animals")
    sloth_img = animals_element[1]['src']
    sloth_img = os.path.join(url, sloth_img)
    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": float(min_temp),
        "max_temp": float(max_temp)
    }
    # Quite the browser after scraping
    browser.quit()
    # Return results
    return costa_data
if __name__ == "__main__":
    data = scrape_info()
    print(data)