import sys,os
import re
import time
import calendar as cal
import datetime as dt
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql

# From 14 October, 2014 new format for reviews

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

    conn = sql.connect('sbtb.db',timeout=100)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Reviews (\
    Id INTEGER UNIQUE, Review_date TEXT, Link TEXT, Reviewer TEXT,
    Guest_review INTEGER, Grade TEXT, Title TEXT, Author TEXT, \
    Pub_year INTEGER, Genres TEXT, Themes TEXT);''')

    start = 0
    cur.execute('SELECT max(id) FROM Reviews;')

    # get max ID used in existing table
    try:
        row = cur.fetchone()
        if row[0] is not None:
            start = row[0]
            print('largest ID: {}'.format(row[0]))
    except:
        start = 0
        row = None

    # find newest review in table
    cur.execute('SELECT max(review_date), link FROM Reviews;')
    try:
        upto_date,upto_link = cur.fetchone()
        print('last review: {}, {}'.format(upto_date,upto_link))
    except:
        print('Error querying table for most recent review')


    baseurl = 'http://smartbitchestrashybooks.com/review/book/page/'

    # hardwired in on num. of pages, there is definitely
    # a better way to do this
    for i in range(0,60): #60 total pages: 06 July 2016
        if i%5 == 0: print(i)
        url = baseurl+str(i)+'/'
        html = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(html,'lxml')

        for entry in soup.find_all('header',{'class':'entry-header book'}):
            start += 1

            book = entry.find('h1',{'class':'entry-title'})
            link = book.a.get('href')

            meta_info = entry.p.text
            x = re.findall('· ([A-Za-z]+ [0-9,]+ [0-9]+) .+ ·',meta_info)
            try:
                date = format_date(x[0])
            except IndexError:
                # Probably and issue where post is updated
                # Set date to a blank value
                date = ' '
                print('Error',meta_info)

            # stop when we are upto last link scrape
            if link == upto_link:
                break
            else:
                cur.execute('INSERT INTO Reviews (id,Review_date,link)\
                VALUES (?, ?, ?)',(start,date,link))

        # need to check again to exit out of outside loop
        # (this should be folded into a function so less clumsy)
        if link == upto_link:
            break

        # only commit every 5 indicies to speed up process
        if i%5 == 0:
            conn.commit()

        time.sleep(1)

    conn.commit()  # commit anything still outstanding
    cur.close()
