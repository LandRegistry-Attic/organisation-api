from flask import request, Blueprint, Response, jsonify, current_app
import json

# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_list(),
        "commit": current_app.config["COMMIT"]
    }),  mimetype='application/json', status=200)


@general.route("/health/service-check")
def service_check_routes():

    # If we can hit this route, we can confirm that the connection is established
    service_list = {
        "status_code": 200,
        "service_from": "deed-api",
        "service_to": "organisation-api",
        "service_message": "Successfully connected"
    }

    return jsonify(service_list)
