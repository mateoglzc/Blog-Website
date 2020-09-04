from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

#CHANGE THIS
app.config['SECRET_KEY'] = 'ad15a7e74cae2a04a436d996579c50f9'
######


#Data Base

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
# Here username and password as enviorenment variables

app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''



# Initialize our extension
mail = Mail(app)




from MattWebsite import routes
