from flask_script import Manager
from organisation_api.main import app
import subprocess  # noqa: F401
import os

from flask_migrate import Migrate, MigrateCommand
from organisation_api.models import Organisation  # noqa: F401
from organisation_api.extensions import db
migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def runserver(port=9998):
    """Run the app using flask server"""

    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"

    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    manager.run()
