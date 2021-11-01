#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as Soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt


def mars_news(browser):
    # visit the mars nasa news site
    url = "https://redplanetscience.com/"
    browser.visit(url)
    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # calling Browser instance: browser from cell 2 and calling its html subclass then saving that string to html var
    html = browser.html
    news_soup = Soup(html, 'html.parser')

    try:
        # sets first <div class='list_text'> to slide_elem
        slide_elem = news_soup.select_one('div.list_text')

        # title in ^<div /> set to news_title, paragraph set to news_p
        news_title = slide_elem.find('div', class_='content_title').text
        news_p = slide_elem.find('div', class_='article_teaser_body').text
    
    except AttributeError:
        return None, None
    
    # returning the title and paragraph for the news article in that order
    return news_title, news_p

def featured_image(browser):
    # ## image scraper
    #new url for the new scrape
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # click the full size button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # soup the new page
    html = browser.html
    img_soup = Soup(html, 'html.parser')

    # making the new url for the full size image
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
    img_url = url + '/' + img_url_rel

    return img_url

def mars_facts():
    # ## mars table
    # making the dataframe that holds the table from the new website
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # converting the df table to html, quits scraper
    return df.to_html().replace("dataframe", "table")

def mars_imgs(browser):
    #Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # processing the browser.html
    hemi_html = Soup(browser.html, "html.parser")

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for div in hemi_html.select("div.description"):
        page_with_link = (url + str(div.a["href"]))
        browser.visit(page_with_link)
        image_page = Soup(browser.html, "html.parser")
        temp_dict = {"title" : div.a.h3.text,
                     "img_url": url + str(image_page.find("a", text="Sample")["href"])}
        hemisphere_image_urls.append(temp_dict)

    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

def scrape_all():
    # initiate headless scrape
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # variable holders for output of functions
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "mars_images": mars_imgs(browser),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

if __name__ == '__main__':
    print(scrape_all())
