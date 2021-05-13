import requests
import re

domain = "https://www.dytt89.com/"

resp = requests.get(domain, verify=False)  # verify=False 去掉安全验证
resp.encoding = 'gb2312'  # 指定字符集
# print(resp.text)

# 拿到ul里面的li
obj1 = re.compile(r"2021必看热片.*?<ul>(?P<ul>.*?)</ul>", re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'", re.S)
obj3 = re.compile(r'◎片　　名(?P<movie>.*?)<br />.*?'
                  r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">', re.S)


# obj2 = re.compile(r"<a href='(?P<href>.*?)'", re.S)
result1 = obj1.finditer(resp.text)
child_href_list = []
for it in result1:
    ul = it.group('ul')
    # print(ul)

    result2 = obj2.finditer(ul)
    for itt in result2:
        child_href = domain +itt.group('href').strip("/")
        child_href_list.append(child_href)
        # print(child_href)

 # 提取子页面内容
for href in child_href_list:
    child_resp = requests.get(href, verify=False)
    child_resp.encoding = 'gb2312'
    result3 = obj3.search(child_resp.text)
    print(result3.group("movie"))
    print(result3.group("download"))
    # break  # 测试用
resp.close()