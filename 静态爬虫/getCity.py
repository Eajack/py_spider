from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
import os
import re
import time
# https://maps.google.com/maps/api/geocode/json?latlng=22.574867,113.920188&sensor=true

# global
## 请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'HSID=AUE1PEl6ncRJ7XRCu; SSID=AwB1iOzP3d96dkOfj; APISID=H-FhId-rT7Hd79-G/A93yuoLxdMdHdAWAe; SAPISID=_bUxkTmGqfkVtCUP/AyfKuJve_yAOV33O2; SID=-ARliXAJsjfppT5yzzm7U3VfWrqmSzlR-fghP98KcxVXXHDrzwtFbmz9O3adI4MObm22kQ.; NID=109=UI2IwnxTFfMcrLUcNwcT7vhVKqV9fZn6XLcN3qXWPg4mPTQp9jxyd-WvVPe3bDTBuRwZ2XKFayGae9xcKDxi1Ao_4xB-r_PYBeQdANHyO1pDX9sV_jsQa5lqlJc5ooUMJn-SdQ_IZGSPvvEWXcblkEvd6UF8mQybdtABxfM; SIDCC=AE4kn79dnrRTGU_T881UfzAUieoCbFCWbi_EjcY_d1797bTh612snLj6siAfridXyL-c_nBs877YU1x0Rf-RhQ',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests' : '1',
    'x-chrome-uma-enabled' : '1',
    'x-client-data': 'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQjSncoBCKqiygE=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}

## 会员点标记
print("=================会员==========================")
lats = [22.947097,]
lngs = [113.45677,]
zhenshen_peopleNum = []
guangzhou_peopleNum = []
dongguan_peopleNum = []
foshan_peopleNum = []
other_peopleNum = []

for count in range(0,len(lats)):
    lat = lats[count]
    lng = logs[count]
    latlogstr = "?latlng=" + str(lat) + "," + str(lng)
    url = r"https://maps.google.com/maps/api/geocode/json" + latlogstr + r"&sensor=true"
    # print(url)

    proxies1 = { "http": "http://45.55.60.124:3128" }
    proxies2 = {"http": "http://98.191.98.146:3128"}
    if count < 500:
        proxies =proxies2
    else:
        proxies = proxies1

    request = requests.get(url,headers = headers,proxies = proxies)
    request.encoding = 'utf-8'
    html = request.text
    if ( "Shenzhen Shi" in html ):
        zhenshen_peopleNum.append(count+1)
    elif ( "Guangzhou Shi" in html ):
        guangzhou_peopleNum.append(count+1)
    elif ( "Dongguan Shi" in html ):
        dongguan_peopleNum.append(count+1)
    elif ( "Foshan Shi" in html ):
        foshan_peopleNum.append(count+1)
    else:
        other_peopleNum.append(count+1)

print("深圳",zhenshen_peopleNum)
print("广州",guangzhou_peopleNum)
print("东莞",dongguan_peopleNum)
print("佛山",foshan_peopleNum)
print("其他",other_peopleNum)
