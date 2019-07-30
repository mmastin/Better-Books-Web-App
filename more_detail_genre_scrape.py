import bs4
import pandas as pd
import requests as r
import re
import traceback
import numpy as np

# Save df - Need the href
df = pd.read_csv('Best_Books_Ever.csv')

url = 'https://www.goodreads.com'

number = '6'
start = 24000
end = 26000

original_title = []
isbn = []
edition_language = []
series = []
characters = []
setting = []
literary_awards = []

genres_list = []

list_ = [original_title, isbn, edition_language, series, characters, setting, literary_awards]

# More Details - Scrape
def more_details_scrape():
    details_1 = soup.find_all('div', {'class': 'infoBoxRowTitle'})
    details_2 = soup.find_all('div', {'class': 'infoBoxRowItem'})
    details_1_list = [details_1[i].text for i in range(len(details_1))]
    details_2_list = [details_2[i].text for i in range(len(details_2))]
    names = ['Original Title', 'ISBN', 'Edition Language', 'Series', 'Characters', 'setting', 'Literary Awards']
    for j in range(len(names)):
        try:
            if names[j] in details_1_list:

                list_[j].append(details_2[details_1_list.index(names[j])].text.strip('\n')
                                .replace('\n', ' ').replace('  ', ' ').strip(' '))
            else:
                list_[j].append(np.nan)

        except IndexError:
            list_[j].append(np.nan)

    print('--- More Details has been Scraped ---')

# Genre Scrape
def genre_scrape():
    genres = []
    genre = soup.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
    print('--- Genres has been Scraped ---', '\n')

    for l in range(len(genre)):
        genres.append(genre[l].text)

    genres_list.append(genres)

    # Change into series
    combine_list = list_ + [genres]
    combine_list_names = ['original_title', 'isbn', 'edition_language', 'series', 
                          'characters', 'setting', 'literary_awards', 'genres']
    series_list = []
    for k in range(len(combine_list)):
        series_list.append(pd.Series(combine_list[k], name=combine_list_names[k]))

names = ['Original Title', 'ISBN', 'Edition Language', 'Series', 'Characters', 'setting', 'Literary Awards']
for i in range(start, end):
    res = r.get(url + df['href'][i])
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text)
    
    print(f"Now Scraping: {i} {df['book_title'][i]}")
          

    more_details_scrape()

    genre_scrape()
          
    series = [pd.Series(list_[i], name=names[i]) for i in range(len(names))]
    genres_series = pd.Series(genres_list, name='Genre')
    series.append(genres_series)

    df_more = pd.concat(series, axis=1)
          
    df_more.to_csv('more_detail_genre' + number + '.csv')