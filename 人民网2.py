import chardet
from selenium import webdriver
from time import sleep, time
from lxml import etree
import requests
bro = webdriver.Chrome(executable_path='/Users/wyw/Desktop/软件杯/爬虫/爬虫课件/第七章：动态加载数据处理/chromedriver')
url = 'http://search.people.cn/'
bro.get(url)

#标签定位
search_input = bro.find_element_by_css_selector("input")
#标签交互
search_input.send_keys('军事')


# #执行一组js程序
# bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# sleep(2)
#点击搜索按钮
browser = bro.find_element_by_class_name('sh-btn').click()
sleep(5)
# browser.window_handles()

# title = bro.find_element_by_xpath('//*[@id="rmw-search"]/div/div[2]/div[2]/div[1]/div/ul/li[1]/div/div[1]/a').text
# info = bro.find_element_by_xpath('//*[@id="rmw-search"]/div/div[2]/div[2]/div[1]/div/ul/li[1]/div/div[2]').text
#
# dic = {}
# dic['书名'] = title
# dic['其他信息'] = info.split('\n')
#
# print(dic)



num=1


while num:
    page_text = bro.page_source
    tree = etree.HTML(page_text)



    ol_li_list = tree.xpath('//*[@id="rmw-search"]/div/div[2]/div[2]/div[1]/div/ul/li')
    all_news_title = []
    all_news_title_links = []
    all_news_content = []
    news_list = []
    #解析到了热门城市的城市名称
    for li in ol_li_list:
        hot_news_name = li.xpath('./div/div[1]/a//text()')
        hot_city_name_link = li.xpath('./div/div[1]/a/@href')[0]
        all_news_title.append(hot_news_name)
        all_news_title_links.append(hot_city_name_link)

        bro.get(hot_city_name_link)
        page_text_sec = bro.page_source
        print(page_text_sec)
        tree = etree.HTML(page_text_sec)
        p_list = bro.find_elements_by_tag_name('p')

        name_li_list = []
        # for i in p_list:
        #     name = i.innerHTML('p')
        #     print(name)
        #     name_li_list.append(name)
        #
        #
        # # 设置字符串变量来存储一条新闻
        # string = ''
        # for text in name_li_list:
        #     # 替换空白字符
        #     text = text.replace('\n\t', '')
        #     text = text.replace(' ', '')
        #     if text is '':
        #         continue
        #     string = string + text
        #     print(string)
        # news_list.append(string)
        #
        # sleep(10)

    print(all_news_title)
    print(all_news_title_links)
    browser = bro.find_element_by_class_name('page-next').click()
    sleep(10)
    num = num -1
    print(num)
print("finish")
# #参数的封装
# for page in range(1,6):
#     page = str(page)
#     data = {
#             "endTime": 0,
#             "hasContent": "true",
#             "hasTitle": "true",
#             "isFuzzy": "true",
#             "key": "军事",
#             "limit": 10,
#             "page": page,
#             "sortType": 2,
#             "startTime": 0,
#             "type": 0,
#     }
#     json_ids = requests.post(url=url, headers=headers, data=data).json()
#     for dic in json_ids['list']:
#         id_list.append(dic['ID'])

bro.quit()

