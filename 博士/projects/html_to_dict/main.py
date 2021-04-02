from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import json

def save():
    save_file = 'cvpr2020.md'
    file = open(save_file, 'w')

    urls=["https://openaccess.thecvf.com/CVPR2020?day=2020-06-16",
         "https://openaccess.thecvf.com/CVPR2020?day=2020-06-17",
         "https://openaccess.thecvf.com/CVPR2020?day=2020-06-18"]
    i = 0
    data = {}
    for url in urls:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        paper_table = soup.find("dl").find_all("dt", attrs={"class": "ptitle"})
        for content in paper_table:
            i += 1
            # if i <= 176:
            #     continue
            paper = content.find("a")
            pdf_name = paper.attrs['href'].split('/')[-1].split('.')[0]
            pdf_path = 'https://openaccess.thecvf.com/content_CVPR_2020/papers/' + pdf_name + '.pdf'
            title = paper.text
            data[title] = {}
            link = urljoin('https://openaccess.thecvf.com', paper.attrs['href'])
            paper_content = requests.get(link).text
            paper_soup = BeautifulSoup(paper_content, "lxml")
            abstract = paper_soup.find("div", attrs={"id": 'abstract'})
            data[title]['abstract'] = abstract.contents[0].replace('\n', '')
            data[title]['pdf'] = pdf_path
            string = '# {}\n{}\n{}\n'.format(title, pdf_path, data[title]['abstract'])
            print(string)
            file.write(string)
    file.close()


def load():
    return


if __name__ == '__main__':
    save()