import io
from flask import Flask, Response, request, session
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta
import os
from bookdatabase import Bookinfo, loadDataFromDatabase, saveDataToDatabase
import matplotlib as mpl

mpl.use('Agg')

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1440)
app.config.from_pyfile('app.cfg')


from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    """Returns html with the img tag for your plot.
    """
 
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


