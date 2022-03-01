# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#################################################
# Scrape Latest Article from redplanetscience.com
#################################################

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

##############################3333333###################
# Scrape Latest Featured Image from spaceimages-mars.com
###############################3333333##################

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

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

#####################################################
# Scrape Mars v Earth table from galaxyfacts-mars.com
#####################################################

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#######################################################
# D1: Scrape High Res Mars Hemisphere Images and Titles
#######################################################

def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    hemi_img_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #initiate a list to hold the pages we need to navigate to
    page_list = []

    #create parent element 
    product_list = hemi_img_soup.select('div.item')

    #add url to page_list for items found in parent element
    for item in product_list:
        try:
            page_url = item.find('a')['href']
            page_list.append(page_url)
        except AttributeError:
            return None

    #loop through each page that holds hemisphere jpgs and title
    for hemisphere in page_list:
        #visit the page
        browser.visit(f'{url}{hemisphere}')
        hemi_html = browser.html
        hemi_soup = soup(hemi_html, 'html.parser')
        
        try:
            #find jpg urls
            jpg = hemi_soup.select('div.downloads') 
            for each in jpg:
                jpg_url = each.find('a')['href']

            #find titles
            titles = hemi_soup.select('h2.title')
            for title in titles:
                hemi_title = title.text
        except AttributeError:
            return None, None

        #add jpg url and title to list of dictionaries
        hemisphere_image_urls.append({"title" : hemi_title, "img_url" : f'{url}{jpg_url}'})

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

