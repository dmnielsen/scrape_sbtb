import glob
import scraping_functions as scrape

if __name__ == '__main__':

    links = glob.glob('testfiles/*book*')

    for link in links:
        print(link)
        if 'new' in link:
            date = '2016-09-09'
        else:
            date = '2013-01-01'

        fields = scrape.scrape_info(link,date,test=True)

        print(' '.join(str(x) for x in fields))
