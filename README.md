# SCRAPE_SBTB

This project was initiated to learn web scraping with Beautiful Soup by
scraping and characterizing the reviews on
[Smart Bitches Trashy Books](http://smartbitchestrashybooks.com/).

**booklinks.py** harvests all review links from the book review index on the
site. Operates in two modes (mode automatically chosen based on
existing database):
1. if ID column is unpopulated, it will go through the book review index
scraping all links to full review pages. The number of pages to look through
is currently hardwired in (not ideal) so you need to manually check how many
pages of reviews there are before running this code.
Data are stored in an SQL table.
2. if the ID column is populated, it finds the MAX(review_date) and
associated link. Starting at page one of the book reivew index, it scrapes
links of full review pages until reaching the newest review in the database.


**scrape_reviews.py** goes through each link for the full book review and
pulls information on the reviewer, grade, book title, book author,
publication year, genres, and themes, and writes it to the database.
Book review format was redesigned and implemented 14 October 2014;
code first tries scraping by assuming the new formatting, and if that fails,
it checks for the old formatting.


TODO:
* ~~In titleauthor occasional "By" is used rather than "by" update code
to catch this~~
* ~~Update pieces to be held in functions rather than inline~~
* Set up error log that is maintained so I know which rows need fixing
* ~~change number of entries to scrape a command line argument~~
* ~~update booklinks.py to add new reviews to table~~
* ~~change scrape format of "new" styled posts to get
 title/author info~~
* ~~get rid of overflow lines by removing unpacking~~
* ~~convert genres into string before returning~~
* ~~create two cursors: one to iterate thru table, one to update table~~
* ~~differentiate between genres and themes (only pull genres? should I pull
  themes?)~~
* ~~Still some issues with genres and themes.~~
  * ~~some themes are still contaminating genres~~
  * ~~Found one early format book rant that has the author name populating
    the Genre column (id=641)~~ It's just one, I'm fixing it by hand
* When using ```scrape_reviews.py```, if you hit don't include a
  scrape number and hit "Enter" to accept default value of 10, it
  gives ```Error: must be integer``` but otherwise does behave
  as expected
* If there are no genres, the field is set to an empty string.
  Should probably be left as null

### Database notes
I'm going to note if I change anything by hand. There are a couple
one-off issues that I'm seeing that are a bit too specialized to
account for by changing my code, so I'm going to change them via SQL
and note them here.
* ID=641, removed genre listing that was only the author name
* ID=993, change grade DNF to N/A. The post is explanatory about
  future DNFs, not about any book in particular.

### Update notes
2016-09-20: I've added a "guest_review" column. 0 = not a guest review,
1 = guest review.

2016-09-28: cleaned up reviewer information with SQL within table.

2016-09-29: Updated booklinks.py to update SQL table with new reviews

2017-02-21: I see the issue that I'm having with genres. In the new format
"themes" are also linked (and not differentiated in the html) in the callout,
so I'm pulling not just genres, but also the listed themes.

2017-03-13: The scraping functions differentiate between genre and theme now!
While paging through a couple results, I discovered that there
are also now occasional "archetypes." My code ignores these and will not
capture them.
Also, I've added a test mode for the scraping functions so I don't have
to manually toggle between how the files are read
