Trying out web scraping with Beautiful Soup by characterizing the reviews on
[Smart Bitches Trashy Books](http://smartbitchestrashybooks.com/).

**booklinks.py** harvests all review links from the book review index on the
site. Currently it is set up to go through on one pass and grab all of them and
the number of pages that it looks through is hardwired in, which is not ideal.
Data are stored in an SQL table.

**scrape_reviews.py** goes through each link and pulls information on the
reviewer, grade, book title, book author, publication year, and genres and
writes it to the table. Review format was redone somewhere along the way
(14 October 2014), so code first looks for the new formatting, if that fails,
it checks for the old formatting. A restructure to look for guest reviews first
was added. Should outsource the whole process into functions.

2016-09-20: I've added a "guest_review" column. 0 = not a guest review,
1 = guest review.

2016-09-28: cleaned up reviewer information with SQL within table.

2016-09-29: Updated booklinks.py to update SQL table with new reviews

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
