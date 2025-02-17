from crypt import methods
from email.policy import default

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Article' {self.id}: {self.title}>"

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/articles', methods=['POST','GET'])
def articles():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка!"
    else:
        return render_template("articles.html")


@app.route('/posts')
def posts():
    articles_posts = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles_posts=articles_posts)


@app.route('/posts/<int:id>')
def post_detail(id):
    post_article = Article.query.get(id)
    return render_template("post_detail.html", post_article=post_article)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


if __name__ == "__main__":
    app.run(debug=True)