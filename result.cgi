#!/usr/bin/python3
import requests
import json
# 日本語を扱うために必要な設定 --- (*1)
import os, sys, io, cgi
sys.stdin, sys.stdout, sys.etderr =  [
  open(sys.stdin.fileno(),  'r', encoding='UTF-8'),
  open(sys.stdout.fileno(), 'w', encoding='UTF-8'),
  open(sys.stderr.fileno(), 'w', encoding='UTF-8')]

form = cgi.FieldStorage()
lat = form.getfirst('y', '')
lng = form.getfirst('x', '')
rng = form.getfirst('range', '')
#print(lat)
#print(lng)
#print("Content-type: text/html; charset=utf-8\r\n\r\n")
#print("<html><body><center><h1>result</h1></center>")

class HotpepperApi:
    form = cgi.FieldStorage()
    lat = form.getfirst('y', '')
    lng = form.getfirst('x', '')
    rng = form.getfirst('range', '')
    # APIのURL
    api = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={key}&lat={lat}&lng={lng}&range={range}&order=1&count=100&format=json"

    # コンストラクタ引数：APIキー
    def __init__(self, api_key):
        self.api_key = api_key

    # 緯度・経度を指定して最寄りの飲食店名リストを取得（とりあえず検索半径は500m固定）
    def get_shop_name_list(self, lat, lng, rng):
        url = self.api.format(key=self.api_key, lat=lat, lng=lng, range=rng)
        response = requests.get(url)        
        # jsonデータをパースする
        result_list = json.loads(response.text)["results"]["shop"]
        return [d.get("name") for d in result_list]
    
    def get_shop_address_list(self, lat, lng, rng):
        url = self.api.format(key=self.api_key, lat=lat, lng=lng, range=rng)
        response = requests.get(url)        
        # jsonデータをパースする
        result_list = json.loads(response.text)["results"]["shop"]
        return [f.get("address") for f in result_list]

myapi='c73c310b6bf87c78'

#if __name__ == '__main__': 
    # json ファイルに「keyキー」があるものとする
    # （key:APIキー）
    #f = open("HotPepperApiSetting.json", 'r')
    #json_data = json.load(f)
obj = HotpepperApi(myapi)
result1 = obj.get_shop_name_list(lat,lng,rng)
result2 = obj.get_shop_address_list(lat,lng,rng)
    #result = obj.get_shop_name_list("36.08615168010187","140.10643782658383")  
    #for i in range(len(result)):
        #print(result[i])



# ヘッダなどを出力 --- (*2)
print("Content-type: text/html; charset=utf-8\r\n\r\n")
print("<html><body><center><h1>result</h1></center>")

print("<center>")
print("<h3>"+str(len(result1))+"</h3")
print("<h3>name　　　　　　address</h3>")
print("</center>")
# パラメータの値を取得 --- (*3)
form = cgi.FieldStorage()
if ("x" in form) and ("y" in form):
    for i in range(len(result1)):
        print("<center>")
        print(result1[i]+"　　　　　　"+result2[i])
        print('<br>')
        print("</center>")
else:
    print("パラメータがありません。")
print("</center>")
print("</body></html>")