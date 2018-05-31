from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

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
def parse_page(problems, html_name):
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
        link = urljoin('https://leetcode-cn.com/', link_suffix) + '/description/'  # 题目名称（英文）
        p.link = link
        problems.append([p.num, p.title_cn, p.link, p.difficulty, p.acp, p.title_en])

    print("一共有 {} 题".format(len(problems)))
    for p in problems:
        print(p)


def write_to_csv(problems, problems_file_name):
    with open(problems_file_name, 'w', encoding='utf-8') as fw:
        writer = csv.writer(fw)
        for row in problems:
            writer.writerow(row)


if __name__ == '__main__':
    # download_page_of_all_link(executable_path, leetcode_url_cn, select_visible_text_cn, html_name_cn)
    # problems_cn = []
    # parse_page(problems_cn, html_name_cn)
    # write_to_csv(problems_cn, problems_file_name_cn)

    download_page_of_all_link(executable_path, leetcode_url_en, select_visible_text_en, html_name_en)
    problems_en = []
    parse_page(problems_en, html_name_en)
    write_to_csv(problems_en, problems_file_name_en)
