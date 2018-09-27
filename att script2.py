import urllib2 as urll
import bs4 as bs
import re
import time
import csv
from multiprocessing import Pool as ThreadPool
import codecs



def get_pages(url):
    req = urll.Request(url,headers={'User-Agent':'Magic Browser'})
    sauce = urll.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    titles = soup.find('table',class_='listing')
    links = titles.find_all('a')
    sources = []
    for link in links:
        src = link.get('href')
        sources.append('http://members.calbar.ca.gov'+src)
    return sources

def parser(url):
    try:
        name = []
        num = []
        name_pat = re.compile(r'[a-zA-Z \s.]+')
        num_pat = re.compile(r'#[0-9]+')
        req = urll.Request(url, headers={'User-Agent':'Magic Browser'})
        sauce = urll.urlopen(req).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        headers = soup.find_all('h3')
        header = headers[1].text
        name_match = name_pat.finditer(header)
        num_match = num_pat.finditer(header)
        for match in name_match:
            name.append(match.group(0))
        for match in num_match:
            num.append(match.group(0))

        with codecs.open(r'Files/attorneys2.csv','a',encoding='utf-8') as f:
            fieldnames = ['Name','Block Number','Profile Url']
            thewriter = csv.DictWriter(f,fieldnames)
            thewriter.writerow({'Name': name[0], 'Block Number': num[0],'Profile Url':url})

    except Exception as e:
        print str(e)


def main():
    with open(r'Files/attorneys2.csv', 'w+') as f:
        fieldnames = ['Name','Block Number','Profile Url']
        thewriter = csv.DictWriter(f,fieldnames)
        thewriter.writeheader()
    print 'Running..............'
    begin = time.time()
    pages = get_pages('http://members.calbar.ca.gov/search/ls_results.aspx?county=All+Counties&specialty=08')
    pool = ThreadPool(4)
    results = pool.map(parser, pages)
    pool.close()
    pool.join()
    print 'Time taken-----',time.time() - begin,'seconds -----------'

if __name__ == '__main__':
    main()
