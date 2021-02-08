import io
from flask import Flask, Response, request, session
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import os
# from flask_matplotlib.bookdatabase import Bookinfo, loadDataFromDatabase, saveDataToDatabase
from bookdatabase import Bookinfo, loadDataFromDatabase, saveDataToDatabase
import matplotlib as mpl

mpl.use('Agg')

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1440)
app.config.from_pyfile('app.cfg')

# app.secret_key = os.urandom(10)

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    """Returns html with the img tag for your plot.
    """
    # book_chapter_answers_word_count = (
    #     ('TGF',(1,1452)),
    #     ('TGF',(2,276)),
    #     ('The Third Wheel',(1,42)),
    #     ('The Third Wheel',(2,30))
    # )
    # book_chapter_answers_word_count = Bookinfo.query.all()
    # word_cnt_list2= []
    # for row in Bookinfo.query.all():
        # print("book name {} chapter number {} word count {}".format(row.book_name, row.chapter_id, row.word_count))
        # name = row.book_name
        # chap = row.chapter_id
        # word_count = row.word_count
        # word_cnt_list2.append((name, (chap, word_count)))
        # # book_chapter_answers_word_count = tuple(word_cnt_list2)
        # groups = groupby(word_cnt_list2, key=itemgetter(0))
        # book_chapter_answers_word_count = tuple([(key, tuple([(item[1], item[2]) for item in subiter])) for key, subiter in groups])
        # print("tuple: ", book_chapter_answers_word_count)
        # book_chapter_answers_word_count = BookChapterWordCount.query.all()
        # book_chapter_answers_word_count_list = []
    # for item in book_chapter_answers_word_count:
    #     word_cnt_list2.append((item.book_name, item.chapter_id, item.word_count))
    #     print("list: ", word_cnt_list2)
    #     groups = groupby(word_cnt_list2, key=itemgetter(0))
    #     book_chapter_answers_word_count = tuple([(key, tuple([(item[1], item[2]) for item in subiter])) for key, subiter in groups])
    #     print("tuple: ", book_chapter_answers_word_count)
    # print ("pause")
    saveDataToDatabase()
    book_chapter_answers_word_count = loadDataFromDatabase()
    session["book_chapter_answers_word_count"] = book_chapter_answers_word_count
    print (book_chapter_answers_word_count)
    return render_template("show_plot.html", book_chapter_answers_word_count = book_chapter_answers_word_count)


@app.route("/matplot-as-image-<book_title>.png")
def plot_png(book_title=""):
    """ renders the plot on the fly.
    """
    book_chapter_answers_word_count = session.get("book_chapter_answers_word_count")
    word_count = []
    chapter_word_count = []
    for (title, book_info) in book_chapter_answers_word_count:
        if title == book_title:
            for (ch, cnt) in book_info:
                word_count.append(cnt)
                chapter_word_count.append(ch)
    sorted_chapter = sorted(chapter_word_count)
    # sorted_chapter, word_count  = zip(*sorted(zip(sorted(chapter_word_count)))
    print(sorted_chapter, word_count)

    fig = plt.figure()
    ax = sns.barplot(x=sorted_chapter, y=word_count, palette="Blues_d")
    ax.set(xlabel="Chapter", ylabel="Word Length")
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8091)
    app.run(debug=True)


