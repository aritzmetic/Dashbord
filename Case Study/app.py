from flask import Flask, render_template
from works import create_dash_app 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")  

@app.route("/enrollment") 
def enrollment():
    return render_template("enrollment.html")  

dash_app = create_dash_app(app)

if __name__ == "__main__":
    app.run(debug=True)
