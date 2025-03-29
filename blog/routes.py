from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required

from blog import app, db
from blog.forms import LoginForm, PostForm, RegistraForm
from blog.models import Post, User
import config
from blog.utils import save_post_picture, save_user_picture

@app.route('/')
def homepage():
    #print(config.Config.SECRET_KEY)
    page_number = request.args.get('page', 1, type=int)
    posts1 = Post.query.order_by(Post.created_at.desc()).paginate(page=page_number, per_page=5, error_out=True)

    posts =[]
    for post in posts1.items:
        utente = Post.query.get(post.user_id)
        utente_image = User.query.get(utente.id).image
        if utente_image :
            utente_image = '/static/img/users/' + utente_image
        else:
            utente_image = '/static/img/users/utente_none.jpg'
        posts.append((post, utente_image))


    if posts1.has_next:
        next_page = url_for('homepage', page=posts1.next_num)
    else:
        next_page = None

    if posts1.has_prev:
        previous_page = url_for('homepage', page=posts1.prev_num)
    else:
        previous_page = None 

    return render_template("homepage.html", posts=posts, current_page=page_number,
                           next_page=next_page, previous_page=previous_page)


@app.route("/create-post", methods=["GET", "POST"])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.body.data,
                        description=form.description.data, author=current_user)
        if form.image.data:
            try:
                image = save_post_picture(form.image.data)
                new_post.image = image
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=new_post.id))

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=new_post.id))
    return render_template("post_editor.html", form=form)

@app.route("/registra", methods=["GET", "POST"])
def user_create():
    form = RegistraForm()
    if form.validate_on_submit():
        if form.password.data != form.ripeti_password.data:
            flash("Le password non combaciano!")
            return  render_template("registra.html", form=form)
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            new_user = User(nome=form.nome.data, cognome=form.cognome.data,
                        username=form.username.data, email=form.email.data)
            new_user.set_password_hash(form.password.data)

            if form.image.data:
                try:
                    image = save_user_picture(form.image.data)
                    new_user.image = image
                except Exception:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                    return redirect(url_for('user_create'))
            try:
                db.session.add(new_user)
                db.session.commit()
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
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
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
                db.session.commit()
                flash("C'è stato un problema con l'upload dell'immagine. Cambia immagine e riprova.")    
                return redirect(url_for('post_update', post_id=post_instance.id))
        db.session.commit()
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
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route("/about")
def about():
    return render_template("about_page.html")

@app.route("/contact")
def contact():
    return render_template("contact_page.html")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post_instance = Post.query.get_or_404(post_id)
    return render_template("post_detail.html",post=post_instance)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
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