from flask import Blueprint, Response, request, current_app
import json
from jsonschema import validate


from organisation_api.models import Organisation, get_organisation


# This a blueprint object that gets registered into the app in blueprints.py.
organisation_name = Blueprint('organisation_name', __name__)


@organisation_name.route("/organisation-name/<organisation_id>", methods=['GET'])
def get_organisation_name(organisation_id):
    result = get_organisation(organisation_id)
    if result.count() > 0:
        current_app.logger.info('Returned name for organisation %s' % organisation_id)
        return Response(response=json.dumps({
            'organisation_name': result[0].organisation_name
        }), mimetype='application/json', status=200)
    else:
        current_app.logger.info('Could not find organisation %s' % organisation_id)
        return Response(response=json.dumps({
            'organisation_name': 'not found'
        }), mimetype='application/json', status=404)


@organisation_name.route("/organisation-name", methods=['POST'])
# For use by tests and DevOps to manage databases if necessary.
# Not called by a production service at the time of writing.
def post_organisation_name():
    organisation_json = request.get_json()

    schema = {
        "type": "object",
        "required": ["organisation_id", "organisation_name"],
        "properties": {
            "organisation_id": {
                "type": "string"
            },
            "organisation_name": {
                "type": "string"
            }
        }
    }

    validate(organisation_json, schema)
    new_organisation = Organisation()
    new_organisation.organisation_id = organisation_json['organisation_id']
    new_organisation.organisation_name = organisation_json['organisation_name']
    new_organisation.save()
    current_app.logger.info('Added organisation %s' % organisation_json['organisation_id'])
    return Response(response=json.dumps({
        'path': '/organisation-name/%s' % new_organisation.organisation_id
    }), mimetype='application/json', status=201)


@organisation_name.route("/organisation-name/<organisation_id>", methods=['DELETE'])
# For use by tests and DevOps to manage databases if necessary.
# Not called by a production service at the time of writing.
def delete_organisation_name(organisation_id):
    name = ''
    result = get_organisation(organisation_id)
    if result.count() > 0:
        for organisation in result:
            name = organisation.organisation_name
            organisation.delete()
            current_app.logger.info('Deleted organisation %s' % organisation_id)
        return Response(response=json.dumps({
            'organisation_name': name
        }), mimetype='application/json', status=200)
    else:
        current_app.logger.info('Could not find organisation %s' % organisation_id)
        return Response(response=json.dumps({
            'organisation_name': 'not found'
        }), mimetype='application/json', status=404)
