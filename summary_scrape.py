import bs4
import pandas as pd
import numpy as np
import requests as r
import re
import traceback

# Change the number variable everytime you run the script 
# or else you will override the varialbe
number = '34'

# Start and end of the row's being parse
start = 27500
end = 30001

description = []
title = []
# Change for loop and to_csv(number)
def initiate_2():

    url = 'https://www.goodreads.com'

    df = pd.read_csv('Best_Books_Ever.csv')

    for i in range(start, end):

        # Make a request to get the html code
        res_des = r.get(url + df['href'][i])

        # Check the website status
        res_des.raise_for_status()

        # Instantiate and Parse description
        soup_des = bs4.BeautifulSoup(res_des.text)
        
        # Get book title
        book_title = (soup_des.find_all('h1', {'id':'bookTitle'})[0].text
                                    .strip('\n').strip())
        title.append(book_title)

        print(f"Now Scraping: {i} {book_title}")

        try:
            # Find description container
            descrip_container = (soup_des.find_all('div', {'class':'readable'})[0].text
                                .strip('\n').replace('\n...more', '').replace('--back cover', ''))
            
            # Append description
            description.append(descrip_container)

            print('--- Description has been Scraped ---','\n')
            
        except IndexError:
            # Print Error
            traceback.print_exc()

            # Append null value
            description.append(np.nan)
            print('Description Does Not Exist')


    # Change lists to Series
    des_series = pd.Series(description, name='description')
    title_series = pd.Series(title, name='book_title')

    # Combine series
    combine = pd.concat([title_series, des_series], axis=1)

    # Export Description
    combine.to_csv('summary_' + str(number) + '.csv')


    print('Done')

initiate_2()