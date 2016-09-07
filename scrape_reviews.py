import sys,os
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sql
import glob # for testing
import re

def get_grade(html_text):
    try:
        grade = html_text.find('h1',{'class':'grade'}).text
    except:
        print('grade problem',link)
        grade = 'N/A'
    return grade
    
def get_reviewer(html_text):
    try:
        reviewer = html_text.find('div',{'class':'entry-meta'}).a.text
    except:
        print('reviewer issue',link)
        reviewer = 'N/A'
    return reviewer
    
def get_reviewertitleauthor(html_text):
    titleauthor = html_text.find('h1',{'class':'entry-title'}).text
    
    if ('guest' and 'review') in titleauthor.lower():
        return get_guestreview(html_text)            
        
    reviewer = get_reviewer(html_text);
    
    ind = (titleauthor.lower().rfind('by'))
    if ind < 0:
        title = titleauthor
        author = ''
        print('no author listed',link)
    else:
        title = titleauthor[:ind]
        author = titleauthor[ind+3:]
    
    return reviewer,title,author
    
def get_guestreview(html_text):
    titleauthor = html_text.find('h1',{'class':'entry-title'}).text
    ind = (titleauthor.lower().rfind('by'))
    if ind < 0:
        print('guest reviewer issue',link)
        reviewer=titleauthor
        author=''
    else:
        reviewer = titleauthor[ind+3:]
        
    reviewbox = html_text.find(
         'div',{'class':'review-box'}).p.text.strip().split('\n')
    #get title     
    try:
        title_info = [s for s in reviewbox if s.lower().startswith('title')][0]
        ind = title_info.find(':')
        title = title_info[ind+1:].strip()
    except:
        print('title error',link)
        title = ''
    #get author
    try:
        auth_info = [s for s in reviewbox if s.lower().startswith('author')][0]
        ind = auth_info.find(':')
        author = auth_info[ind+1:].strip()
    except IndexError:
        print('no listed author',link)
        author = ''
    return reviewer,title,author
    
    
    
def get_genre_pubyear(html_text):
    try:
        genres = [genre.text for genre in html_text.find(
        'div',{'class':'callout'}).find_all('a')[1:]]
        pub_info = html_text.find('div',{'class':'featured'}).find(
        'p',{'class':'pub'}).text
        pub_years = re.findall(r'\d{4}',pub_info)
        if len(pub_years) < 1:
            pub_year = None
            print("no pub_year: ",link)
        elif len(pub_years) > 1:
            print("multiple pub_years: ",pub_years,link)
            pub_year = min(pub_years)
        else:
            pub_year = pub_years[0]
    except AttributeError:
        try:
            genre = html_text.find(
            'div',{'class':'review-box'}).text.strip().split('\n')
            genres = [genre[-1].split(':')[1]]
            pub_info = [s for s in genre if s.startswith('Publication')][0]
            pub_years = (re.findall('\d{4}',pub_info))
            if len(pub_years) < 1:
                pub_year = None
                print("no pub_year: ",link)
            elif len(pub_years) > 1:
                print("multiple pub_years: ",pub_years,link)
                pub_year = min(pub_years)
            else:
                pub_year = pub_years[0]
            
        except IndexError:
            print('genre problem',link)
            genres = ['']
            pub_year = None
            
        except AttributeError:
            print('other problem, setting genre, pub_year to null',link)
            genres = ['']
            pub_year = None
            print('')
    return genres,pub_year
    
def newformat_genre_pubyear(html_text):
    pass
    
def oldformat_genre_pubyear(html_text):
    pass
    
def input_scrape_number():
    """Asks user to input number of reviews to scrape
    Default value is used if no input is given/ValueError raised
    Returns integer 
    """
    default = 10
    num = input('Number to scrape [default {}]: '.format(default))
    try:
        return int(num)
    except ValueError:
        print('Error: non-numeric value')
        print('setting value to default: {}'.format(default))
    return default



def parse_webpage(link):
    html = urllib.request.urlopen(link).read()
    review = BeautifulSoup(html,'lxml').article
    return review

if __name__ == '__main__':
    
    #COMMENT OUT FOR TESTING 
    conn = sql.connect('sbtb.db',timeout=100)
    cur = conn.cursor()
    
    try:
        iters = int(sys.argv[1])
    except ValueError:
        # arg isn't a number
        print('Error: non-numeric value provided')
        iters = input_scrape_number()
    except IndexError:
        # no arg passed in
        iters = input_scrape_number()
        
    i = 0
    
    while i < iters:
        
        cur.execute('SELECT Id,Link From Reviews WHERE Grade IS NULL;')
        
        Id,link = cur.fetchone()
        #print(Id,link)
        
        if link == None:
            break
    
        review = prase_webpage(link)
        
        grade = get_grade(review)
        
        reviewer,title,author = get_reviewertitleauthor(review)
        
        genres,pub_year = get_genre_pubyear(review)
                
        
        #print(grade,reviewer,genres,title,author,pub_year,'\n')
        #print('; '.join(genres))
        
        
        cur.execute('UPDATE Reviews SET Reviewer=?,Grade=?,Title=?,Author=?,\
                     Pub_year=?,genres=? WHERE Id=?;',(reviewer,grade,\
                     title,author,pub_year,' '.join(genres),Id))
        
        if i%10 == 0:
            print(i)
            conn.commit()
            
        i += 1
    
    conn.commit()
    
    """
    links = glob.glob('testfiles/book*')
    
    for link in links:
        review = BeautifulSoup(open(link,'r'),'lxml').article
        
        grade = get_grade(review)
        reviewer,title,author = get_reviewertitleauthor(review)
        
        genres,pub_year = get_genre_pubyear(review)
        
        print(grade,reviewer,genres,title,author,pub_year,'\n')
    """