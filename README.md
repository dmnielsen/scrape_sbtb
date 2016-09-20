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

New format guest review is still not configured.

Strange issue: found one "new format" review _well_ into the old
review timeline ()

TODO:
* ~~In titleauthor occasional "By" is used rather than "by" update code
to catch this~~
* ~~Update pieces to be held in functions rather than inline~~
* Write some tests (think about edge cases that I've missed)
* Set up error log that is maintained so I know which rows need fixing
* drop "Not a book" genres/tags from the table
* write code to go thru existing rows in table to look for improperly
attributed "Guest Reviews"
  - ~~Old format~~
  - New format
* ~~change number of entries to scrape a command line argument~~
* update booklinks.py to add new reviews to table
* change scrape format of "new" styled posts to get title/author info
* get rid of overflow lines by removing unpacking
* ~~convert genres into string before returning~~
* create two cursors: one to iterate thru table, one to update table
* **authors are not showing up with new scraping functions**
