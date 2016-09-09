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
        grade,reviewer,title,author,genre,pub_year = scrape_new_format(review)
    else:
        grade,reviewer,title,author,genre,pub_year = '','','','',[''],''
    return grade,reviewer,title,author,genre,pub_year
    
    
def parse_webpage(link):
    """Parse html of given link
    Return article text
    """
    try:
        html = open(link,'r') #for testing
        #html = urllib.request.urlopen(link).read()
    except:
        print('Invalid link',link)
        raise
    review = BeautifulSoup(html,'lxml').article
    
    return review

def scrape_new_format(review):
    """Find and return scraped info from reviews with new format
    Returns: grade,reviewer,title,author,genres,pub_year
    """
    grade = get_grade(review)
    return grade,'','','',[''],''
    
def get_grade(html_text):
    """Returns grade for a review
    Returns "N/A" if can't find grade
    """
    try:
        grade = html_text.find('h1',{'class':'grade'}).text
    except:
        print('grade problem')
        grade = 'N/A'
    return grade

def get_new_reviewertitleauthor(html_text):
    """Returns reviewer,title,author for new format reviews"""
    review_title = html_text.find('h1',{'class':'entry-title'}).text
    
    if ('guest' and 'review') in titleauthor.lower():
        return get_new_guestreview(html_text)            
        
    reviewer = get_reviewer(html_text);
    
    ind = (titleauthor.lower().rfind(' by '))
    if ind < 0:
        title = titleauthor
        author = ''
        print('no author listed')
    else:
        title = titleauthor[:ind]
        author = titleauthor[ind+3:]
    
    return '','',''

def get_new_guestreview(html_text):
    """Returns reviewer info, title,author for new format guest reviews"""
    return '','',''
    
if __name__ == '__main__':
    
    pass