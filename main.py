from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(9999))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    username = db.Column(db.String(120), unique=True)
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash("User password incorrect, or user does not exist")
            return redirect('/login')


    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if len(username) < 1 or len(password) < 1 or len(verify) < 1:
            flash("One or more fields are empty")
            return redirect("/signup")
        if len(username) < 3 or len(password) < 3:
            flash("Username and Password must be 3 characters long")
            return redirect("/signup")
        if password != verify:
            flash("Passwords do not match")
            return redirect("/signup")

        existing_user = User.query.filter_by(username = username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash("User successfully registered!")
            return redirect('/')
        else:
            flash("User already exists")
            return redirect('/signup')

    return render_template("signup.html")

@app.route("/logout")
def logout():
    del session['username']
    return redirect("/")

@app.route("/newpost", methods=['POST', 'GET'])
def new_post(): 

    #Username/Password verification here? There is an additional paramater to consider when creating a blog entry.

    if request.method == 'POST':    
        title = request.form['title']
        content = request.form['content']
        errors = False
        if len(title) < 1 or len(content) < 1:
            title_error = ""
            body_error = "Please fill in the body"
            errors = True
            if len(title) < 1:
                title_error = "Please fill in the title"
                errors = True
            if len(content) < 1:
                body_error = "Please fill in the body"
                errors = True


        if errors == True:
            return render_template("/newpost.html", title_error=title_error, body_error=body_error)

        if errors == False:
            title = request.form['title']
            content = request.form['content']
            owner = User.query.filter_by(username = session['username']).first()
            new_entry = Blog(title, content, owner)
            db.session.add(new_entry)
            db.session.commit()
            blog_id = new_entry.id
            return redirect("/individual-blog?id={0}".format(blog_id))

    else:
        return render_template("newpost.html")


@app.route("/blog", methods=['POST', 'GET'])
def blog_list():     

    all_blogs = Blog.query.all()   
    
    blog_query = request.args.get('id')
    if blog_query:
        blog = Blog.query.get(blog_query)
        return render_template("individual-blog.html", blog_id=blog_id)

    user_query = request.args.get('user')
    if user_query:
        user_id = Blog.query.get(user_query)
        blogs = Blog.query.filter_by(owner=user_id)
        return render_template("user-blogs.html", blogs=blogs)


    return render_template("blog.html", all_blogs=all_blogs)
    


@app.route("/individual-blog")
def individual_blog():
    blog_query = request.args.get('id')
    blog = Blog.query.get(blog_query)
    return render_template("individual-blog.html", blog=blog)


@app.route("/", methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template("index.html", users = users)


if __name__ == '__main__':
    app.run()