from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

def save(date):
    page = 1
    paper_id = 1
    while True:
        url = 'http://arxitics.com/browse?categories=cs.CV&published=' + date + '&abstract=true&page=' + str(page)
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml").find('ol').find_all('li', attrs={"class": "ui-skip-medium"})
        if len(soup) == 0:
            break
        for content in soup:
            title = content.find('h4').text
            abstract = content.find('p').text
            pdf = content.find('ul').find('li').find('a').attrs['href']
            print("{}\t{}\t{}\t{}\t{}".format(date, paper_id, title, abstract, pdf))
            paper_id += 1

        """结束循环"""
        page += 1


def main():
    date = '2021-03-23'
    save(date)


if __name__ == '__main__':
    main()