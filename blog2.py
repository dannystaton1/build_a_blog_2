from flask import Flask, request, redirect, render_template,session
import cgi
import os
import jinja2
from flask_sqlalchemy import SQLAlchemy



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build_a_blog:9QDJJZuXsCm1UvoW@localhost:8889/build_a_blog' 
app.config['SQLALCHEMY_ECHO']= True

db = SQLAlchemy(app)
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['GET', 'POST'])
def index():

    
    
    if request.args.get('post_id'):
        post_id = request.args.get('post_id')
        blog = Blog.query.get(post_id)

        return render_template('post.html',title = "It's a blog!",post_title = blog.title,content = blog.content)

    posts = Blog.query.all()
    
    return render_template('post.html',title="It's a Blog!",posts=posts)



@app.route('/', methods=['GET','POST'])
def newpost():
    
    

    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']

        if not title or not contents:
            return render_template('add.html',title = "Add a Blog Entry!")
        
        
        blog = Blog(title, contents)
        
        
        db.session.add(blog)
        db.session.commit()
        
        return redirect('post.html?post_id={}'.format(blog.id))

    return render_template('add.html',title = "Add a Blog Entry!")






if __name__ == '__main__':
    app.run()