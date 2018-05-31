import csv
import re
import os

template_file_name = "leetcode-solution-template.md"
dir_name = 'out'


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


if __name__ == '__main__':
    mkdir()
    read_problems_list()
