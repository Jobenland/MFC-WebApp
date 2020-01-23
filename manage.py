from flask_script import Manager
from app import create_app, db


manager = Manager(create_app)


@manager.command
def createdb(drop_first=False):
    """Creates the database."""
    if drop_first:
        db.drop_all()
    db.create_all()

#additional run options given in CLI. NOT HERE
if __name__ == '__main__':
    manager.run()
