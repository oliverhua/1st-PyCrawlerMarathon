from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
def find_cor(addr):
    browser = webdriver.Chrome(executable_path='chromedriver')
    browser.get("http://www.map.com.tw/")

    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(1)
    iframe = browser.find_elements_by_tag_name("iframe")[1]
    browser.switch_to.frame(iframe)
    cor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    cor_btn.click()
    coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    cor = coor.text.strip().split(" ")
    lat = cor[-1].split("：")[-1]
    log = cor[0].split("：")[-1]
    browser.close()
    return (lat, log)


print(find_cor("高雄市新興區大同一路203－1號"))
