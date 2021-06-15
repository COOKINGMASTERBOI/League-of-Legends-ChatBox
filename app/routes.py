# 从app模块中即从__init__.py中导入创建的app应用
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm

# 建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('personal_page'))  # 之后改成personal page

    form = LoginForm()

    # 对表格数据进行验证
    if form.validate_on_submit():

        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()

        # 判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')

            # 然后重定向到登录页面
            return redirect(url_for('login'))

        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)

        # # 此时的next_page记录的是跳转至登录页面是的地址
        # next_page = request.args.get(url_for('personal_page'))  # 应该是个人首页？
        #
        # # 如果next_page记录的地址不存在那么就返回首页
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('home')
        #
        # # 综上，登录后要么重定向至跳转前的页面，要么跳转至首页
        return render_template('personal_page.html', user=current_user)

    return render_template('login.html', title='Login', form=form, user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_required
@app.route('/personal_page', methods=['GET', 'POST'])
def personal_page():
    if request.method == 'POST':
        post = request.form.get('post')

        if len(post) < 1:
            flash('Post is too short!', category='error')
        else:
            new_post = Post(body=post, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')

    return render_template('personal_page.html', user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():

    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a member of ChatBox')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    post_list = Post.query.all()
    return render_template('explore.html', user=current_user, post_list=post_list)


@app.route('/comment/<postId>', methods=['GET', 'POST'])
@login_required
def comment(postId):
    if request.method == 'POST':
        comm = request.form.get('comment')
        if len(comm) == 0:
            flash('Comment is too short!', category='error')
        else:
            post = db.session.query(Post).get(postId)
            comm += ";"
            if post.comment is not None:
                post.comment += comm
            else:
                post.comment = comm
            db.session.commit()
            flash('Comment added!', category='success')
    return render_template('comment.html', user=current_user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    user_list = db.session.query(User).all()
    post_list = db.session.query(Post).all()
    return render_template("search.html", user=current_user, user_list=user_list, post_list=post_list)