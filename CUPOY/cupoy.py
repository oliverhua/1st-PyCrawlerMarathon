import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
url = "https://www.cupoy.com/newsfeed/topstory"
browser = webdriver.Chrome()
SCROLL_PAUSE_TIME = 3

browser.get(url) 
news
def get_title():
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    all_news = soup.find_all("div", attrs={'class':'sc-eEieub sc-iuDHTM ibJqYc'})
    for news in all_news:
        title = news.a["title"]
        print(title)
        news_url = news.a["href"]

time.sleep(3)
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # browser.execute_script("window.scrollTo(0, 100000000000);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    print("new_height:",new_height)
    last_height = new_height
    get_title()
    
print("last_height:",last_height)