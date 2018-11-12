from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://database:1234asdf@localhost:8889/database'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(1024))
	date = db.Column(db.DateTime)

	def __init__(self, title, body, date):
		self.title = title
		self.body = body
		self.date = date

@app.route('/blog', methods=['GET'])
def index():

	id = request.args.get('id')
	if (id != None):
		post = Blog.query.get(int (id))
		return render_template('post.html',title=post.title, body=post.body)
	posts = Blog.query.order_by('date DESC').all()
	return render_template('blog.html',title="Build a Blog", posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

	if (request.method == 'GET'):
		return render_template('newpost.html',title="Add a Blog Entry")
	else:
		title = request.form ['title']
		body = request.form ['body']
		titleError = ""
		bodyError = ""
		error = False
		if (title == ""):
			titleError = "Please fill in the title"
			error = True
		if (body == ""):
			bodyError = "Please fill in the body"
			error = True
		if error:
			return render_template('newpost.html',title="Add a Blog Entry", terror=titleError, berror=bodyError,
				blogTitle=title, blogBody=body)
		blog = Blog(title=title, body=body, date=datetime.utcnow())
		db.session.add(blog)
		db.session.commit()
		return redirect('/blog?id=' + str(blog.id))
	
if __name__ == '__main__':
	app.run()
