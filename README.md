# SCRAPE_SBTB

Trying out web scraping with Beautiful Soup by characterizing the reviews on
[Smart Bitches Trashy Books](http://smartbitchestrashybooks.com/).
I've worked on and off again on this project as other things have come
up.

**booklinks.py** harvests all review links from the book review index on the
site. Two modes:
1. if ID column is unpopulated, it will go through on one pass and grab all
of them and the number of pages that it looks through is hardwired in,
which is not ideal. Data are stored in an SQL table.
2. if the ID column is populated, it finds the MAX(review_date) and associated
link and adds reviews until it finds that review.


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

2017-02-21: I see the issue that I'm having with genres. In the new format
"themes" are also linked (and not differentiated in the html) in the callout,
so I'm pulling not just genres, but also the listed themes.

2017-03-13: The scraping functions differentiate between genre and theme now!
Huzzah! I reset the grades to Null for the entries I want to rerun and have
done a few. While paging through a couple results, I discovered that there
are also now occasional "archetypes." My code ignores these and will not
capture them.

Also, I've added a test mode in the scraping functions so I don't have
to manually toggle between how the files are read

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
