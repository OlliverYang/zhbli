from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def main():
    i = 0
    save_file = 'iclr2021.txt'
    file = open(save_file, 'w', encoding='UTF-8')
    urls = ['oral.html', 'spotlight.html', 'poster.html']
    for url in urls:
        input = open(url, 'r', encoding='UTF-8').read()
        soup = BeautifulSoup(input, "lxml")
        paper_table = soup.find_all('li', attrs={"class": "note"})
        for content in paper_table:
            i += 1
            title = content.find_all("a")[0].text.replace("  ", "").replace("\n", "")
            paper = content.find_all("span", attrs={"class": "note-content-value"})
            abstracts = [x.text.replace("  ", "").replace("\n", "") for x in paper]
            abstract = max(abstracts, key=len)
            id = content.attrs['data-id']
            link = 'https://openreview.net/pdf?id=' + id
            string = '{}\n{}\n{}\n'.format(title, link, abstract).replace('<', '-').replace('>', '-').replace('&', '-')
            file.write(string)
            print(i)


if __name__ == '__main__':
    main()