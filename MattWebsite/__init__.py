from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from MattWebsite import secret_code as sc


app = Flask(__name__)

#CHANGE THIS
app.config['SECRET_KEY'] = sc.SECRET_KEY
######


#Data Base

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# Here username and password as enviorenment variables

app.config['MAIL_USERNAME'] = sc.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = sc.MAIL_PASSWORD



# Initialize our extension
mail = Mail(app)




from MattWebsite import routes
