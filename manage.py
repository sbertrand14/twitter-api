# manage.py

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#from wsgi import create_app
from app import db, create_app

application = create_app()

migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
