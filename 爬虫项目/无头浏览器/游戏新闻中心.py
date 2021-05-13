import requests
import re
import xlwt

if __name__ == '__main__':
    url = 'http://interface.17173.com/content/list.jsonp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    title_list = []
    news_list = []
    num = 0
    for count in range(1,101):
        params = {
            'callback': 'jQuery11110028782863316979768_1618835665951',
            'categoryIds': '10019,10152,10161',
            'pageSize': '21',
            'pageNo': str(count),
            '_': '161883566595'+str(count+1)
        }
        page_text = requests.get(url=url, headers=headers, params=params).text
        ex_title = '"title":"(.*?)",'
        titles = re.findall(ex_title, page_text, re.S)
        for title in titles:
            title_list.append(title)
            num += 1
            print(title)
        ex_content = '"content":"(.*?)",'
        contents = re.findall(ex_content, page_text, re.S)
        for content in contents:
            news_list.append(content)

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('科技', cell_overwrite_ok=True)
    row0 = ["id", "title", "content", "channelName"]
    print("本地开始爬虫")
    fp = open('./游戏.txt', 'w', encoding='utf-8')
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    for i in range(num):
        title = title_list[i]
        content = news_list[i]
        fp.write('游戏'+'   '+title + '   ' + content + '\n')
    print('结束爬虫')
    fp.close()

