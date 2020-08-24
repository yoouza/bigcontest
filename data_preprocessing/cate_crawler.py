import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# 드라이버 오픈
path = r'C:\Users\dlagh\Downloads\chromedriver_win32\chromedriver'
driver = webdriver.Chrome(path)
driver.get("https://www.11st.co.kr/main")

driver.find_element_by_xpath('//*[@id="wrapBody"]/div[2]/div[1]/div/div[5]/button').click()
driver.implicitly_wait(3)
big_cate_list = []
for i in range(1, 13):
    big_cate_list.append(driver.find_element_by_xpath('//*[@id="gnbCategory"]/div/div[1]/div[2]/nav/ul/li[{}]'.format(i)))

# print(len(big_cate_list))

# 카테고리 list 생성
data_list = []
for cate in big_cate_list:
    # data_dict = {}
    big_cate_name = cate.find_element_by_tag_name('a').text
    big_cate_id = json.loads(cate.find_element_by_tag_name('a').get_attribute('data-log-body'))['content_no']

    mid_cate_name_list = cate.find_element_by_tag_name('dl').find_elements_by_tag_name('dd')

    for idx, mid_cate in enumerate(mid_cate_name_list):
        data_dict = {}
        # mid_link = mid_cate.find_element_by_tag_name('a').get_attribute('href')
        mid_cate_name = mid_cate.find_element_by_tag_name('a').text
        print(mid_cate_name)
        mid_cate_id = json.loads(mid_cate.find_element_by_tag_name('a').get_attribute('data-log-body'))['content_no']

        data_dict['big_cate'] = big_cate_name
        data_dict['big_cate_id'] = big_cate_id
        data_dict['mid_cate'] = mid_cate_name
        data_dict['mid_cate_id'] = mid_cate_id

        data_list.append(data_dict)

        print(data_dict)

df = pd.DataFrame(data_list)
print(df.head(50))
print(df.tail(50))

# json 파일화
df_file = df.to_json('category_table.json')

