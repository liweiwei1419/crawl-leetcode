import csv
from itertools import islice
from bs4 import BeautifulSoup
from selenium import webdriver

executable_path = "C:\\Users\\Administrator\\Desktop\\crawl-leetcode\\geckodriver-v0.19.1-win64\\geckodriver.exe"


def batch_crawl_question_descriptions():
    with open("problems-cn.csv", 'r', encoding='utf-8') as fr:
        csv_reader = csv.reader(fr)
        for row in islice(csv_reader, 70, 140):
            # print(row[0], row[2])
            crawl_question_description(row[0], row[2])


res = []


def crawl_question_description(num, question_url):
    driver.get(question_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    question_description = soup.select(
        "#descriptionContent > div.col-md-9.question-panel > div > div.question-description__3U1T")
    res.append([num, question_description[0]])


# 该方法重复！！！
def write_to_csv(problems, problems_file_name):
    with open(problems_file_name, 'a', encoding='utf-8', newline='') as fw:
        writer = csv.writer(fw)
        for row in problems:
            writer.writerow(row)


if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path=executable_path)
    # driver = webdriver.PhantomJS(executable_path="C:\\Users\\Administrator\\Desktop\\crawl-leetcode\\phantomjs.exe")
    batch_crawl_question_descriptions()
    driver.close()
    print(res)
    problems_file_name = "question_descriptions.csv"
    write_to_csv(res, problems_file_name)
    print("end")
