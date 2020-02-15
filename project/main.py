import requests
import csv
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

url = "https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv"

cnt = 1
error_cnt = 0
dic = []
demo_dic = []
address_dic = {}
demo_address_dic = {}
tmp_dic = {}
# print(rows[0])
def convert_string(full):
    s = full
    s = s.replace("Ｆ","F")
    s = s.replace("Ｃ","C")
    s = s.replace("－","-")
    s = s.replace("（","(")
    s = s.replace("）",")")
    s = s.replace("：",":")
    s = s.replace("０","0")
    s = s.replace("１","1")
    s = s.replace("２","2")
    s = s.replace("３","3")
    s = s.replace("４","4")
    s = s.replace("５","5")
    s = s.replace("６","6")
    s = s.replace("７","7")
    s = s.replace("８","8")
    s = s.replace("９","9")
    return s
    
def get_coor(addr):
    global cnt
    cnt += 1
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(executable_path='chromedriver',options=options)
    browser.get("http://www.map.com.tw/")
    search = browser.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    browser.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click() 
    time.sleep(2)
    iframe = browser.find_elements_by_tag_name("iframe")[1]
    browser.switch_to.frame(iframe)
    cor_btn = browser.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    cor_btn.click()
    coor = browser.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    cor = coor.text.strip().split(" ")
    lat = cor[-1].split("：")[-1]
    log = cor[0].split("：")[-1]
    browser.quit()
    return (lat, log)

threads = []
# for i in range(5):
#   threads.append(threading.Thread(target = job, args = (i,)))
#   threads[i].start()

# def job(url):

def update_mask():
    global demo_address_dic
    r = requests.get(url)
    csv_data = csv.reader(r.text.splitlines(), delimiter=',')
    next(csv_data)
    rows = list(csv_data)
    for row in rows:
        row[2] = convert_string(row[2])
        if not row[2] in address_dic:
                address_dic[row[2]] = get_coor(row[2]) #return tuple
                print("Find New", row[2], address_dic[row[2]])
                if cnt % 5 == 0:
                    print("[cnt]"+str(cnt))
                    save_data()
        elif address_dic[row[2]][0] == 0 and address_dic[row[2]][1] == 0:
                address_dic[row[2]] = get_coor(row[2])
                print("Update", row[2], address_dic[row[2]])
                if cnt % 5 == 0:
                    print("[cnt]"+str(cnt))
                    save_data()
        if address_dic[row[2]][0] != 0 and address_dic[row[2]][1] != 0:
            # print("Good", row[2], address_dic[row[2]])
            demo_address_dic[row[2]] = address_dic[row[2]]
            dic.append({
                "id":row[0],
                "name":row[1],
                "address":row[2],
                "phone":row[3],
                "lat": address_dic[row[2]][0],
                "lng": address_dic[row[2]][1],
                "adult_count":row[4],
                "child_count": row[5],
                "updatetime": row[6]
            })
    # print(dic)

def load_data():
    with open('data.json', 'r') as json_file:
        global tmp_dic
        tmp_dic = json.load(json_file)
    with open('demo_address.json', 'r') as json_file:
        global demo_address_dic
        demo_address_dic = json.load(json_file)
    with open('address.json', 'r') as json_file:
        global address_dic
        address_dic = json.load(json_file)
    print("Data Loaded")

def save_data():
    with open('data.json', 'w', encoding="utf-8") as json_file:
        json.dump(dic, json_file, indent=4, ensure_ascii=False)
    with open('demo_address.json', 'w', encoding="utf-8") as json_file:
        json.dump(demo_address_dic, json_file, indent=4, ensure_ascii=False)
    with open('address.json', 'w', encoding="utf-8") as json_file:
        json.dump(address_dic, json_file, indent=4, ensure_ascii=False)
    print("Data Saved")

def get_coor_google(addr):
    res = requests.get("https://www.google.com.tw/maps/place/"+ addr, headers = headers)
    end1 = 0
    end2 = 0

    start1 = res.text.find("ll=", end1)
    end1 = res.text.find("\"", start1)
    ll1 = res.text[start1+3:end1].split(",")
    start2 = res.text.find("markers=", end2)
    end2 = res.text.find("&amp;", start2)
    ll2 = res.text[start2+8:end2].split("%2C")
    global error_cnt
    if len(ll1) == 2:
        error_cnt = 0
        print(ll1)
        return ll1
    elif len(ll2) == 2:
        error_cnt = 0
        print(ll2)
        return ll2
    else:
        error_cnt += 1
        return (0,0)


load_data()
ori_address_dic = len(address_dic)
ori_data_dic = len(tmp_dic)
print("address_dic:", ori_address_dic)
print("data_dic:", ori_data_dic)
update_mask()

print("ori_address_dic:", ori_address_dic)
print("ori_data_dic:", ori_data_dic)
print("address_dic:", len(address_dic))
print("data_dic:", len(dic))
# get_coor_google("新北市平溪區公園街17號1樓")

for i in address_dic.item():
    if 
save_data()