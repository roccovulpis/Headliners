from flask import Flask, render_template
app = Flask(__name__)

#Secret key, not sure what for but it is in the lab2 code! N.S.
app.secret_key = 'Fire Breathing Rubber Duckies'

@app.route("/")

#Runs the page
def home():
    #Calls the homepage template to format the webpage
    return render_template("homepage.html")

#Runs the app (Website)
if __name__ == '__main__':
    app.run()