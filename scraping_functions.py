import sys,os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import re



def scrape_info(link,date):
    """Find and return review data from webpage
    Returns: 
    grade,reviewer,title,author,pub_year as strings
    genres as list
    """
    review = parse_webpage(link)
    
    if date > '2014-10-13':
        grade,reviewer,title,author,genre,pub_year = '','','','',[''],''
    else:
        grade,reviewer,title,author,genre,pub_year = '','','','',[''],''
    return grade,reviewer,title,author,genre,pub_year
    
    
def parse_webpage(link):
    """Parse html of given link
    Return article text
    """
    try:
        html = urllib.request.urlopen(link).read()
    except:
        print('Invalid link',link)
        raise
    review = BeautifulSoup(html,'lxml').article
    
    return review
    
if __name__ == '__main__':
    
    pass