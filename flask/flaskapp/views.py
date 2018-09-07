import os
from sqlalchemy import and_, or_
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db
from flaskapp.forms import RegisterForm, LoginForm, UpdateProfileForm, PostForm
from flaskapp.models import User, Post,followers
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    posts =Post.query.order_by(Post.date_posted.desc()).filter_by(post_type ='public').all()
    return render_template('home.html', posts=posts)


@app.route("/signup", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong Username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(image):
    picture_path = os.path.join(app.root_path, 'static/profile_pics', image.filename)
    img_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(img_size)
    i.save(picture_path)
    return image.filename


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    posts = Post.query.order_by(Post.date_posted.desc()).filter_by(user_id = current_user.id).all()
    form = PostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            post_img = save_post_img(form.post_image.data)
        else:
            post_img = None

        post = Post(content=form.content.data, post_image=post_img, post_type=form.post_type.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('profile.html', title='Profile', form = form,user=current_user, posts=posts)


@app.route("/profile/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('profile'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('edit_profile.html', title='Profile',
                           image_file=image_file, form=form,user=current_user)

def save_post_img(image):

    post_img_path = os.path.join(app.root_path, 'static/post_imgs', image.filename)
    img_size = (500, 500)
    i = Image.open(image)
    i.thumbnail(img_size)
    i.save(post_img_path)

    return image.filename


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            post_img = save_post_img(form.post_image.data)
        else:
            post_img = None
        post = Post(content=form.content.data,post_image = post_img, post_type=form.post_type.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            post.post_image = save_post_img(form.post_image.data)
        post.content = form.content.data
        post.post_type = form.post_type.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home', post_id=post.id))
    form.post_image.data = post.post_image
    form.content.data = post.content
    form.post_type.data = post.post_type
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/allusers")
@login_required
def all_users():
    users = User.query.order_by(User.username).all()
    return render_template('all_users.html', title='Users', users=users, legend='All Users')

@app.route("/user/<int:user_id>")
@login_required
def user(user_id):

    user = User.query.get_or_404(user_id)
    if user_id == current_user.id:
        return redirect(url_for('profile'))
    following = User.is_following(current_user,user)
    if following:
        posts = db.session.query(Post).order_by(Post.date_posted.desc()).filter(and_(Post.user_id == user.id,(or_(
            Post.post_type == 'public', Post.post_type == 'protected'))))
    else:
        posts = db.session.query(Post).order_by(Post.date_posted.desc()).filter(and_(Post.user_id == user.id,
            Post.post_type == 'public'))
    return render_template('user.html', user=user, posts=posts, following=following)


@app.route("/user/<int:user_id>/follow", methods=['GET', 'POST'])
@login_required
def follow(user_id):
    user2 = User.query.get_or_404(user_id)
    current_user.followed.append(user2)
    db.session.commit()
    return redirect(url_for('user', user_id=user_id))


@app.route("/user/<int:user_id>/unfollow", methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    user2 = User.query.get_or_404(user_id)
    current_user.followed.remove(user2)
    db.session.commit()
    return redirect(url_for('user', user_id=user_id))

@app.route("/followings")
@login_required
def followings():
    users = User.query.join(followers, (followers.c.followed_id == User.id)).filter(
        followers.c.follower_id == current_user.id)



    return render_template('all_users.html', title='Followings',
                           users=users, legend='Followings')


# @app.route("/followers")
# @login_required
# def followers():
#     users = User.query.join(followers, (followers.c.follower_id == User.id)).filter(
#         followers.c.followed_id == current_user.id)
#
#
#
#     return render_template('all_users.html', title='Followers',
#                            users=users, legend='Followers')
#


