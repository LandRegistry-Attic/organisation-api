# Import every blueprint file
from organisation_api.views import general, organisation_name


def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(organisation_name.organisation_name)

    # All done!
    app.logger.info("Blueprints registered")
