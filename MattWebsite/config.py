from MattWebsite import secret_code as sc

class Config():
    SECRET_KEY = sc.SECRET_KEY

    #Data Base
    SQLALCHEMY_DATABASE_URI = sc.DATA_BASE

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # Here username and password as enviorenment variables

    MAIL_USERNAME = sc.MAIL_USERNAME
    MAIL_PASSWORD = sc.MAIL_PASSWORD