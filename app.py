# newsDiscussion | app.py
# copyright 2022・5・11 | @gamma_410

import feedparser
from flask import Flask, render_template

rssURL = "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE5mTTJRU0FtcGhLQUFQAQ?hl=ja&gl=JP&ceid=JP:ja"
feed = feedparser.parse(rssURL)

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html', feed=feed.entries)

if __name__ == "__main__":
    app.run(debug=True)