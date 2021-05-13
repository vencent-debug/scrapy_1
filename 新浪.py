from selenium import webdriver
from time import sleep
bro = webdriver.Chrome(executable_path='/Users/wyw/Desktop/软件杯/爬虫/爬虫课件/第七章：动态加载数据处理/chromedriver')
url = 'https://news.sina.com.cn/'
bro.get(url)

#标签定位
search_input = bro.find_element_by_class_name('cheadSeaKey')
#标签交互
search_input.send_keys('军事')


# #执行一组js程序
# bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
# sleep(2)
#点击搜索按钮
btn = bro.find_element_by_class_name('cheadSeaSmt').click()



bro.quit()

