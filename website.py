''' Creation Date: 22/11/2022 '''

from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import InputRequired, Email, length
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from os import urandom, environ
from dotenv import load_dotenv
import smtplib, ssl
from email.mime.text import MIMEText
import redis

# Get .env variables
def get_environment(variable: str):
	''' Returns: Loaded .env file variable. '''
	return environ[variable]

# Setup Environment
csrf = CSRFProtect()
app = Flask(__name__)
app.config['WTF_CSRF_TIME_LIMIT'] = None
csrf.init_app(app)
try:
    app.secret_key = bytes(get_environment('SECRET'), encoding='utf-8')
except Exception:
    print('Warning: Found no app.secret_key, using random value...')
    app.secret_key = urandom(128)

# Load Projects JSON
class JSON:
    ''' Contents: Stores project data and associated methods. '''
    def __init__(self):
        with open('projects.json') as data:
            self.data = json.load(data)
    def get_constants(self):
        ''' Returns: Dictionary of project constant values. '''
        return self.data['constants']
    def get_projects(self):
        ''' Returns: Dictionary of all projects and values. '''
        return self.data['projects']
    def get_project(self, project: str):
        ''' Returns: Dictionary of project specific values. '''
        return self.data['projects'][project]
    def get_endpoints(self):
        ''' Returns: List of all project endpoints. '''
        return list(self.data['projects'].keys())

# Define cache
cache = redis.Redis(host='redis', port=6379, db=0)

# Set Limits
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['500 per day'],
    storage_uri='memory://'
)

# Email Setup
port = 465
smtp_server = 'smtp.gmail.com'
context = ssl.create_default_context()

# Home Route
@app.route('/')
@app.route('/home')
def home():
    Projects = JSON()
    constants = Projects.get_constants()
    projects = Projects.get_projects()
    return render_template('home.html', projects=projects, constants=constants)    

# About Route
@app.route('/about')
def about():    
    return render_template('about.html')  

# Project Routes
@app.route('/project/<endpoint>')
def project(endpoint: str):
    Projects = JSON()
    if endpoint in Projects.get_endpoints():
        constants = Projects.get_constants()
        project = Projects.get_project(endpoint)
        return render_template('project.html', project=project, constants=constants)
    else:
        return redirect(url_for('home'))  

# Contact Route
class ContactForm(FlaskForm):
    ''' Contents: All fields from the contact us page form. '''
    name = StringField('name', [
        InputRequired(message='Name is required...'), 
        length(max=60, message='Name must not exceed 60 characters...')
        ])
    email = EmailField('email', [
        InputRequired(message='Email is required...'), 
        Email(message='Email must contain a valid email...'),
        length(max=60, message='Email must not exceed 60 characters...')
        ])
    subject = StringField('subject', [
        InputRequired(message='Subject is required...'), 
        length(max=60, message='Subject must not exceed 60...')
        ])
    message = TextAreaField('message', [
        InputRequired(message='Message is required...'), 
        length(max=1000, message='Message must not exceed 1000 characters...')
        ])

class Email:
    ''' Contents: All email field values including user entered. '''
    def __init__(self, form: ContactForm):
        self.name = form.name.data
        self.email = form.email.data
        self.subject = form.subject.data
        self.text = form.message.data
        self.receiver = get_environment('RECEIVER')
        self.sender = get_environment('ACCOUNT')
        self.password = get_environment('APPPASSWORD')

def send_email(email: Email):
    ''' Purpose: Sends email to specified destination. '''
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email.sender, email.password)
        msg = MIMEText('From: %s\nEmail: %s\n\n%s' % (email.name, email.email, email.text))
        msg['Subject'] = email.subject
        msg['To'] = email.receiver
        server.sendmail(email.sender, email.receiver, msg.as_string())

def validate_form(form: ContactForm):
    ''' Purpose: Validate form inputs else raise error. '''
    if not form.validate_on_submit():
        for error in form.errors:
            flash(form.errors[error][0], 'alert-danger')
        raise ValueError('Invalid form inputs.')

@app.route("/contact" , methods=['GET'])
def contactus_get():
    return render_template('contact.html')

@app.route("/contact" , methods=['POST'])
@limiter.limit('20 per day')
def contactus_send():
    ip_address = request.remote_addr
    if not cache.exists(ip_address):
        cache.set(ip_address, 1, ex=86400)
        form = ContactForm()
        try:
            validate_form(form)
            send_email(Email(form))
            flash('Your message has been emailed!', 'alert-success')
        except Exception as error:
            print(error)
            cache.delete(ip_address)
            flash('Email failed, please try later...', 'alert-danger')       
    else:
        flash('Already emailed, please try later...', 'alert-danger')
    return render_template('contact.html')

# Error Handling
@app.errorhandler(404)
def not_found(_):
    return redirect(url_for('home'))

# Security Headers
@app.after_request
def add_header(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self';font-src 'self' fonts.gstatic.com;style-src 'self' fonts.googleapis.com;object-src 'none';img-src 'self' data: https://www.w3.org/2000/svg;require-trusted-types-for 'script'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response

if __name__ == "__main__":
    load_dotenv()   
    app.run(debug=True)
