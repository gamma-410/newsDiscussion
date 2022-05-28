# newsDiscussion | app.py
# copyright 2022・5・11 | @gamma_410

import feedparser
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

rssURL = "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE5mTTJRU0FtcGhLQUFQAQ?hl=ja&gl=JP&ceid=JP:ja"
feed = feedparser.parse(rssURL)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    opinion = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    return render_template('index.html', feed=feed.entries)

@app.route('/opinion', methods=['GET', 'POST'])
def opinion():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('opinion.html', posts=posts)
    else:
        user = request.form.get('user')
        title = request.form.get('title')
        opinion = request.form.get('opinion')
        post_date = request.form.get('post_date')

        post_date = datetime.strptime(post_date, '%Y-%m-%d')
        new_post = Post(user=user, title=title, opinion=opinion, post_date=post_date)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/opinion')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def detail(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/opinion')


if __name__ == "__main__":
    app.run(debug=True)