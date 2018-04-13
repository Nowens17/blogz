from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogit@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(9999))

    def __init__(self, title, content):
        self.title = title
        self.content = content



@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    blog_title = request.form['title']
    blog_content = request.form['content']

    return render_template("newpost.html")

@app.route("/blog", methods=['POST', 'GET'])
def blog_list():
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("base.html")


if __name__ == '__main__':
    app.run()