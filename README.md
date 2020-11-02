This is v4.

v3 (the Colab file) was much faster than v2 (the Dash and Heroku app), but I wanted to make it faster. I noticed that once a menu is set for the day, it doesn't change, so I had to take advantage of that and find a way to run some code once a day and run other code per use. I looked into AWS Lambda and Google Cloud Scheduler but couldn't figure them out. I ended up choosing WayScript.

The code in directory 'Daily Lambda' (not a real Lambda, I know) runs at 12:01, the minute after midnight, every day. It performs the web scraping, stores it as a dataframe, and commits the dataframe as a csv to scraped.txt. The Colab ipynb file in the main directory is run per use. It generates a dataframe from scraped.txt and inserts an accurate 'isOpen' column. This is near instantaneous once the Colab is connected to a runtime.

The Colab is still at http://bit.ly/mdining-scraper

PRIOR VERSION OF README
This is v3 of my MDining Scraper app. 

v2 was quite slow. v3 is a Google Colab file that doesn't take long to connect and performs the web scraping much faster. More details at https://www.georgefane.com/all-posts/mdining-scraper

This Colab file is at http://bit.ly/mdining-scraper

PRIOR VERSION OF README
This is v2 of my MDining Scraper app.

v0 simply got the hours for each meal for each dining hall, which my friends helped me realize was not very useful. v1 got all hours, checks which meal for each dining hall is open right now, and then gets all foods for that meal. It showed all foods that you could feasibly get at this instant. v2 has everything in v1, as well as a 'search table' for users to find which hall is serving the food they want.

This app is deployed on Heroku at https://mdining-scraper.herokuapp.com/
