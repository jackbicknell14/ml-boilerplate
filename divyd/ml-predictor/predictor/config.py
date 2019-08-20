import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = '22a9b2484150dd4f5f46457755fa6ce2'
	# Database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
