from bs4 import BeautifulSoup
import requests


def main():
    url = 'https://www.ijcai.org/Proceedings/2020/'
    save_file = 'IJCAI2020.txt'
    file = open(save_file, 'w', encoding='UTF-8')
    i = 0
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    papers = soup.find_all('div', attrs={"class": "paper_wrapper"})
    for paper in papers:
        i += 1
        id = '{:04d}'.format(int(paper.attrs['id'][5:]))
        if int(id) == 12:
            print('debug')
        title = paper.find('div', attrs={"class": "title"}).text
        pdf = 'https://www.ijcai.org/Proceedings/2020/{}.pdf'.format(id)
        abstract_url = 'https://www.ijcai.org/proceedings/2020/{}'.format(int(id))
        abstract_content = requests.get(abstract_url).text
        abstract_soup = BeautifulSoup(abstract_content, 'lxml')
        abstract = abstract_soup.find('div', attrs={"class": "col-md-12"}).text.replace('\n', '').replace('\t', '').replace('  ', '').replace('\r', '')
        string = '{}\n{}\n{}\n'.format(title, pdf, abstract).\
            replace('\t', '').\
            replace('  ', '').\
            replace('<', '-').\
            replace('>', '-').\
            replace('&','-')
        string = string.encode("ascii", "ignore")
        string = string.decode()
        file.write(string)
        file.flush()
        print(i)


if __name__ == '__main__':
    main()