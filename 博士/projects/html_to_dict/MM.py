from bs4 import BeautifulSoup
import requests


i = 0
save_file = 'MM2020.txt'
file = open(save_file, 'w', encoding='UTF-8')
url = 'MM2020.html'
input = open(url, 'r', encoding='UTF-8').read()
soup = BeautifulSoup(input, "lxml")
papers = soup.find_all('h5', attrs={"class": "issue-item__title"})
abstracts = soup.find_all('div', attrs={"class": "issue-item__abstract truncate-text trunc-done"})
for paper, abstract_ in zip(papers, abstracts):
    i += 1
    title = paper.find('a').text.replace('\n', '')
    abstract = abstract_.find('p').text.replace('\n', '')
    abstract_url = paper.find('a').attrs['href']
    pdf = abstract_url.replace('doi', 'doi/pdf')
    string = '{}\n{}\n{}\n'.format(title, pdf, abstract).replace('\t', '').replace('  ', '').replace('<', '-'). \
        replace('>', '-').replace('&', '-').replace('\r', '')
    string = string.encode("ascii", "ignore")
    string = string.decode()
    file.write(string)
    file.flush()
    print(i)
