from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required

#from blog import app, db
from blog import app
from blog.forms import LoginForm, PostForm, RegistraForm
from blog.models import Post, User
import config
from blog.utils import save_post_picture, save_user_picture
import os

from blog.data import *

@app.route('/')
def homepage():
    #print(config.Config.SECRET_KEY)
    page_number = request.args.get('page', 1, type=int)
        
    posts1, has_prev_page ,has_next_page  = get_post_page(page=page_number, per_page=5)
    posts =[]
    for post in posts1:
        if post.image :
            post.image = '/static/img/posts/' +  post.image
        else:
            post.image = '/static/img/users/utente_none.jpg'
        posts.append((post, post.image))

    if has_next_page:
        next_page = url_for('homepage', page=page_number+1)
    else:
        next_page = None

    if has_prev_page:
        previous_page = url_for('homepage', page=page_number-1)
    else:
        previous_page = None 

    return render_template("homepage.html", posts=posts, current_page=page_number,
                           next_page=next_page, previous_page=previous_page)


# login di prova:
# admin    pippo
# mario    mario


@app.route("/create-post", methods=["GET", "POST"])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post()
        new_post.title=form.title.data
        new_post.description=form.description.data
        new_post.body=form.body.data
        new_post.markdown=form.markdown.data 
        new_post.user_id=current_user.id
        


        if form.image.data:
            try:
                image = save_post_picture(form.image.data)
                new_post.image = image
            except Exception:
                post_insert(new_post)
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=new_post.id))
        else:
            new_post.image = None

        new_id = post_insert(new_post)
        return redirect(url_for('post_detail', post_id=new_id))
    return render_template("post_editor.html", form=form)


@app.route("/registra", methods=["GET", "POST"])
def user_create():
    form = RegistraForm()
    if form.validate_on_submit():
        if form.password.data != form.ripeti_password.data:
            flash("Le password non combaciano!")
            return  render_template("registra.html", form=form)
        user = get_user(form.username.data)

        if user == None:
            new_user = User()
            new_user.nome=form.nome.data
            new_user.cognome=form.cognome.data
            new_user.username=form.username.data
            new_user.email=form.email.data      
            
            new_user.set_password_hash(form.password.data)

            if form.image.data:
                try:
                    image = save_user_picture(form.image.data)
                    new_user.image = image
                except Exception:
                    user_insert(new_user)
                    flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                    return redirect(url_for('user_create'))
            try:
                user_insert(new_user)
            except Exception as e:
                flash(e.orig.args[0])   
                return render_template("registra.html", form=form) 
        else:
            flash("Username già esistente!")
            return render_template("registra.html", form=form)
        return redirect(url_for('homepage'))
    return render_template("registra.html", form=form) 

@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post_instance = get_post(post_id)
    if post_instance == None:
        abort(404)
    if post_instance.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body = form.body.data
        post_instance.markdown = form.markdown.data
        if form.image.data:
            try:
                image = save_post_picture(form.image.data)
                post_instance.image = image
            except Exception:
                upadate_post(post)
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=post_instance.id))
        upadate_post(post_instance)
        return redirect(url_for('post_detail', post_id=post_instance.id))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body.data = post_instance.body
        form.markdown.data = post_instance.markdown
    return render_template("post_editor.html", form=form) 


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post_instance = get_post(post_id)
    if post_instance == None:
        abort(404)
    if post_instance.user_id != current_user.id:
        abort(403)
    try:
        #raise Exception("errore")
        if post_instance.image:
            image=app.root_path + "/static/img/posts/" + post_instance.image
            image = os.path.normpath(image)
            #print(image)
            #image = os.path.join('D:/ProvePython/CorsoFlask/FLASK-BLOG/blog' , post_instance.image)
            os.remove(image)

    except Exception as err:
        return render_template("errore.html", err=err, image = image)

    delete_post(post_id)   
    
    return redirect(url_for('homepage'))


@app.route("/about")
def about():
    return render_template("about_page.html")

@app.route("/contact")
def contact():
    return render_template("contact_page.html")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post_instance = get_post(post_id)
    if post_instance == None:
        abort(404)
    if post_instance.image :
        post_instance.image = 'img/posts/' +  post_instance.image
    else:
        post_instance.image = 'img/users/utente_none.jpg'
    user = get_user_by_id(post_instance.user_id)
    image ='img/users/' +  user.image
    return render_template("post_detail.html",post=post_instance, user=user,image=image)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user =  get_user(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('username e password non combaciano!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# form di prova
@app.route("/prova")
def prova():
    form = PostForm()
    if form.validate_on_submit():
        return redirect(url_for('prova')) 
    return render_template("prova.html", form=form)

# form di errore
@app.route("/errore")
def errore(exception):
    form = LoginForm()
    return render_template("prova.html", form=form)