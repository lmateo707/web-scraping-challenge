from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # nasa website
    mars_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_url)
    time.sleep(2)
    html_mars_site = browser.html
    

    # scraoe page into Soup
    soup = bs(html_mars_site,"html.parser")
    

    # Find the latest news title and headline text in soup
    news_title = soup.find_all("div",class_="content_title")[1].text
    news_p = soup.find("div",class_="article_teaser_body").text

    # Image
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_image_url_base = "https://www.jpl.nasa.gov"
    browser.visit(jpl_image_url)
    time.sleep(1)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()
    html_mars_site = browser.html
    time.sleep(1)
    soup = bs(html_mars_site,"html.parser")
    img = soup.find("img",class_="main_image")['src']
    featured_image_url = jpl_image_url_base + img


    # Mars Facts



    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    facts_df = mars_facts[0]

    facts_df.columns = ['Planet Profile','Recorded']
    mars_facts_table_html = facts_df.to_html(index=False, classes="table table-striped")



    #Mars Hemisphere Image

    hemisphere_image_urls = []
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_base_url = "https://astrogeology.usgs.gov"

    browser.visit(mars_hemisphere_url)
    time.sleep(1)
    html_hemispheres = browser.html
    time.sleep(1)
    hemisphere_soup = bs(html_hemispheres, 'html.parser')
    time.sleep(1)
    items = hemisphere_soup.find_all('div', class_='item')
    time.sleep(1)

    for x in items:
        title = x.find("h3").text
        time.sleep(1)
        
        image_url = x.find('a', class_='itemLink product-item')["href"]
        time.sleep(1)

        
        browser.visit(hemisphere_base_url + image_url)
        time.sleep(1)
        
        image_url_html = browser.html
        time.sleep(1)
        
        hemisphere_soup = bs(image_url_html,"html.parser")
        time.sleep(1)
        
        hem_image_url = hemisphere_base_url + hemisphere_soup.find("img",class_="wide-image")["src"]
        time.sleep(1)
        
        hemisphere_image_urls.append({"title":title,"img_url":hem_image_url})
        time.sleep(1)




    # Dont code under this line
    browser.quit()
    return{
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts_table_html": mars_facts_table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
