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
        pass