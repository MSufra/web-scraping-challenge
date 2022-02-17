#import libraries
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #scrape mars news
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html,'html.parser')

    #find the first title
    news_title = soup.find('div', class_="content_title").text
    
    #find paragraph text
    news_p = soup.find('div',class_="article_teaser_body").text

    #
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    imgs = browser.find_by_tag('img')

    for img in imgs:
        if img.has_class('headerimage fade-in')== True:
            featured_image_url = img['src']
            break

    #scrape mars facts with pandas
    url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(url)
    
    mars_df = table[0]
    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df.set_index(['Mars - Earth Comparison'])
    mars_df = mars_df.iloc[1: , :]
    table_html = mars_df.to_html()
    
    #scrape hemipsheres
    url = 'https://marshemispheres.com'
    browser.visit(url)

    html = browser.html
    
    img_soup = bs(html, 'html.parser')

    imgs = img_soup.find_all('div', class_='description')

    hemispheres = {'img_url':[],'title':[]}

    for img in imgs:
        hemispheres['title'].append(img.a.h3.text)
    
        browser.visit('https://marshemispheres.com/'+img.a['href'])
        img_url = browser.find_by_text('Sample')
        hemispheres['img_url'].append(img_url['href'])
        browser.visit(url)

    browser.quit()

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_image_url,
        'table_html':table_html,
        'hemispheres':hemispheres
        
    }
    
    return mars_data


