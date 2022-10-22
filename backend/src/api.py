from ast import JoinedStr
#from crypt import methods
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implemention of endpoint
    GET /drinks
        
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = [drinking.short() for drinking in Drink.query.all()]
    return jsonify(
        {
            'success': True,
            'drinks': drinks
        }
    )


'''
@TODO implemention of endpoints
    GET /drinks-detail
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = [drinking.short() for drinking in Drink.query.all()]
    return jsonify(
        {
            'success': True,
            'drinks': drinks
        }
    )


'''
@TODO implementing endpoints for 
    POST /drinks
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    drinks = request.get_json()
    new_title = drinks.get('title')
    new_recipe = drinks.get('recipe')
    recepe = json.dumps(new_recipe)

    responses = Drink(title=new_title, recipe=recepe)

    responses.insert()

    return jsonify({
        'success': True,
        'drinks': [drinking.long() for drinking in Drink.query.all()]
    })


'''
@TODO implemention of endpoint
    PATCH /drinks/<id>
    
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
    records = Drink.query.filter(Drink.id == id).one()

    if (records) == 0:
        abort(422)

    else:
        drinks = request.get_json()
        records.title = drinks.get('title')
        records.recipe = json.dumps(drinks.get('recipe'))

        #responses = Drink(title=new_title, recipe=recepe)

        records.update()

        return jsonify({
            'success': True,
            'drinks': [drinking.long() for drinking in Drink.query.all()]
        })


'''
@TODO implementing endpoints for
    DELETE /drinks/<id>
        
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleting_drinks(jwt, id):
    records = Drink.query.filter(Drink.id == id).one()

    if (records) == 0:
        abort(404)
    else:
        records.delete()

        return jsonify({
            'success': True,
            'delete': records.id
        })

    # Error Handling
'''
Examples of errors handling mechanisms for unprocessable entity list and other errors generated
'''


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "unprocessable Entity"
    }), 422


@app.errorhandler(403)
def forbidden_request(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'forbidden '

    }), 403


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found"
    }), 404


@app.errorhandler(401)
def resource_unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': "unauthorized access"
    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'sucess': False,
        'error': 500,
        'message': 'Internal server error, server not found'
    }), 500
