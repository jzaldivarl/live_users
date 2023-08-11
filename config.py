import os

class DevConfig():
    DEBUG = True
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/app/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False