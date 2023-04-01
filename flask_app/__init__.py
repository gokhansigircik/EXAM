from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key = "exam"

bcrypt = Bcrypt(app) 
DATABASE = "belt_exam_db" 