from flask import Blueprint

from .models import Student
from app import db

englix = Blueprint('englix', __name__,  url_prefix='/englix')

@englix.route('/')
def index():
   return "Hello World"
