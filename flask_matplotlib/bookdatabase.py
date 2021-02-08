from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itertools import groupby
from operator import itemgetter
from datetime import datetime
app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


class Bookinfo(db.Model):
    book_name = db.Column(db.String(50), unique = False, nullable = False)
    chapter_id = db.Column(db.Integer)
    # word_count = db.Column(db.Integer, primary_key=True)
    word_count = db.Column(db.Integer)

    id = db.Column(db.Integer(), primary_key=True)


    def __repr__(self):
        return '<Bookinfo %r>' % self.book_name


db.create_all()

book_chapter_answers_word_count = {'TGF': {1: 1452,
                                           2: 276},
                                   'The Third Wheel': {1: 42,
                                                       2: 30}}

def saveDataToDatabase():
    for book_name in book_chapter_answers_word_count.keys():
        for chapter_id, word_count in book_chapter_answers_word_count[book_name].items():
            np = Bookinfo(book_name=book_name,chapter_id=chapter_id,word_count=word_count)
            check = Bookinfo.query.filter_by(book_name=book_name,chapter_id=chapter_id,word_count=word_count).first()
            if check is None:
                db.session.add(np)
                db.session.commit()

def loadDataFromDatabase():
    book_chapter_answers_word_count = Bookinfo.query.all()
    word_cnt_list2 = []
    for item in book_chapter_answers_word_count:
        word_cnt_list2.append((item.book_name, item.chapter_id, item.word_count))
        print("list: ", word_cnt_list2)
        groups = groupby(word_cnt_list2, key=itemgetter(0))
        book_chapter_answers_word_count = tuple(
            [(key, tuple([(item[1], item[2]) for item in subiter])) for key, subiter in groups])
        print("tuple: ", book_chapter_answers_word_count)
    return book_chapter_answers_word_count

if __name__ == '__main__':
    saveDataToDatabase()
    loadDataFromDatabase()