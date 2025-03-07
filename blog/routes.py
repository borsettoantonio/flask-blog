from flask import render_template
from blog import app

@app.route('/')
def homepage():
    posts = [{"title": "primo post", "body": "random body"},
             {"title": "secondo post", "body": "more random body"}]
    some_boolean_flag = True
    return render_template("homepage.html", posts=posts, 
                           boolean_flag=some_boolean_flag)

@app.route("/about")
def about():
    return render_template("about_page.html")