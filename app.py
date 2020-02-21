import requests
import time
from pymongo import MongoClient
client = MongoClient()
db = client.chinaAir
cities = ["Shanghai",
          "Beijing",
          "Chongqing",
          "Tianjin",
          "Guangzhou",
          "Shenzhen ",
          "Chengdu",
          "Nanjing",
          "Wuhan",
          "@1396",
          "Hangzhou",
          "Dongguan",
          "Foshan",
          "Shenyang",
          "Harbin",
          "Qingdao",
          "Dalian",
          "Jinan",
          "Zhengzhou",
          "Changsha",
          "Kunming",
          "Changchun",
          "Ürümqi",
          "Shantou",
          "Hefei",
          "Shijiazhuang",
          "Ningbo ",
          "Taiyuan",
          "Nanning",
          "Xiamen",
          "Fuzhou",
          "Changzhou",
          "Wenzhou",
          "Nanchang",
          "Tangshan",
          "Guiyang",
          "Wuxi",
          "Lanzhou",
          "Zhongshan",
          "Handan",
          "Huai'an",
          "Weifang",
          "Zibo",
          "Shaoxing",
          "Yantai",
          "Huizhou",
          "Luoyang",
          "Nantong",
          "Baotou",
          "Liuzhou"]
token = "4a13562e652883c84057938d69935a29ac7caf45"
def queryCity(city):
  url = "https://api.waqi.info/feed/" + city + "/?token=" + token
  res = requests.get(url, {}).json()
  print("Inserting city data: " + str(res["data"]["city"]["name"]) + " at time " + res["data"]["time"]["s"])
  db.air.insert_one(res["data"])

def queryCities():
  for city in cities:
    try:
      queryCity(city)
    except Exception as e:
      print("Err in city " + city + str(e))

def queryPeriodic(seconds):
  while(True):
    queryCities()
    time.sleep(seconds)

queryPeriodic(3600)
