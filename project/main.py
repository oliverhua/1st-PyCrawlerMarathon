import requests
import csv
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

url = "https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv"

headers = {
    "cookie": "CONSENT=YES+GB.zh-TW+20150803-20-0; SID=tgcUAXYOR6oFj5lAvcw3O-hj0kfvOte0c-qxfuqt_BcDpQlnKtZ1mEpSsa9bMGtsw8qf0w.; __Secure-3PSID=tgcUAXYOR6oFj5lAvcw3O-hj0kfvOte0c-qxfuqt_BcDpQln-TqmLIajBloKEfasYq63kA.; HSID=Ap8eYih2aKxp_-R08; SSID=AhrL54ug2Md28NAr-; APISID=RLZidnRS24PvVrte/AdJXbcKtT-AvzK7et; SAPISID=UW7sVtpr1fUqynEX/AuKDEqqnKN-KepntB; __Secure-HSID=Ap8eYih2aKxp_-R08; __Secure-SSID=AhrL54ug2Md28NAr-; __Secure-APISID=RLZidnRS24PvVrte/AdJXbcKtT-AvzK7et; __Secure-3PAPISID=UW7sVtpr1fUqynEX/AuKDEqqnKN-KepntB; NID=198=sx71LiI-6Zr-W2lsys3539dFDp_FVvtT_C32jjAsJk-ky3ptgCfQiHm2Lrr-eeRin7yj39UGmKL3TtgGQeKa2BfQYd1WpZwA0u0cv0vvVZkHvd8rylv6gzi5GSI42Ijh62WhauX5MO7BA79HYidr2sQroKlBwUHwr2O1y9wcg6IhvGHzJPR4f-dRC_g8ADsEfRmPCTQ8e_xdLk_0o_AN77KpRDv55xQmyYU0a_dHdhKA8cEreNaxnxA36ByY2iGugr4QamAW0GFYjOY2h29zGCkAtoxfPfZ3z_zSoU-u6NxQ2HQpInKKAcqqPo7kLcDYYD_AMFadlrJCRQFwSQj0Dl6qwZQr; GOOGLE_ABUSE_EXEMPTION=ID=7a810cf3c7f11dae:TM=1581661992:C=r:IP=2001:b400:e2db:95c5:547f:29bd:43be:b272-:S=APGng0sPZnkOrkFCS14O3Rwl9tD17ritqw; 1P_JAR=2020-2-14-6",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "x-client-data": "CKm1yQEIlbbJAQijtskBCMS2yQEIqZ3KAQicoMoBCMuuygEIvLDKAQiXtcoBCO21ygEIjrrKARirpMoBGIqyygE=",
    "dnt" : "1",
    "referer": "https://www.google.com.tw/"
}
error_cnt = 0
dic = []
demo_dic = []
address_dic = {}
demo_address_dic = {}
# print(rows[0])
def convert_string(full):
    s = full
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
    browser = webdriver.Chrome(executable_path='chromedriver')
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
    browser.close()
    return (lat, log)

def update_mask():
    global demo_address_dic
    r = requests.get(url)
    csv_data = csv.reader(r.text.splitlines(), delimiter=',')
    next(csv_data)
    rows = list(csv_data)
    for row in rows:
        row[2] = convert_string(row[2])
        if error_cnt >= 100:
            return
        if not row[2] in address_dic:
            address_dic[row[2]] = get_coor(row[2]) #return tuple
            print("Find New", row[2], address_dic[row[2]])

        elif address_dic[row[2]][0] == 0 and address_dic[row[2]][1] == 0:
            address_dic[row[2]] = get_coor(row[2])
            print("Update", row[2], address_dic[row[2]])

        if address_dic[row[2]][0] != 0 and address_dic[row[2]][1]!=0:
            print("Good", row[2], address_dic[row[2]])
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
    # with open('data.json', 'r') as json_file:
    #     global dic
    #     dic = json.load(json_file)
    # with open('demo_address.json', 'r') as json_file:
    #     global demo_address_dic
    #     demo_address_dic = json.load(json_file)
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
update_mask()
save_data()
# get_coor_google("新北市平溪區公園街17號1樓")


