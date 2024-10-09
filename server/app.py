#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User
from datetime import datetime

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Set session['page_views'] to 0 if it's not set yet
    session['page_views'] = session.get('page_views', 0)

    # Increment the page_views count
    session['page_views'] += 1

    # Check if the user has viewed more than 3 articles
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Fetch the article by its id using session.get()
    article = db.session.get(Article, id)
    if article:
        # Calculate the number of words in the article content
        word_count = len(article.content.split())
        # Estimate reading time assuming an average reading speed of 200 words per minute
        minutes_to_read = max(1, round(word_count / 200))

        preview = article.content[:50]  # Taking first 50 characters as preview
        date_published = article.date.strftime('%Y-%m-%d')  # Format the date field (assuming article.date is a datetime object)

        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,  # Directly return author as string
            'preview': preview,  # Add preview field
            'minutes_to_read': minutes_to_read,  # Add minutes_to_read field
            'date': date_published  # Add date field
        }), 200
    else:
        return jsonify({'message': 'Article not found'}), 404


if __name__ == '__main__':
    app.run(port=5555)
