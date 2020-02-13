import requests
import csv
import json

url = "https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv"

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

def update_mask():
    global demo_address_dic
    r = requests.get(url)
    csv_data = csv.reader(r.text.splitlines(), delimiter=',')
    next(csv_data)
    rows = list(csv_data)
    for row in rows:
        row[2] = convert_string(row[2])
        
        if not row[2] in address_dic:
            print(row[2])
            address_dic[row[2]] = get_coor_google(row[2]) #return tuple
        # elif address_dic[row[2]][0] == 0 and address_dic[row[2]][1] == 0:
        #     address_dic[row[2]] = get_coor_google(row[2])
        #     print("Find New", address_dic[row[2]])

        if address_dic[row[2]][0] != 0 and address_dic[row[2]][1]!=0:
            demo_address_dic[row[2]] = address_dic[row[2]]
            demo_address_dic.append({
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

    print(dic)
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

def save_data():
    # with open('data.json', 'w') as json_file:
    #     json.dump(dic, json_file)
    with open('demo_address.json', 'w') as json_file:
        json.dump(demo_address_dic, json_file)
    # with open('address.json', 'w') as json_file:
    #     json.dump(address_dic, json_file)

def get_coor_google(addr):
    res = requests.get("https://www.google.com.tw/maps/place/"+ addr)
    end1 = 0
    end2 = 0

    start1 = res.text.find("ll=", end1)
    end1 = res.text.find("\"", start1)
    ll1 = res.text[start1+3:end1].split(",")
    start2 = res.text.find("markers=", end2)
    end2 = res.text.find("&amp;", start2)
    ll2 = res.text[start2+8:end2].split("%2C")

    if len(ll1) == 2:
        print(ll1)
        return ll1
    elif len(ll2) == 2:
        print(ll2)
        return ll2
    else:
        return (0,0)
    
load_data()
update_mask()
save_data()
# get_coor_google("新北市平溪區公園街17號1樓")



def get_coor(addr):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    params = {
        "search_class": "Landmark",
        "searchkey": "D43A19151569F32A449B7EDCB8555165B68B5F95",
        "fun": "funB",
        "SearchWord":addr
    }
    res = requests.get("http://api.map.com.tw/net/GraphicsXY.aspx", params=params, headers=headers)
    print(res.text)
    # return ll
