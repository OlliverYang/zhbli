from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import html2text


def main():
    i = 0
    save_file = 'ECCV2020.txt'
    file = open(save_file, 'w', encoding='UTF-8')
    url = 'ECCV2020.html'
    input = open(url, 'r', encoding='UTF-8').read()
    soup = BeautifulSoup(input, "lxml")
    paper_table = soup.find_all('dt', attrs={"class": "ptitle"})
    pdfs = soup.find_all('a', text='pdf')
    for content, pdf in zip(paper_table, pdfs):
        i += 1
        pdf = pdf.attrs['href']
        if 'eccv_2020' not in pdf:
            break
        title = content.text.replace('\n', '')
        link = content.find("a").attrs['href']
        paper_content = requests.get(link).text
        paper_soup = BeautifulSoup(paper_content, "html5lib")
        abstract = paper_soup.find('div', attrs={"id": "abstract"}).text.replace('\n', '')
        string = '{}\n{}\n{}\n'.format(title, pdf, abstract).replace('<', '-').replace('>', '-').replace('&', '-')
        file.write(string)
        print(i)



if __name__ == '__main__':
    main()