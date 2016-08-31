Trying out web scraping with Beautiful Soup by characterizing the reviews on
[Smart Bitches Trashy Books](http://smartbitchestrashybooks.com/).

**booklinks.py** harvests all review links from the book review index on the
site. Currently it is set up to go through on one pass and grab all of them and
the number of pages that it looks through is hardwired in, which is not ideal.
Data are stored in an SQL table.

**scrape_reviews.py** goes through each link and pulls information on the
reviewer, grade, book title, book author, publication year, and genres and
writes it to the table. Review format was redone somewhere along the way,
so code first looks for the new formatting, if that fails, it checks for
the old formatting.

TODO:
* In titleauthor occasional "By" is used rather than "by" update code
to catch this
* Update pieces to be held in functions rather than inline
* Write some tests (think about edge cases that I've missed)
* Set up error log that is maintained so I know which rows need fixing
* make number of entries to scrape an argument
* drop "Not a book" genres/tags from the table
