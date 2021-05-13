import requests
import re
import csv

url = "https://movie.douban.com/top250"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
}
resp = requests.get(url, headers=headers)
page_content = resp.text

obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp.*?'
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                 r'<span>(?P<num>.*?)人评价</span>',re.S)
result = obj.finditer(page_content)
f = open("data2.csv",mode="w")
csvwriter = csv.writer(f)
for i in result:
    # print(i.group("name"))
    # print(i.group("score"))
    # print(i.group("num")+"人评价")
    # print(i.group("year").strip())
    dic = i.groupdict()
    dic['year']=dic['year'].strip()
    csvwriter.writerow(dic.values())

f.close()
resp.close()