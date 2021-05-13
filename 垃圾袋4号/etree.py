import requests
from lxml import etree
import csv

f = open("data.csv", 'w',encoding="utf-8")

csvwriter = csv.writer(f)

def down_one_page(url):

    #拿到页面源代码
    resp = requests.get(url)
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div[2]/div[1]/div[3]/div[2]")[0]
    trs = table.xpath("./p")

    for p in trs:
        txt = p.xpath("/text()")
        txt = (item.replace("\\","").replace("/", "") for item in txt)
        print(txt)
        csvwriter.writerow(txt)
    print(url,"finish")

if __name__ == '__main__':
    for i in range(1):
        down_one_page(f"https://www.163.com/news/article/G8BHUTDA0001899O.html")

