from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "this a secret"

bcrypt = Bcrypt(app)

DATABASE = "login_reg_schema"

from flask_app.controllers import controller_user, controller_route