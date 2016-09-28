import sys,os

if __name__ == '__main__':
    cutoff_date = '2014-10-28'
    
    conn = sql.connect('sbtb.db', timeout=100)
    cur = conn.cursor()
    
    conn.close()