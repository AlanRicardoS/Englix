from flask import Blueprint

englixBP = Blueprint('englix', __name__)

@englixBP.route('/')
def index():
   return "Hello World"
