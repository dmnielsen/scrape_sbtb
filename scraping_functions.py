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
    reviewer,title,author = get_new_reviewertitleauthor(review)
    return grade,reviewer,title,author,[''],''
    
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
    
    if ('guest' and 'review') in review_title.lower():
        return get_new_guestreview(html_text)            
        
    reviewer = get_reviewer(html_text);
    
    ind = (review_title.lower().rfind(' by '))
    if ind < 0:
        title = review_title
        author = ''
        print('no author listed')
    else:
        title = review_title[:ind]
        author = review_title[ind+3:]
    
    return reviewer,'',''

def get_new_guestreview(html_text):
    """Returns reviewer info, title,author for new format guest reviews"""
    return '','',''

def get_reviewer(html_text):
    """Return reviewer (listed as post author)"""
    try:
        reviewer = html_text.find('div',{'class':'entry-meta'}).a.text
    except:
        print('reviewer issue',link)
        reviewer = 'N/A'
    
    return reviewer
    
if __name__ == '__main__':
    
    pass