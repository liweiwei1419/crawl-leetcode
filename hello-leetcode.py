from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import csv
import re
import os

import pandas as pd
import re

pd.set_option('display.width', 1000)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行

# 配置
# executable_path = '/Users/liwei/geckodriver'
executable_path = "C:\\Users\\Administrator\\Desktop\\crawl-leetcode\\geckodriver-v0.19.1-win64\\geckodriver.exe"

leetcode_url_en = 'https://leetcode.com/problemset/all/'
leetcode_url_cn = 'https://leetcode-cn.com/problemset/all/'
question_select_en = ""  # question-app > div > div:nth-child(2) > div.question-list-base > div.table-responsive.question-list-table > table > tbody.reactable-pagination > tr > td > span.row-selector > select""
question_select_cn = "#question-app > div > div:nth-child(2) > div.question-list-base > div.table-responsive.question-list-table > table > tbody.reactable-pagination > tr > td > span > select"
select_visible_text_en = "all"
select_visible_text_cn = "全部"

html_name_en = "leetcode-en.html"
html_name_cn = "leetcode-cn.html"

problems_file_name_en = "problems-en.csv"
problems_file_name_cn = "problems-cn.csv"

url_prefix_en = "https://leetcode.com/"
url_prefix_cn = "https://leetcode-cn.com/"

template_file_name = "leetcode-solution-template.md"
dir_name = 'out'


# 第 1 步：下载中文网页
def download_page_of_all_link(executable_path, url, select_visible_text, html_name):
    driver = webdriver.Firefox(executable_path=executable_path)
    driver.get(url=url)  # 让浏览器访问网页
    driver.maximize_window()

    s1 = Select(driver.find_element_by_css_selector(question_select_cn))
    s1.select_by_visible_text(select_visible_text)
    content = driver.page_source
    with open(html_name, 'w', encoding='utf-8') as fw:
        fw.write(content)
    driver.close()


class Problem:
    num = ""
    difficulty = ""
    acp = ""
    title_cn = ""
    title_en = ""
    link = ""


# 解析中文网页
def parse_page(problems, html_name, url_prefix):
    with open(html_name, 'r', encoding='utf-8') as fr:
        html = fr.read();

    soup = BeautifulSoup(html, 'lxml')
    lines = soup.select(".reactable-data tr")
    for line in lines:
        p = Problem()
        p.num = line.select("td")[1].text  # 序号
        p.acp = line.select("td")[4].text  # 通过率
        p.difficulty = line.select("td")[5].text  # 题目难度
        p.title_cn = line.select("td")[2].text.strip()  # 题目名称（中文）
        p.title_en = line.select("td")[2].attrs['value']  # 题目名称（英文）
        link_suffix = line.select("td")[2].select("div a")[0].attrs['href']
        link = urljoin(url_prefix, link_suffix) + '/description/'  # 题目名称（英文）
        p.link = link
        problems.append([p.num, p.title_cn, p.link, p.difficulty, p.acp, p.title_en])

    print("一共有 {} 题".format(len(problems)))
    for p in problems:
        print(p)


def write_to_csv(problems, problems_file_name):
    with open(problems_file_name, 'w', encoding='utf-8', newline='') as fw:
        writer = csv.writer(fw)
        for row in problems:
            writer.writerow(row)


def download_csv():
    download_page_of_all_link(executable_path, leetcode_url_en, select_visible_text_en, html_name_en)
    problems_en = []
    parse_page(problems_en, html_name_en, url_prefix_en)
    write_to_csv(problems_en, problems_file_name_en)

    download_page_of_all_link(executable_path, leetcode_url_cn, select_visible_text_cn, html_name_cn)
    problems_cn = []
    parse_page(problems_cn, html_name_cn, url_prefix_cn)
    write_to_csv(problems_cn, problems_file_name_cn)
    print('第 1 步：爬取 LeetCode 中英文网站完成！')


# 根据文件名创建文件（模板内容固定）
def touch_one_solution_file(file_name):
    with open(template_file_name, 'r', encoding='utf-8') as fr:
        content = fr.read()
    file_name = "out" + os.sep + file_name
    with open(file_name, 'w', encoding='utf-8') as fw:
        fw.write(content)


# 读 LeetCode 问题列表，并且创建文件名
def read_problems_list():
    with open("problems-en.csv", 'r', encoding="utf-8") as fr:
        csv_reader = csv.reader(fr)
        for row in csv_reader:
            number = "{:0>4d}".format(int(row[0]))
            title = re.search("/problems/(.*?)/description/", row[2]).group(1)
            file_name = "leetcode-" + number + "-" + title + ".md"
            touch_one_solution_file(file_name)


def mkdir():
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def merge_en_cn_problems():
    dataframe_en = pd.read_csv(problems_file_name_en, header=None)
    dataframe_en.columns = ["num", "title_en", "link_en", "difficulty", "acp", "title_en2"]

    dataframe_cn = pd.read_csv(problems_file_name_cn, header=None)
    dataframe_cn.columns = ["num", "title_cn", "link_cn", "difficulty", "acp", "title_en"]

    result = pd.merge(dataframe_en, dataframe_cn, on='num')
    result.to_csv("leet-code-en-cn-merge.csv", index=None)
    print("第 2 步：中英文 csv 文件合并完成！")


template_content = ""


def read_from_template():
    global template_content
    with open('leetcode-solution-template.md', 'r', encoding='utf-8') as fr:
        template_content = fr.read()


def transform_template(row):
    template = template_content
    template = re.sub('\$title\$', row['title_en_x'], template)
    template = re.sub('\$difficulty\$', row['difficulty_y'], template)
    template = re.sub('\$link-en\$', row['link_en'], template)
    template = re.sub('\$title-en\$', str(row['num']) + '. ' + row['title_en_x'], template)
    template = re.sub('\$link-cn\$', row['link_cn'], template)
    template = re.sub('\$title-cn\$', str(row['num']) + '. ' + row['title_cn'], template)
    return template


def read_template_and_replace():
    read_from_template()
    dataframe = pd.read_csv('leet-code-en-cn-merge.csv', index_col=None)
    for index, row in dataframe.iterrows():
        content = transform_template(row)
        number = "{:0>4d}".format((row['num']))
        title = re.search("/problems/(.*?)/description/", row['link_en']).group(1)
        # 文件全名，创建它
        file_name = "leetcode-" + number + "-" + title + ".md"
        file_name = "out" + os.sep + file_name
        with open(file_name, 'w', encoding='utf-8') as fw:
            fw.write(content)
    print("第 3 步：读取模板并且替换完成！")


if __name__ == '__main__':
    # download_csv()
    # merge_en_cn_problems()
    read_template_and_replace()
