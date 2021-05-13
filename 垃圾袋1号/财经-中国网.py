#http://app.finance.china.com.cn/news/live.php?channel=财经&p=1
from lxml import etree         #Xpath解析
import requests                  #制定URL，获取网页数据
import xlwt                    #进行Excel操作
import chardet

if __name__ == "__main__":
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    url = "http://app.finance.china.com.cn/news/live.php?channel=财经&p=%d"
    title_list = []
    news_list = []
    num = 0
    for pagenum in range(1, 50):
        new_url = format(url%pagenum)
        print(new_url)
        res = requests.get(url=new_url,headers=head)
        res.encoding = chardet.detect(res.content)['encoding']
        #print(res.text)
        tree = etree.HTML(res.text)
        li_list = tree.xpath('/html/body/div[4]/div[1]/ul[1]/li')
        for li in li_list:
            no_title_url = li.xpath('./a/@href')[0]
            if no_title_url[-7:-6] == "x":
                title = li.xpath('./a[2]/text()')[0]
                title_url = li.xpath('./a[2]/@href')[0]
            else:
                title = li.xpath('./a/text()')[0]
                title_url = li.xpath('./a/@href')[0]

            title_list.append(title)
            num += 1
            new_res = requests.get(url=title_url,headers=head)
            new_res.encoding = chardet.detect(new_res.content)['encoding']
            tree = etree.HTML(new_res.text)
            new_text = tree.xpath('//*[@id="fontzoom"]/p/text()')

            #设置字符串变量来存储一条新闻
            string = ''
            for text in new_text:
                # 替换空白字符
                text = text.replace('\u3000', '')
                if text is '':
                    continue
                string = string + text
            news_list.append(string)
    # print(title_list)
    # print(news_list)

    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('财经', cell_overwrite_ok=True)
    row0 = ["id", "title", "content", "channelName"]
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    for i in range(num):
        print("第%d条" %i)
        sheet.write(i + 1, 0, i + 1)
        sheet.write(i + 1, 1, title_list[i])
        sheet.write(i + 1, 2, news_list[i])
        sheet.write(i + 1, 3, '1')
    book.save('.\\财经-中国网.xls')





