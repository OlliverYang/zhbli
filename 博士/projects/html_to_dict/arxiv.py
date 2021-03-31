from bs4 import BeautifulSoup
import requests
import datetime


def save(dates):
    paper_id = 1
    for date in dates:
        page = 1
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


def get_dates(start, end):
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    data_list = list()
    while datestart <= dateend:
        data_list.append(datestart.strftime('%Y-%m-%d'))
        datestart += datetime.timedelta(days=1)
    return data_list


def main():
    start_date = '2021-03-24'
    end_date = '2021-03-31'
    dates = get_dates(start_date, end_date)
    save(dates)


if __name__ == '__main__':
    main()
