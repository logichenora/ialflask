import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Bubbol0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://ial:ial@localhost:5432/ialflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False