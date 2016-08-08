import sys,os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import glob # for testing
import re

if __name__ == '__main__':
    
    #COMMENT OUT FOR TESTING 
    conn = sql.connect('sbtb.db',timeout=100)
    cur = conn.cursor()
    
    cur.execute('SELECT Id,Link From Reviews WHERE Grade IS NULL;')
    
    test = 0
    
    while test < 1:
        
        Id,link = cur.fetchone()
        print(Id,link)
        
        if link == None:
            break
    
        html = urllib.request.urlopen(link).read()
        review = BeautifulSoup(html,'lxml').article
        
        grade = review.find('h1',{'class':'grade'}).text
        reviewer = review.find('div',{'class':'entry-meta'}).a.text
        
        try:
            genres = [genre.text for genre in review.find(
            'div',{'class':'callout'}).find_all('a')[1:]]
            pub_info = review.find('div',{'class':'featured'}).find(
            'p',{'class':'pub'}).text
            pub_years = re.findall(r'\d{4}',pub_info)
            if len(pub_years) < 1:
                pub_year = -9999
                print("no pub_year: ",link)
            elif len(pub_years) > 1:
                print("multiple pub_years: ",pub_years,link)
                pub_year = pub_years[0]
            else:
                pub_year = pub_years[0]
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
        
        ind = (titleauthor.rfind('by'))
        if ind < 0:
            title = titleauthor
            author = ''
            print('titleauthor issue',link)
        else:
            title = titleauthor[:ind]
            author = titleauthor[ind+3:]
        
        #print(grade,reviewer,genres,title,author,pub_year,'\n')
        #print('; '.join(genres))
        
        
        cur.execute('UPDATE Reviews SET Reviewer=?,Grade=?,Title=?,Author=?,\
                     Pub_year=?,genres=? WHERE Id=?;',(reviewer,grade,\
                     title,author,pub_year,'; '.join(genres),Id))
        conn.commit()
        
        test += 1
    
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
            'p',{'class':'pub'}).text
            pub_years = re.findall(r'\d{4}',pub_info)
            if len(pub_years) < 1:
                pub_year = -9999
                print("no pub_year: ",link)
            elif len(pub_years) > 1:
                print("multiple pub_years: ",pub_years,link)
                pub_year = pub_years[0]
            else:
                pub_year = pub_years[0]
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
        
        ind = (titleauthor.rfind('by'))
        if ind < 0:
            title = titleauthor
            author = ''
            print('titleauthor issue',link)
        else:
            title = titleauthor[:ind]
            author = titleauthor[ind+3:]
        print(author)
        
        print(grade,reviewer,genres,title,author,pub_year,'\n')
        """