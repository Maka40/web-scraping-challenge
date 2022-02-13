import pymongo
import pandas as pd
from bs4 import BeautifulSoup
import selenium
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    

def scrape():

    browser = init_browser()
    mars_data = {}

    # NASA Mars News
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    mars_soup = BeautifulSoup(news_html, "html.parser")
    latest_header = mars_soup.find("div", class_ = "content_title").text.strip()
    latest_p = mars_soup.find("div", class_ = "article_teaser_body").text.strip()
    return latest_header, latest_p

    # Space Images
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, "html.parser")
    src = image_soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = image_url + src
    return featured_image_url

    # Mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    print(mars_facts)
    mars_facts.columns = ["Properties", "Mars", "Earth"]
    mars_facts.reset_index(drop=True, inplace=True)
    mars_facts
    
    #Mars Hemispheres
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    hemisphere_image_urls = []
    
    #Cerberus Hemispheres
    hemi_url = ("https://marshemispheres.com/")
    query = "cerberus.html"
    response = requests.get(hemi_url + query)
    soup = BeautifulSoup(response.text, 'html.parser')
    cerberus = soup.find_all('div', class_="wide-image-wrapper")
    
    for image in cerberus:
        pic = image.find('img', class_='wide-image')['src']
    cerberus_title = soup.find('h2', class_='title').text.strip()
    cerberus_hemisphere = {"Title": cerberus_title, "url": hemi_url + pic}
    hemisphere_image_urls.append(cerberus_hemisphere)
    
    
    # Schiaparelli Hemisphere
    hemi_url = ("https://marshemispheres.com/")
    query = "schiaparelli.html"
    response = requests.get(hemi_url + query)
    soup = BeautifulSoup(response.text, 'html.parser')
    schiaparelli = soup.find_all('div', class_="wide-image-wrapper")
    
    for image in schiaparelli:
        pic = image.find('img', class_='wide-image')['src']
    schiaparelli_title = soup.find('h2', class_='title').text.strip()
    schiaparelli_hemisphere = {"Title": schiaparelli_title, "url": hemi_url + pic}
    hemisphere_image_urls.append(schiaparelli_hemisphere)
    
    
    # Syrtis Hemisphere
    hemi_url = ("https://marshemispheres.com/")
    query = "syrtis.html"
    response = requests.get(hemi_url + query)
    soup = BeautifulSoup(response.text, 'html.parser')
    syrtis = soup.find_all('div', class_="wide-image-wrapper")
    
    for image in syrtis:
        pic = image.find('img', class_='wide-image')['src']
    syrtis_title = soup.find('h2', class_='title').text.strip()
    syrtis_hemisphere = {"Title": syrtis_title, "url": hemi_url + pic}
    hemisphere_image_urls.append(syrtis_hemisphere)
    
    
    # Valles Marineris Hemisphere
    hemi_url = "https://marshemispheres.com/"
    query = "valles.html"
    response = requests.get(hemi_url + query)
    soup = BeautifulSoup(response.text, 'html.parser')
    valles = soup.find_all('div', class_="wide-image-wrapper")
    
    for image in valles:
        pic = image.find('img', class_='wide-image')['src']
    valles_title = soup.find('h2', class_='title').text.strip()
    valles_hemisphere = {"Title": valles_title, "url": hemi_url + pic}
    hemisphere_image_urls.append(valles_hemisphere)
    
    browser.quit()


    # Return results
    mars_data ={
        'news_title' : latest_header,
        'summary': latest_p,
        'featured_image': feature_url,
        'featured_image_title': featured_image_title,
        'fact_table': mars_facts,
        'hemisphere_image_urls': hemisphere_image_urls,
        'news_url': news_url,
        'image_url': image_url,
        'facts_url': facts_url,
        'hemisphere_url': hemi_url,
        }
    collection.insert(mars_data)
	#mars_collection["hemisphere_image"] = hemisphere_image_urls
    
    return mars_data
