import sys,os
import calendar as cal
from bs4 import BeautifulSoup
import requests

def define_month_abbr():
    # define dictionary to convert month_abbr to integer with leading zero
    global months = {v: str(k).zfill(2) for k,v in enumerate(cal.month_abbr)}
    

if __name__ == '__main__':
    
    linkfile = open('entrylinks.txt','w')
    
    baseurl = 'http://smartbitchestrashybooks.com/review/book/page/'
    
    for i in range(0,61): #60 total pages: 27 June 2016
    
        r = requests.get(baseurl+str(i)+'/')
    
        soup = BeautifulSoup(r.text,lxml)
    
        for entry in soup.find_all('h1',{'class':'entry-title'}):
            link = entry.find('a').get('href')
            linkfile.write(link+'\n')
            
    linkfile.close()