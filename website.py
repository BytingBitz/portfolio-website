''' Creation Date: 22/11/2022 '''

from flask import Flask,render_template,request,flash
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import InputRequired, Email, length
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter, RateLimitExceeded
from flask_limiter.util import get_remote_address
from os import urandom

csrf = CSRFProtect()
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(128)
app.config['WTF_CSRF_TIME_LIMIT'] = None
csrf.init_app(app)
app.secret_key = b'test'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["500 per day"],
    storage_uri="memory://",
)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')    

@app.route("/about")
def about():    
    return render_template('about.html')  

@app.route("/portfolio/work")
def work():    
    return render_template('portfolio/work.html')  

# @app.route("/portfolio/workdetail")
# def workdetail():    
#     return render_template('portfolio/workdetail.html') 

class ContactForm(FlaskForm):
    ''' Contents: All fields from the contact us page form. '''
    name = StringField('name', [InputRequired(), length(max=32)])
    email = EmailField('email', [InputRequired(), Email()])
    subject = StringField('subject', [InputRequired(), length(max=1)])
    message = TextAreaField('message', [InputRequired(), length(max=1)])

class Email:
    def __init__(self, form: ContactForm):
        self.name = form.name.data
        self.email = form.email.data
        self.subject = form.subject.data
        self.message = form.message.data

@app.route("/contact" , methods=['GET' , 'POST'])
def contactus():  
    if request.method == 'POST':
        form = ContactForm()
        if form.validate_on_submit():
            try:
                with limiter.limit("2 per week"):    
                    email = Email(form)
                    flash('Your message has been sent!')
            except RateLimitExceeded:
                flash('You have sent to many emails.')       
        else:
            flash(form.errors)
    return render_template('contact.html')       

if __name__ == "__main__":  
    app.run(debug=True)
   