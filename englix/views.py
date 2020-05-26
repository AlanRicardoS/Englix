from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from .models import User, Lesson, Activity, Quiz, Answer, RoleType
from app import db

englix = Blueprint('englix', __name__)

class NewModelView(ModelView):
    def is_accessible(self):
      if current_user.role_type == RoleType.Student: 
         return abort(404)
      else:
         return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)

class NewAdminIndexView(AdminIndexView):
    def is_accessible(self):
      if current_user.role_type == RoleType.Student: 
         return abort(404)
      else:
         return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


# -------------------------------------------------------------------------------------- #

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


# -------------------------------------------------------------------------------------- #

@englix.route('/index')
def index():
   if current_user.is_authenticated:
      return redirect(url_for('englix.home'))
   return render_template('Index.html')

@englix.route('/home')
@login_required
def home():
   user_name = current_user.name
   return render_template('home.html', name=user_name)

@englix.route('/lessons')
@login_required
def lessons(): 
   user_name = current_user.name
   user_level = current_user.level_type
   return render_template('lessons.html', lessons=Lesson.query.filter_by(level_type=user_level).all(), name=user_name)


@englix.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
   user_name = current_user.name
   return render_template('lesson.html', lesson=Lesson.query.filter_by(id=lesson_id).first(), name=user_name)

@englix.route('/AR/<string:file>')
@login_required
def AR(file):
   user_name = current_user.name
   
   return render_template('/AR/'+file, name=user_name)

