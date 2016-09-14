import glob
import scraping_functions as scrape

if __name__ == '__main__':
    
    links = glob.glob('testfiles/old_book*')
    
    for link in links:
        print(link)
        if 'new' in link:
            date = '2016-09-09'
        else:
            date = '2013-01-01'
        
        grade,reviewer,title,author,genres,pub_year = \
        scrape.scrape_info(link,date)
        
        
        print(grade,reviewer,title,author,genres,pub_year,'\n')