from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sozia.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)


  
#Index Page
@app.route("/")
def index():    
    return render_template('index.html')    

#About Page
@app.route("/about")
def about():    
    return render_template('about/about.html')  


####PORTFOLIO######

#Work
@app.route("/portfolio/work")
def work():    
    return render_template('portfolio/work.html')  

#Work Details
@app.route("/portfolio/workdetail")
def workdetail():    
    return render_template('portfolio/workdetail.html') 
    
    
#####CONTACT#########

class Contactus(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.email} - {self.subject} - {self.message}"

@app.route("/contact" , methods=['GET' , 'POST'])
def contactus():  
    if request.method == 'POST':  
        name= request.form.get('name')
        email= request.form.get('email')
        subject= request.form.get('subject')
        message= request.form.get('message')
        contactus = Contactus(name=name , email=email , subject=subject , message=message)   
        db.session.add(contactus)
        db.session.commit()  
        flash(' Your response has been successfully saved. We will contact you soon.')        
        return render_template('contact/contact.html')
            
    contactus = Contactus.query.all()
    return render_template('contact/contact.html',contactus=contactus)       

if __name__ == "__main__":  
    app.run(debug=True)     