from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User, Device
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, PedForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Great day to be in the office!'
        },
        {
            'author': {'username': 'Sheraz'},
            'body': 'I love working for Valitor!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/ped', methods=['GET', 'POST'])
@login_required
def ped():
    if current_user.is_authenticated:
        form = PedForm()
        if form.validate_on_submit():
            device = Device(terminal=form.terminal.data, serial=form.serial.data, model=form.model.data,
                            delivered_to_customer=form.delivered_to_customer.data,
                            date_delivered=form.date_delivered.data,
                            returned_to_logistics=form.returned_to_logistics.data,
                            date_returned=form.date_returned.data)
            db.session.add(device)
            db.session.commit()
            flash('Submission for device with serial {}'.format(form.serial.data))
            return redirect(url_for('index'))
        return render_template('ped.html', title='Submit', form=form)

# @app.route('/index')
# @login_required
# def search():
#     if current_user.is_authenticated:
#         results = []
#         search_string = search.data['search']
#
#         if search.data['search'] == '':
#             qry = db_session.query(serial)
#             results = qry.all()
#
#         elif not results:
#             flash('No results found')
#             return redirect(url_for('index'))
#
#         else:
#
#             return render_template('results.html', results=results)