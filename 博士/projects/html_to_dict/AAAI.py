from bs4 import BeautifulSoup
import requests


def main():
    save_file = 'AAAI2020.txt'
    file = open(save_file, 'w', encoding='UTF-8')
    urls = ['https://www.aaai.org/Library/AAAI/aaai20contents-issue{:02d}.php'.format(x) for x in range(1, 11)]
    i = 0
    jump = True
    for url in urls:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        papers = soup.find_all('p', attrs={"class": "left"})
        for paper in papers:
            i += 1
            if i != 264 and jump:
                continue
            else:
                jump = False
            content = paper.find_all('a')
            paper_url = content[0].attrs['href']
            title = content[0].text.replace('\n', '')
            pdf = content[1].attrs['href']
            abstract_content = requests.get(paper_url).text
            abstract_soup = BeautifulSoup(abstract_content, "lxml")
            try:
                abstract = abstract_soup.find('section', attrs={"class": "item abstract"}).find('p').text
            except:
                abstract = 'None'
            string = '{}\n{}\n{}\n'.format(title, pdf, abstract).replace('<', '-').replace('>', '-').replace('&',
                                                                                                             '-').replace(
                '\\', '')
            file.write(string)
            print(i)

if __name__ == '__main__':
    main()