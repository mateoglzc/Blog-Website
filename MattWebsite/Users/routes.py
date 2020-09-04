from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from MattWebsite import db, bcrypt
from MattWebsite.models import User, Post
from MattWebsite.Users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from MattWebsite.Users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unseccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    posts = current_user.posts
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='ProfilesPhotos/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, posts=posts)

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    posts = current_user.posts
    image_file = url_for('static', filename='ProfilesPhotos/' + current_user.image_file)
    return render_template('Profile.html', image_file=image_file, posts=posts)

@users.route("/user/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        print('hola')
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "alert-info")
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', "alert-info")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)