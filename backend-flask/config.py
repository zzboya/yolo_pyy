import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'infos.db')
    ROOT_PATH = basedir
    STATIC_FOLDER = os.path.join(
        basedir, 'processor//imagesbig//')
    TEMPLATE_FOLDER = os.path.join(basedir, 'app//View//templates')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
