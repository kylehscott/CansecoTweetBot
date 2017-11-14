#!/usr/bin/python

import bs4, requests, praw, sqlite3, datetime, time

conn = sqlite3.connect('CansecoTweets.db')
c = conn.cursor()

def tweet_db(tweet, tweet_url):
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    c.execute("INSERT INTO cansecoTweets (datestamp, tweet, tweetUrl) VALUES (?, ?, ?)",
               (date, tweet, tweet_url))
    conn.commit()

def get_tweet():
    res = requests.get('https://twitter.com/JoseCanseco')
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    tweet = soup.find("p", class_="tweet-text").text
    tweet_url = soup.select('.time > a')[0].get('href')
    return [tweet, tweet_url]

tweet = get_tweet()[0]

tweet_url = get_tweet()[1]

user_agent = ('Canseco Tweet 0.1')

r = praw.Reddit(user_agent = user_agent)

c.execute('SELECT tweet FROM cansecoTweets ORDER BY datestamp DESC')

if c.fetchall()[0][0] != tweet:
    r.login('CansecoTweetBot', 'password', disable_warning=True)
    r.submit('JoseCansecoTweets', tweet, url = "https://twitter.com" + tweet_url)
    tweet_db(tweet, tweet_url)
    print('Posted!')
else:
    print('Already posted')
