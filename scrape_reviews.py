import sys,os
import sqlite3 as sql
import scraping_functions as scrape

   
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
        print('Error: must be integer')
        print('setting value to default: {}'.format(default))
    return default


if __name__ == '__main__':


    conn = sql.connect('sbtb.db',timeout=100)
    cur_iter = conn.cursor()
    cur_update = conn.cursor()
    
    try:
        iters = int(sys.argv[1])
    except ValueError:
        # arg isn't a number
        print('Error: value must be integer')
        iters = input_scrape_number()
    except IndexError:
        # no arg passed in
        iters = input_scrape_number()
        
    i = 0
    
    cur_iter.execute('SELECT Id,Link,Review_date \
                From Reviews WHERE Grade IS NULL;')
    
    while i < iters:
               
        Id, link, date = cur_iter.fetchone()
        # print(Id,link,date)
        
        if link == None:
            break
        
        try:
    
            grade,reviewer,guest,title,author,genres,pub_year = \
            scrape.scrape_info(link,date)
        except:
            print("error on: ", link)
            break

        # print(grade,reviewer,guest,title,author,genres,pub_year,'\n')
        
        cur_update.execute('UPDATE Reviews SET Reviewer=?,Grade=?,Title=?,\
                    Author=?,Pub_year=?,genres=?,guest_review=? WHERE Id=?;',\
                    (reviewer,grade,title,author,pub_year,\
                    ' '.join(genres),guest,Id))

        if i%10 == 0:
            print(i)
            conn.commit()
            
        i += 1
    
    conn.commit()
    
    