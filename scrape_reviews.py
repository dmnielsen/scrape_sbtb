import sys,os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import glob # for testing
import re

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
                pub_info = [s for s in genre if s.startswith('Publication')][0]
                pub_years = (re.findall('\d{4}',pub_info))
                if len(pub_years) < 1:
                    pub_year = -9999
                    print("no pub_year: ",link)
                elif len(pub_years) > 1:
                    print("multiple pub_years: ",pub_years,link)
                    pub_year = pub_years[0]
                else:
                    pub_year = pub_years[0]
                
            except IndexError:
                print('genre problem',link)
                continue
            
        titleauthor = review.find('h1',{'class':'entry-title'}).text
        
        print(grade,reviewer,genres,titleauthor,pub_year,'\n')