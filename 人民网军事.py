from lxml import etree
import requests
import xlwt
import chardet


if __name__ == "__main__":
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    url = "http://military.people.com.cn/GB/367540/index%d.html"
    title_list = []
    news_list = []
    num = 0
    for pagenum in range(1, 11):
        new_url = format(url%pagenum)
        #print(new_url)

        res = requests.get(url=new_url,headers=head)
        res.encoding = chardet.detect(res.content)['encoding']
        #print(res.text)
        tree = etree.HTML(res.text)
        ul_list = tree.xpath('/html/body/div[6]/div[1]/div[2]/ul')
        for ul in ul_list:
            li_list = ul.xpath('./li')
            for li in li_list:
                title = li.xpath('./a/text()')[0]
                title_url = 'http://military.people.com.cn' + li.xpath('./a/@href')[0]
                title_list.append(title)
                num += 1
                #print(title,title_url)
                new_res = requests.get(url=title_url,headers=head)
                new_res.encoding = chardet.detect(new_res.content)['encoding']
                tree = etree.HTML(new_res.text)
                new_text = tree.xpath('/html/body/div[5]/div[1]/div[2]/p/text() | //*[@id="rwb_zw"]/p/text()')
                #设置字符串变量来存储一条新闻
                string = ''
                for text in new_text:
                    # 替换空白字符
                    text = text.replace('\n\t', '')
                    text = text.replace(' ', '')
                    if text is '':
                        continue
                    string = string + text
                    #print(string)
                news_list.append(string)

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('军事', cell_overwrite_ok=True)
    row0 = ["title", "content", "channelName"]
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    for i in range(num):
        print("第%d条" %i)
        sheet.write(i+1, 0, title_list[i])
        sheet.write(i+1, 1, news_list[i])
        sheet.write(i+1, 2, '5')
    book.save('.\\人民网军事7.xls')
