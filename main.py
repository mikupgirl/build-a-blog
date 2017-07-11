from flask import Flask, request, redirect, render_template, session, flash#can use bcrypt instead of hashlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] =  True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    submitted = db.Column(db.Boolean)
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.submitted = False



@app.route('/', methods=['GET'])
def index():

    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        blog_name_title = request.form['blog_title']
        blog_name_body = request.form['blog_body']        
        new_blog = Blog(blog_name_title, blog_name_body)        
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(submitted=False).all()
    return render_template('mainBlogPage.html',title="Build a Blog", blogs=blogs)

@app.route('/addBlogEntry', methods=['POST', 'GET'])
def addBlogEntry():
    
    title_error = ''
    blog_error = ''
    blog_title = ''
    blog_body = ''

    if request.method == 'POST':
        blog_name_title = request.form['blog_title']
        blog_name_body = request.form['blog_body']
        if len(blog_name_title) == 0:
            title_error = 'Please enter a title'

        if len(blog_name_body) == 0:
            blog_error = 'Please write your blog'

        if not title_error and not blog_error:
            new_blog = Blog(blog_name_title, blog_name_body)
            db.session.add(new_blog)
            db.session.commit()     
           
            return render_template('singleBlogEntries.html', blog=new_blog)   

    return render_template('addBlogEntry.html', title_error=title_error, blog_error=blog_error)


@app.route('/singleBlogs')
def singleBlogs():
    
    blog_id = request.args.get("id")       
    blog = Blog.query.get(blog_id)
    return render_template('singleBlogEntries.html', blog=blog)

if __name__ == '__main__':
    app.run()