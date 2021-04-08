from bs4 import BeautifulSoup
import requests
import re

def main():
    i = 0
    save_file = 'NIPS2020.txt'
    file = open(save_file, 'w', encoding='UTF-8')
    url = 'https://papers.nips.cc/paper/2020'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    papers = soup.find_all('li')
    for paper in papers:
        try:
            link = 'https://papers.nips.cc' + paper.find('a').attrs['href']
            if not 'Abstract' in link:
                continue
            i += 1
            title = paper.find('a').text
            paper_content = requests.get(link).text
            paper_soup = BeautifulSoup(paper_content, "lxml")
            abstract_content = paper_soup.find('div', attrs={"class": "container-fluid"}).find_all('p')
            abstracts = [x.text.replace("  ", "").replace("\n", "") for x in abstract_content]
            abstract = max(abstracts, key=len)
            pdf = paper_soup.find('meta', attrs={"content": re.compile(r'pdf')}).attrs['content']
            string = '{}\n{}\n{}\n'.format(title, pdf, abstract).replace('<', '-').replace('>', '-').replace('&', '-').replace('\\', '')
            file.write(string)
            print(i)
        except:
            pass


if __name__ == '__main__':
    main()