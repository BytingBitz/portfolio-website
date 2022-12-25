''' Creation Date: 22/11/2022 '''

from flask import Flask,render_template,request,flash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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

@app.route("/contact" , methods=['GET' , 'POST'])
def contactus():  
    if request.method == 'POST':    
        flash(' Your message has been sent!')        
        return render_template('contact.html')
    return render_template('contact.html')       

if __name__ == "__main__":  
    app.run(debug=True)
   