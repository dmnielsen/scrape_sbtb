import sys,os
import calendar as cal
import datetime as dt
from bs4 import BeautifulSoup
import re
import sqlite3 as sql

def define_month_abbr():
    # global define dict to convert month_abbr to integer with leading zero
    global months
    months = {v: k for k,v in enumerate(cal.month_abbr)}
    
def format_date(d):
    # convert Mon DD, YYYY to YYYY-MM-DD
    d = d.replace(',','').split()
    d[0] = months[d[0]]
    d = [int(x) for x in d]
    d_format = dt.date(d[2],d[0],d[1])
    return d_format 

if __name__ == '__main__':
    
    define_month_abbr()
    
    linkfile = open('entrylinks.txt','w')
    
    conn = sql.connect('sbtb.db',timeout=10)
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Reviews (\
    Id INTEGER UNIQUE, Review_date TEXT, Link TEXT, Reviewer TEXT,\
    Grade TEXT, Title TEXT, Author TEXT, Pub_year INTEGER, Genres TEXT);''')
    
    start = 0
    cur.execute('SELECT max(id) FROM Reviews')
    
    try:
        row = cur.fetchone()
        if row[0] is not None:
            start = row[0]
            print(row)
    except:
        start = 0
        row = None
    
    #baseurl = 'http://smartbitchestrashybooks.com/review/book/page/'
    baseurl = os.getcwd()+'/testfiles/review_index'  # for testing
    
    
    for i in range(0,2): #60 total pages: 27 June 2016

        fn = baseurl+str(i)+'.html'  # for testing
        fhand = open(fn)  # for testing
    
        #fn = baseurl+str(i)+'/'
        #r = requests.get(fn)
    
        soup = BeautifulSoup(fhand,'lxml')
        
        fhand.close() # for testing
    
        for entry in soup.find_all('header',{'class':'entry-header book'}):
            start += 1
            
            book = entry.find('h1',{'class':'entry-title'})
            link = book.a.get('href')
            
            meta_info = entry.p.text
            x = re.findall('· ([A-Za-z]+ [0-9,]+ [0-9]+) .+ ·',meta_info)
            date = format_date(x[0])
            
            cur.execute('INSERT INTO Reviews (id,Review_date,link)\
            VALUES (?, ?, ?)',(start,date,link))
            
    linkfile.close()
    conn.commit()
    cur.close()