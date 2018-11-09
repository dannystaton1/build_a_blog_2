from flask import Flask, request, redirect, render_template,session
import cgi
import os
from flask_sqlalchemy import SQLAlchemy
 






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


@app.route('/blog', methods=['GET'])

def index():

    id = request.args.get('id')
    if (id != None):
	
        post = Blog.query.get(int (id))

        return render_template('post.html',title=post.title, content=post.content)
    posts = Blog.query.order_by('date DESC').all()
    return render_template('post.html',title="Its a Blog", posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

    

    if (request.method == 'GET'):
	    return render_template('newpost.html',title="Add a Blog Entry")
    else:
	    title = request.form ['title']
	    content = request.form ['content']
    
    
    blog = Blog(title=title,  content=content())	
        
		
        
    db.session.add(blog)
    db.session.commit()
		
    return redirect('/blog?id=' + str(blog.id))



if __name__ == '__main__':
    app.run()