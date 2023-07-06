import git
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy


#creating an instance of the Flask class and assigns it to the variable 'app'
app = Flask(__name__)                    #passing name as an argument; tells Flask to use the cur. module as.a starting point
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'e396d8bc80ca4a84e00fd241e0f374b0'

#setting up a database for users
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
        
    if form.validate_on_submit(): #already in your code file
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html', title='Register', form=form)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/SEOTECHapp/SEOwebapp')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
@app.route("/") 
#associates a URL with a Python function - access the root URL '/'
#TODO: change this home directory to locate other pages as well
def home(): #the home function is defined
  return render_template('home.html', subtitle='Home Page')
#render_template takes the name of the template, subtitle, and text
# as args and renders it

@app.route('/name')
def index():
  return render_template('index.html', subtitile='Index Page')

@app.route('/about')
def about():
  return render_template('about.html', subtitile='About Page', text='This is the second page')


if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0") #this line is ran if 
    #checks if the code is being ran directly or as a module

    #in our current case it is being imported as module
