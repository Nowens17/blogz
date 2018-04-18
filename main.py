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
    content = db.Column(db.String(9999))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route("/newpost", methods=['POST', 'GET'])
def new_post(): 

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
            new_entry = Blog(title, content)
            db.session.add(new_entry)
            db.session.commit()
            blog_id = new_entry.id
            return redirect("/individual-blog?id={0}".format(blog_id))

    else:
        return render_template("newpost.html")

#TODO: DONE
#One of the first and easiest changes is to make the header for the blog title on the home page be a link. But what url do we want it to link to? Well, this is the format that we want the url of a single blog entry to have: ./blog?id=6 (Here 6 is just one example of an id number for a blog post.) So using jinja2 templating syntax, how can you make sure that each blog entry that is generated on the main page has an href with a query parameter corresponding to its id?
#TODO: 
#The next thing we need to determine is how we are going to handle an additional GET request on our homepage since we are already handling a GET request there. Of course, the difference is that in this use case it's a GET request with query parameters. So we'll want to handle the GET requests differently, returning a different template, depending on the contents (or lack thereof) of the dictionary request.args.
#TODO: 
#Finally, we need to think about how the template is going to know which blog's data to display. The blog object will be passed into the template via render_template. What are the steps we need to take to get the right blog object (the one that has the id we'll get from the url) from the database and into the render_template function call?


@app.route("/blog", methods=['POST', 'GET'])
def blog_list():    
    blogs = Blog.query.all()
    return render_template("blog.html", blogs=blogs)



@app.route("/individual-blog")
def individual_blog():
    blog_query = request.args.get('id')
    blog = Blog.query.get(blog_query)
    return render_template("individual-blog.html", blog=blog)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("base.html")


if __name__ == '__main__':
    app.run()