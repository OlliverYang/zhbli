from bs4 import BeautifulSoup
import requests


i = 0
save_file = 'ICML2020.txt'
file = open(save_file, 'w', encoding='UTF-8')
url = 'http://proceedings.mlr.press/v119/'
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
papers = soup.find_all('div', attrs={"class":"paper"})
for paper in papers:
    i += 1
    title = paper.find('p', attrs={"class": "title"}).text
    urls = list(paper.find('p', attrs={"class": "links"}).children)
    abstract_url = urls[1].attrs['href'].replace('\n', '')
    pdf = urls[3].attrs['href'].replace('\n', '')
    abstract_content = requests.get(abstract_url).text
    abstract_soup = BeautifulSoup(abstract_content, "lxml")
    abstract = abstract_soup.find('div', attrs={"class": "abstract"}).text.replace('\n', '')
    string = '{}\n{}\n{}\n'.format(title, pdf, abstract).replace('\t', '').replace('  ', '').replace('<', '-'). \
        replace('>', '-').replace('&', '-').replace('\r', '')
    string = string.encode("ascii", "ignore")
    string = string.decode()
    file.write(string)
    file.flush()
    print(i)

