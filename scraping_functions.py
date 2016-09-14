import sys, os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import re


def scrape_info(link, date):
    """Find and return review data from webpage
    Returns:
    grade,reviewer,title,author,pub_year as strings
    genres as list
    """
    review = parse_webpage(link)

    if date > '2014-10-13':
        info = scrape_new_format(review)
    else:
        info = '', '', '', '', [''], ''
    return info


def parse_webpage(link):
    """Parse html of given link
    Return article text
    """
    try:
        html = open(link, 'r') #for testing
        #html = urllib.request.urlopen(link).read()
    except:
        print('Invalid link', link)
        raise
    review = BeautifulSoup(html, 'lxml').article
    return review


def scrape_new_format(review):
    """Find and return scraped info from reviews with new format
    Returns: grade,reviewer,title,author,genres,pub_year
    """
    grade = get_grade(review)
    reviewer, title, author = get_new_reviewertitleauthor(review)
    genres = get_new_genres(review)
    return grade, reviewer, title, author, genres, ''


def get_grade(html_text):
    """Returns grade for a review
    Returns "N/A" if can't find grade
    """
    try:
        grade = html_text.find('h1', {'class': 'grade'}).text
    except:
        print('grade problem')
        grade = 'N/A'
    return grade


def get_new_reviewertitleauthor(html_text):
    """Returns reviewer,title,author for new format reviews"""
    review_title = html_text.find('h1', {'class': 'entry-title'}).text
    
    if ('guest' and 'review') in review_title.lower():
        return get_new_guestreview(html_text)            
        
    reviewer = get_reviewer(html_text)
    title, author = get_new_titleauthor(html_text)
    
    if title is None:
        title = review_title
    
    return reviewer, title, author


def get_new_guestreview(html_text):
    """Returns reviewer info, title,author for new format guest reviews"""
    return '', '', ''


def get_reviewer(html_text):
    """Return reviewer (listed as post author)"""
    try:
        reviewer = html_text.find('div', {'class': 'entry-meta'}).a.text
    except:
        print('reviewer issue', link)
        reviewer = 'N/A'
    
    return reviewer

    
def get_new_titleauthor(html_text):
    """Return title and author for new format reviews"""
    try:
        details = html_text.find('div', {'class': 'hide-for-mobile-large'})
    except:
        print("problem with title author details")
        return None, None
    try:
        title = details.h6.em.text
    except AttributeError:
        print("No title found")
        return None, None
    try:
        author = details.find('p', {'class': 'small'}).a.text
    except AttributeError:
        print("No author found")
        return title, None
    
    return title, author


def get_new_genres(html_text):
    """Return genres from new format reviews"""
    try:
        genres = [genre.text for genre in html_text.find(
            'div', {'class': 'callout'}).find_all('a')[1:]]
    except AttributeError:
        print('issue with genres')
        return ''
    return ' '.join(genres)
        

if __name__ == '__main__':

    pass
