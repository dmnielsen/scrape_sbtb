import sys,os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import glob # for testing

if __name__ == '__main__':
    
    """ COMMENT OUT FOR TESTING 
    conn = sql.connect('sbtb.db',timeout=100)
    cur = conn.cursor()
    
    cur.execute('SELECT Link From Reviews WHERE Grade IS NULL;')
    
    while True:
        
        link = cur.fetchone()
        
        if link == None:
            break
    
        html = urllib.request.urlopen(link[0]).read()
    """
    
    links = glob.glob('testfiles/book*')
    
    for link in links:
        review = BeautifulSoup(open(link,'r'),'lxml').article
        
        grade = review.find('h1',{'class':'grade'}).text
        reviewer = review.find('div',{'class':'entry-meta'}).a.text
        
        try:
            genres = [genre.text for genre in review.find(
            'div',{'class':'callout'}).find_all('a')[1:]]
            pub_info = review.find('div',{'class':'featured'}).find(
            'p',{'class':'pub'}).text.split()
            pub_year = pub_info[pub_info.index('·')-1]
        except AttributeError:
            try:
                genre = review.find(
                'div',{'class':'review-box'}).text.strip().split('\n')
                genres = [genre[-1].split(':')[1]]
                print([s for s in genre if s.startswith('Publication')][0].split())
            except IndexError:
                print('genre problem',link)
                continue
            
        titleauthor = review.find('h1',{'class':'entry-title'}).text
        
        print(grade,reviewer,genres,titleauthor,'\n')