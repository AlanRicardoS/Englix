from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from .models import User
from app import db

englix = Blueprint('englix', __name__)

@englix.route('/login')
def login():
    return render_template('login.html')

@englix.route('/login', methods=['POST'])
def login_post():
   email = request.form['email']
   password = request.form['password']

   remember = True if request.form.get('remember') else False

   user = User.query.filter_by(email=email).first()

   if not user and not check_password_hash(user.password, password):
      return redirect(url_for('englix.login'))
   
   login_user(user, remember=remember)

   return redirect(url_for('englix.home'))

@englix.route('/signup') 
def signup():
    return render_template('cadastro.html')

@englix.route('/signup', methods=['POST'])
def signup_post():

   email = request.form['email']
   name = request.form['name']
   password = request.form['password']

   user = User.query.filter_by(email=email).first()

   if user:
      flash('Email adress already exists.')
      return redirect(url_for('englix.login'))

   new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

   db.session.add(new_user)
   db.session.commit()
   
   return redirect(url_for('englix.login'))


@englix.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('englix.index'))

@englix.route('/index')
def index():
    return render_template('Index.html')

@englix.route('/home')
@login_required
def home():
   user_name = current_user.name
   return render_template('home.html', name=user_name)
