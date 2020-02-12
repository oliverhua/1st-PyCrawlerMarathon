import requests
import csv

url = "https://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv"

dic = []
address_dic = {}
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
    r = requests.get(url)
    csv_data = csv.reader(r.text.splitlines(), delimiter=',')
    next(csv_data)
    rows = list(csv_data)
    for row in rows:
        row[2] = convert_string(row[2])
        if not row[2] in address_dic:
            print(row[2])
            address_dic[row[2]] = get_coor(row[2]) #return tuple

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
    print(dic)

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

def get_coor_google(addr):
    res = requests.get("http://"+ addr)
    end = 0
    while True:
        start = res.text.find("ll=", end)
        end = res.text.find("\"", start)
        if end - start < 25:
            break
    if end - start == 0: return (0,0)
    ll = res.text[start+3:end].split(",")
    print(ll)
    return ll

# update_mask()
get_coor("連江縣南竿鄉復興村217號")