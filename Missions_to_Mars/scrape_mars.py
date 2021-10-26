import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = news(browser)
    hemisphere_image_urls = hemispheres(browser)

    # dictionary to store scraped data
    mars_data = {
        'title':title,
        'paragraph':paragraph,
        'feat_img':feat_img(browser),
        'mars_facts':mars_facts(),
        'hemispheres':hemisphere_image_urls
    }

    browser.quit()

    return mars_data

def news(browser):
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    
    html = browser.html
    soup = bs(html,'html.parser')

    try:
        news_title = soup.find_all('div', class_='content_title')[0].text

        news_paragraph = soup.find_all('div', class_='rollover_description_inner')[0].text
        
        return news_title, news_paragraph

    except:
        return None, None
     
    return news_title, news_paragraph

def feat_img(browser):

    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(browser.html, 'html.parser')

    try:
        img_path = jpl_soup.find('img', class_='headerimage fade-in').get('src')
    except AttributeError:
        return None

    feat_img_url = jpl_url + img_path

def mars_facts():
    try:
        mars_df = pd.read_html('https://galaxyfacts-mars.com/')[0]

    except BaseException:
        return None

    mars_df = mars_df.drop(columns=[2],index=[0]).rename(columns={0:'Measure',1:'Mars'}).set_index('Measure')

    return mars_df.to_html(classes='table table-striped')


def hemispheres(browser):
    hemi_base_url='https://astrogeology.usgs.gov'
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_hemispheres = soup.find('div',class_='collapsible results')
    mars_items = mars_hemispheres.find_all('div',class_='item')
    hemi_image_urls = []

    for item in mars_items:
        
        hem = item.find('div',class_='description')
        title = hem.h3.text

        hem_url = hem.a['href']
        browser.visit(hemi_base_url+hem_url)
        html = browser.html
        soup = bs(html,'html.parser')
        image_src = soup.find('li').a['href']

        hem_dict = {
            'title':title,
            'image_url':image_src
        }
        
        hemi_image_urls.append(hem_dict)

if __name__=='__main__':
    print(scrape())