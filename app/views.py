from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Role, Post
from datetime import datetime

@app.route('/')
@app.route('/index')
##user must be logged in to view this page.
#@login_required
def index():
    #get page number from url. If no page number use page 1
    page = request.args.get('page',1,type=int)
    #return page number and how per page.
    #True means 404 error is returned if page is out of range. False means an empty list is returned
    #paginate returns a Pagination object
    posts = Post.query.order_by(Post.timestamp.desc()) \
        .paginate(page,app.config['POSTS_PER_PAGE'],False)

    #Python ternary operator
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html',posts=posts.items, \
        next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        #username/password is valid. sets current_user to the user
        login_user(user, remember=form.remember_me.data)

        #where was the user trying to get to? after user logs in redirect him back to the page he was going
        next_page = request.args.get('next')

        #in case url is absolute we will ignore, we only want a relative url
        #netloc returns the www.website.com part
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    #returns a user if not it returns 404 to browser
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        #copy the form to the user object and write to db
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        #access this route with a get request then return current user database
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    #also if is post request but validation faied then just go back to webpage.
    #wtforms will display the errors.
    return render_template('edit_profile.html',form=form)

@app.route('/add_post',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published!')
        return redirect(url_for('index'))
    return render_template('add_post.html',form=form)

#checks this before any function, updates last seen with current time
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
