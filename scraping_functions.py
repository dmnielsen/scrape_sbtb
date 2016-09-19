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
        info = scrape_old_format(review)

    if info[-1]:
        print(link, info[-1])

    return info[:-1]


def parse_webpage(link):
    """Parse html of given link
    Return article text
    """
    try:
        html = open(link, 'r')  # for testing
        # html = urllib.request.urlopen(link).read()
    except:
        print('Invalid link', link)
        raise
    review = BeautifulSoup(html, 'lxml').article
    return review


def scrape_new_format(review):
    """Find and return scraped info from reviews with new format
    Returns: grade,reviewer,title,author,genres,pub_year
    """
    grade, e1 = get_grade(review)
    reviewer, title, author, e2 = get_new_reviewertitleauthor(review)
    genres, e3 = get_new_genres(review)
    pub_year, e4 = get_new_pubyear(review)

    error = ''.join([e1, e2, e3, e4])

    return grade, reviewer, title, author, genres, pub_year, error


def scrape_old_format(review):
    """Find and return scraped info from reviews with old format
    Returns: grade, reviewer, title, author, genres, pub_year"""
    grade, e1 = get_grade(review)
    reviewer, title, author, e2 = get_old_reviewertitleauthor(review)
    genres, e3 = get_old_genres(review)
    pub_year, e4 = get_old_pubyear(review)

    error = ''.join([e1, e2, e3, e4])

    return grade, reviewer, title, author, genres, pub_year, error


def get_grade(html_text):
    """Returns grade for a review
    Returns "N/A" if can't find grade
    """
    try:
        grade = html_text.find('h1', {'class': 'grade'}).text
    except:
        return 'N/A', 'grade problem/'
    return grade, ''


def get_new_reviewertitleauthor(html_text):
    """Returns reviewer,title,author for new format reviews
    If any errors occur, return descriptive string
    If no errors occur, return empty string
    """
    review_title = html_text.find('h1', {'class': 'entry-title'}).text

    if ('guest' and 'review') in review_title.lower():
        return get_new_guestreview(html_text)

    reviewer, e1 = get_reviewer(html_text)
    title, author, e2 = get_new_titleauthor(html_text)

    if title is None:
        title = review_title

    error = ''.join([e1, e2])

    return reviewer, title, author, error


def get_new_guestreview(html_text):
    """Returns reviewer info, title,author for new format guest reviews
    If any errors occur, return descriptive string
    If no errors occur, return empty string
    """
    return '', '', '', ''


def get_old_reviewertitleauthor(html_text):
    """Returns reviewer, title, author for old format reviews"""
    review_title = html_text.find('h1', {'class': 'entry-title'}).text

    if ('guest' and 'review') in review_title.lower():
        return get_old_guestreview(html_text)

    reviewer, e1 = get_reviewer(html_text)
    title, author, e2 = get_old_titleauthor(html_text)

    error = ''.join([e1, e2])

    return reviewer, title, author, error


def get_old_guestreview(html_text):
    """Returns reviewer info, title,author for old format guest reviews"""
    return '', '', '', ''


def get_reviewer(html_text):
    """Return reviewer (listed as post author)"""
    try:
        reviewer = html_text.find('div', {'class': 'entry-meta'}).a.text
    except:
        reviewer = 'N/A', 'reviewer issue/'
    return reviewer, ''


def get_new_titleauthor(html_text):
    """Return title and author for new format reviews"""
    try:
        details = html_text.find('div', {'class': 'hide-for-mobile-large'})
    except:
        return None, None, "problem with title author details/"
    try:
        title = details.h6.em.text
    except AttributeError:
        return None, None, "No title found/"
    try:
        author = details.find('p', {'class': 'small'}).a.text
    except AttributeError:
        return title, None, "No author found/"
    return title, author, ''


def get_old_titleauthor(html_text):
    """Return title and author for old format reviews"""
    reviewbox = html_text.find(
        'div', {'class': 'review-box'}).p.text.strip().split('\n')
    try:
        title_info = [s for s in reviewbox if s.lower().startswith('title')][0]
        ind = title_info.find(':')
        title = title_info[ind+1:].strip()
        title_error = ''
    except:
        title_error = 'title error/'
        title = ''
    try:
        auth_info = [s for s in reviewbox if s.lower().startswith('title')][0]
        ind = auth_info.find(':')
        author = auth_info[ind+1].strip()
        author_error = ''
    except IndexError:
        author_error = 'no author listed'
        author = ''
    return title, author, title_error+author_error


def get_new_genres(html_text):
    """Return genres from new format reviews"""
    try:
        genres = [genre.text for genre in html_text.find(
            'div', {'class': 'callout'}).find_all('a')[1:]]
    except AttributeError:
        return '', 'issue with genres/'
    return ' '.join(genres), ''


def get_old_genres(html_text):
    """Return genres from new format reviews"""
    try:
        genre = html_text.find(
            'div', {'class': 'review-box'}).text.strip().split('\n')
        genres = [genre[-1].split(':')[1]]
    except IndexError:
        return [''], 'Genre problem (index)/'
    except AttributeError:
        return [''], 'other genre problem (attribute)'
    return genres, ''


def get_new_pubyear(html_text):
    """Return publication year from new format reviews"""
    try:
        pub_info = html_text.find('div', {'class': 'featured'}).find(
                   'p', {'class': 'pub'}).text
    except AttributeError:
        return None, 'no publication info found/'
    pub_years = re.findall(r'\d{4}', pub_info)
    if len(pub_years) < 1:
        pub_year = None
        print("no pub_year")
    elif len(pub_years) > 1:
        print("multiple pub_years: ", pub_years)
        pub_year = min(pub_years)
    else:
        pub_year = pub_years[0]
    return pub_year, ''


def get_old_pubyear(html_text):
    """Return publication year from new format reviews"""
    try:
        genre = html_text.find(
            'div', {'class': 'review-box'}).text.strip().split('\n')
        pub_info = [s for s in genre if s.startswith('Publication')][0]
        pub_years = (re.findall('\d{4}', pub_info))
        if len(pub_years) < 1:
            pub_year = None
            err = "no pub_year/"
        elif len(pub_years) > 1:
            err = "multiple pub years/"
            pub_year = min(pub_years)
        else:
            err = ''
            pub_year = pub_years[0]
    except IndexError:
        pub_year = None
        err = 'no publication info found (index)'
    except AttributeError:
        pub_year = None
        err = 'no publication info found (attribute)'

    return pub_year, err


if __name__ == '__main__':

    pass
