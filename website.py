from os import urandom
from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import json

csrf = CSRFProtect()
app = Flask(__name__)
app.config['WTF_CSRF_TIME_LIMIT'] = None
csrf.init_app(app)
app.secret_key = urandom(128)


class Content:

    def __init__(self):
        with open('projects.json') as data:
            self.data = json.load(data)

    def get_constants(self):
        return self.data['constants']

    def get_projects(self):
        return self.data['projects']

    def get_project(self, selected_project: str):
        return self.data['projects'][selected_project]

    def get_endpoints(self):
        return list(self.data['projects'].keys())


@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    projects = Content()
    constants = projects.get_constants()
    projects = projects.get_projects()
    return render_template('home.html', projects=projects, constants=constants)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/project/<endpoint>', methods=['GET'])
def project(endpoint: str):
    projects = Content()
    if endpoint in projects.get_endpoints():
        constants = projects.get_constants()
        selected_project = projects.get_project(endpoint)
        return render_template('project.html', project=selected_project, constants=constants)
    else:
        return redirect(url_for('home'))


@app.route("/contact", methods=['GET'])
def contactus_get():
    return render_template('contact.html')


@app.errorhandler(404)
def not_found(_):
    return redirect(url_for('home'))


@app.after_request
def add_header(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self';font-src 'self' fonts.gstatic.com;style-src 'self' "
        "fonts.googleapis.com;object-src 'none';img-src 'self' data: "
        "https://www.w3.org/2000/svg;require-trusted-types-for 'script'"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response


if __name__ == "__main__":
    print('WARNING: Beginning debug Flask session...')
    app.run(debug=True)
