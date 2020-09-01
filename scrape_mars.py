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
    # mars_facts_url = "https://space-facts.com/mars/"
    # browser.visit(mars_facts_url)
    # time.sleep(1)
    # mars_facts_soup = bs(mars_facts_url,"html.parser")
    # time.sleep(1)
    # mars_table = mars_facts_soup.find("table",class_="tablepress tablepress-id-mars")
    # column1 = mars_table.find_all("td",class_="column-1")
    # column2 = mars_table.find_all("td",class_="column-2")
    # planet_profile = []
    # recorded = []
    # for x in column1:
    #     planet_profile.append(x.text.strip())
    # for y in column2:
    #     recorded.append(y.text.strip())
    # mars_facts_table = pd.DataFrame({
    #     "planet_profile": planet_profile,
    #     "recorded": recorded
    # })
    # mars_facts_table_html = mars_facts_table.to_html(header=False, index=Flase)


    # Dont code under this line
    browser.quit()
    return{
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        # "planet_profile": planet_profile,
        # "recorded": recorded,
        # "fact_table": mars_facts_table_html,
    }
    # Do Images for Mars