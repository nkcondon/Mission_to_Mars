
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#driver = webdriver.Chrome(executable_path='C:/path/to/chromedriver.exe')


#driver = webdriver.Chrome(ChromeDriverManager().install())
#executable_path ={'excutable_path': ChromeDriverManager().install()}
#Initiate browser, create data dictionary, end the webdriver and returned scraped data
def scrape_all():
  #Initiate headless driver for deployment
 
  browser = Browser("chrome", executable_path = "chromedriver", headless = True)


  hemisphere_image_urls = hemisphere(browser)

  news_title, news_paragraph = mars_news(browser)

  # Run all scraping functions and store results in dictionary
  data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemisphere(browser) 

  }

  # Stop webdriver and return data
  browser.quit()
  return data

# Set up Splinter()
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    #url = 'https://data-class-mars.s3.amanzonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #slide_elem = news_soup.select_one('div.list_text')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    #news_title = slide_elem.find('div', class_='content_title').get_text()

    # Use the parent element to find the paragraph text
    #news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    
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

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    #url = 'https://data-clas-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      #df = pd.read_html('https://galaxyfacts-mars.com')[0]
      df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere(browser):
  #Use a browser to visit the URL
  url = "https://marshemispheres.com/"
  browser.visit(url + "index.html")

  # 2. Create a list. 
  hemisphere_image_urls = []

  # 3. Write code to retrieve the image urls and titles for each hemisphere.
  for i in range(4):
      #create empty dictionary
      #hemispheres = {}
      browser.find_by_css('a.product-item h3')[i].click()
      #element = browser.find_link_by_text('Sample').first
      data_hemi = hemisphere_scrape(browser.html)
      data_hemi["img_url"] = url + data_hemi["img_url"]
      #img_url = element['href']
      #title = browser.find_by_css("h2.title").text
      #hemispheres["img_url"] = img_url
      #hemispheres["title"] = title
      hemisphere_image_urls.append(data_hemi)
      browser.back()
  return hemisphere_image_urls

def hemisphere_scrape(html_text):
    hemi_soup = soup(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres

if __name__ == "__main__":

    #If running as script, print scraped data
    print(scrape_all())

#browser.quit()


