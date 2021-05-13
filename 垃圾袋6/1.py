from bs4 import BeautifulSoup
import requests
import csv
url = "http://www.xinfadi.com.cn/marketanalysis/0/list/1.shtml"
resp = requests.get(url)
f = open("菜价.csv",mode="w")
csvwrite = csv.writer(f)

page = BeautifulSoup(resp.text,"html.parser")

table = page.find("table",attrs={"class":"hq_table"})
print(table)

trs = table.find_all("tr")[1:]
for tr in trs:
    tds = tr.find_all("td")
    name = tds[0].text
    low = tds[1].text
    avg = tds[2].text
    high = tds[3].text
    gui = tds[4].text
    kind = tds[5].text
    date = tds[6].text
    csvwrite.writerow([name,low,avg,high,gui,kind,date])
    print(name,low,avg,high,gui,kind,date)
f.close()