
# SBTB grade analysis
This is a markdown summary of the output of the jupyter notebook ```analysis_sbtb.ipynb```. While I'm working, I hate saving doing version control on the output of jupyter notebooks, so this serves as an output checkpoint.

This goes through an overview of the data pulled, looking at grade distribution and genres for site and by reviewer.


## Plot reviewer distribution
Number of reviews by each unique reviewer. Carrie S' reviews *include* her guest reviews before she was a regular contributor.

![png](output_5_0.png)


---

## Rendering grades

Grading scale is a 5 point scale +/- 0.3 for plus and minus so that I can set "DNF" to zero.

Non-graded reviews are given a category of "Misc" and assigned a numerical score of -1. These reviews include "Rant" and "Squee" reviews, as well as the "N/A" reviews. Some "N/A" reviews were miscategorized and don't belong in the book review section. Others were non-graded reviews.

---

## Plot grade distribution
This plots the grade distribution for the full site including all reviews by all reviewers.


![png](output_10_0.png)


---

## Plot grade distribution by reviewer

Now we want to look at grade distributions for each reviewer.
I would expect Guest Reviews are going to be bimodal (very positive or very negative).


```python
def fill_grade_gaps(grade_df):
    # Want all possible grades, any not in dataframe will be set to zero
    if len(grade_df) == len(grade_dict_invert):
        return grade_df
    df_zeros = pd.DataFrame(0, index=sorted(list(grade_dict_invert.keys())), columns=['Id'])
    return grade_df.add(df_zeros, fill_value=0)
```


```python
reviewers = df['Reviewer'].unique()

fig = plt.figure(figsize=(15,25))

for i, reviewer in enumerate(reviewer_count.index):
    #print(reviewer)
    grades = df[df['Reviewer']== reviewer]
    grades = grades[['grade_num','Id']]
    grades_count = grades.groupby('grade_num').count(); #print(grades_count)
    grades_count = fill_grade_gaps(grades_count)

    ax = fig.add_subplot(4,2,7-i)
    ax.set_frame_on(False)

    y_pos = np.arange(len(grades_count));
    ax.barh(y_pos, grades_count['Id'], align='center', color='grey', lw=0)

    ax.set_title(reviewer)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels)

    ax.set_xlabel('# reviews', size=14)
    ax.set_ylabel('Review grade', size=14)

    ax.yaxis.set_ticks_position('none')
    ax.yaxis.set_tick_params(labelsize=12)

    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2, length=7, color='grey', labelsize=12)




    #grades_count.plot(kind='bar',legend=False,grid=True,title=reviewer)

plt.show()
```


![png](output_13_0.png)


---

## Calculate the review GPA

Ignore any of the "Miscellaneous" category entries, mostly those are "Rant" and "Squee" reviews. It's like an audit.

This calculation could be put into the title of the above bar charts.


```python
for i, reviewer in enumerate(reviewer_count.index):
    grades = df[(df['Reviewer']==reviewer) & (df['grade_num']>-1)]['grade_num']
    print('{} GPA: {:.2f}'.format(reviewer, grades.sum()/grades.count()))
```

    Amanda GPA: 3.62
    Candy GPA: 3.37
    Guest Reviewer GPA: 4.08
    Redheadedgirl GPA: 3.82
    Elyse GPA: 3.81
    SB Sarah GPA: 3.41
    Carrie S GPA: 4.07


---

## Find top genres reviewed

I believe "Romance" might be one of those genres, so that might need to be kicked out if it's the top genre for all reviewers. There might be consistency issues with how genres were done in the past versus now.

Multi-genre books have genres separated by semicolons. First, let's do the whole site, then by reviewer. Looping does not feel ideal, but the multi-genre thing is a killer.

Let's only look at graded reviews, so those not assigned a "miscellaneous" grade.


```python
genresdb = df[df['grade_num'] > -1]['Genres']; print("Total reviews: {}\n".format(genresdb.count()))
genres = {}
for genre in genresdb:
    genre_list = [g.strip() for g in genre.split(';')]
    for g in genre_list:
        genres.setdefault(g, 0)
        genres[g] += 1

pprint.pprint(genres)
```

    Total reviews: 1261

    {'Anthology': 2,
     'Art': 2,
     'Chick Lit': 13,
     'Classic': 19,
     'Comic': 26,
     'Contemporary Romance': 274,
     'Contemporary/Other': 10,
     'Cookbook': 11,
     'Erotica/Erotic Romance': 60,
     'Fantasy/Fairy Tale Romance': 12,
     'GLBT': 45,
     'Gothic': 3,
     'Graphic Novel': 18,
     'Historical': 165,
     'Historical: American': 26,
     'Historical: European': 137,
     'Historical: Other': 14,
     'Horror': 17,
     'Humor': 10,
     'Inspirational': 1,
     'Literary Fiction': 27,
     'Memoir': 10,
     'Middle Grade': 1,
     'Mystery/Thriller': 47,
     'New Adult': 19,
     'Nonfiction': 86,
     'Not a Book': 1,
     'Novella': 28,
     'Paranormal': 84,
     'Regency': 41,
     'Romance': 362,
     'Romantic Suspense': 41,
     'Science Fiction/Fantasy': 215,
     'Steampunk': 15,
     'Teen Fiction': 2,
     'Time Travel': 13,
     'Top 100 Banned Books': 21,
     'Urban Fantasy': 22,
     'Western': 1,
     "Women's Fiction": 13,
     'Young Adult': 76}


---

## Find top 5 genres for each reviewer


```python
for i, reviewer in enumerate(reviewer_count.index):
    genresdb = df[(df['Reviewer']==reviewer) & (df['grade_num'] > -1)]['Genres'];

    print("\nReviewer: {}".format(reviewer))

    genres = {}
    for genre in genresdb:
        genre_list = [g.strip() for g in genre.split(';')]
        for g in genre_list:
            genres.setdefault(g, 0)
            genres[g] += 1
    reviewer_genres = pd.DataFrame.from_dict(genres, orient='index').rename(columns={0:'count'})
    pprint.pprint(reviewer_genres.sort_values(by='count', ascending=False)[:5])
```


    Reviewer: Amanda
                             count
    Romance                     34
    Contemporary Romance        22
    Erotica/Erotic Romance      12
    Paranormal                   6
    Science Fiction/Fantasy      5

    Reviewer: Candy
                             count
    Historical                  23
    Science Fiction/Fantasy     10
    Contemporary Romance        10
    Paranormal                   8
    Literary Fiction             3

    Reviewer: Guest Reviewer
                            count
    Romance                    23
    Contemporary Romance       19
    Historical                  9
    Erotica/Erotic Romance      6
    GLBT                        6

    Reviewer: Redheadedgirl
                          count
    Romance                  52
    Historical: European     32
    Historical               27
    Contemporary Romance     13
    Nonfiction                8

    Reviewer: Elyse
                          count
    Romance                 114
    Contemporary Romance     54
    Historical: European     43
    Romantic Suspense        26
    Mystery/Thriller         24

    Reviewer: SB Sarah
                          count
    Contemporary Romance    131
    Historical               70
    Romance                  51
    Paranormal               35
    Young Adult              26

    Reviewer: Carrie S
                             count
    Science Fiction/Fantasy    154
    Romance                     88
    Nonfiction                  64
    Historical: European        45
    Young Adult                 34



```python

```
