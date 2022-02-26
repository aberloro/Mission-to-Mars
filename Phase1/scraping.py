#Import Pandas, splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set executable path for splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#################################################
# Scrape Latest Article from redplanetscience.com
#################################################

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page in case page is slow to load
#search tag 'div' and attribute 'list_text'
browser.is_element_present_by_css('div.list_text', wait_time=1)

#Set up HTML Parser
html = browser.html
news_soup = soup(html, 'html.parser')

#variable to set 'parent element' within which we look for first <div/> tag with class .list_text
slide_elem = news_soup.select_one('div.list_text')

#begin scraping for article title to .find() data in the slide variable set earlier
#.find() returns FIRST instance vs .findall(_)
slide_elem.find('div', class_='content_title')

#just the text from above, no HTML
#Use the parent element to find the first 'anchor' tag and save it as `news_title`
#with .get_text
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

##############################3333333###################
# Scrape Latest Featured Image from spaceimages-mars.com
###############################3333333##################

# tell splinter to visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button, located at index [1] (the second button)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url with img tag, class 'fancybox-image' and .get('src')
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL variable with f string
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

######################################3333###########
# Scrape Mars v Earth table from galaxyfacts-mars.com
#####################################3333############

#find the first table ([0]) from this website and read_html into a pandas DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]

#assign columns
df.columns=['description', 'Mars', 'Earth']

#set_index to the descrption inplace
df.set_index('description', inplace=True)
df

#convert dataframe back to html
df.to_html()

#end automated session
browser.quit()


