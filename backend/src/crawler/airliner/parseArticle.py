from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re

def getAllLinksToArticle( endPos):
    output = []
    for i in range(endPos):
        html = getArticleSite('https://www.airliners.de/ticker?page='+str(i))
        for link in html.find('div',{'class':'ticker'}).find_all('a', href = re.compile('https://www.airliners.de/*')):
            if 'href' in link.attrs:
                output.append(link.attrs['href'])

def getArticleSite(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'lxml')
    except HTTPError as e:
        return 'Error!'
    except URLError as e:
        return 'Error!'

    return bs;

def mapMonth(month):
    list = {'Januar':'01','Februar':'02','März':'03','April':'04','Mai':'05', 'Juni':'06','Juli':'07','August':'08', 'September':'09', 'Oktober':'10', 'November':'11', 'Dezember':'12'}
    map = lambda x: list[x]
    return map(month)

def getDate(bs):
    try:
        date = bs.find('span', {'class':'teaser__datetime'})
    except AttributeError as e:
        print("Date not found!")
    else:
        output = ''
        for char in date:
            output += '{}'.format(char)

        #remove whitespace
        output = output.strip()

        #remove time from date, because only months can match to pax
        output = output.split(',')
        output = output.pop(0).split(' ')
        #reformat date
        output = output.pop(0).split('.').pop(0)+ '.' +mapMonth(output.pop(0))+ '.' +output.pop(0)
        return output


def getArticleHeadline(bs):
    try:
        #getting headline
        headline_temp = bs.find('h1',{'id':'article-title'})
        #if span in headline
        try:
            headline = headline_temp.span.next_sibling
        except Exception as e:
            headline = headline_temp

    except AttributeError as e:
        print("Title could not be found!")
    else:
        #cast headline to String
        output = ''
        for chars in headline:
            output += '{}'.format(chars)

        return output.strip()


def getArticleText(bs):
    try:
        #some articls have only a lead
        text = bs.find('section', {'class':'article__body'})
        #Lead of article
        lead = bs.find('p', {'class':'lead'})
    except AttributeError as e:
        print("Text could not be found!")
    else:
        #cast Text to String
        output = ''
        for chars in lead.getText():
            output += '{}'.format(chars)

        for chars in text.getText():
            output += '{}'.format(chars)

        return output.strip()
        return output

