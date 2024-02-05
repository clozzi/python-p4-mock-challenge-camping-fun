#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)

@app.route('/')
def home():
    return 'Home for Campers'
# api.add_resource(Home, '/')

@app.route('/campers', methods=['GET', 'POST'])
def campers():

    if request.method == 'GET':

        campers = Camper.query.all()
        camper_data = []
        for camper in campers:
            camper = {
                'id': camper.id,
                'name': camper.name,
                'age': camper.age
            }
            camper_data.append(camper)

        return camper_data, 200
    
    elif request.method == 'POST':

        name = request.json.get('name')
        age = request.json.get('age')

        try:
            new_camper = Camper(
                name = name,
                age = age
            )

            db.session.add(new_camper)
            db.session.commit()

            return new_camper.to_dict(), 201
        
        except:

            return {'errors': ['validation errors']}, 400

@app.route('/campers/<int:id>', methods=['GET', 'PATCH'])
def campers_by_id(id):

    camper = Camper.query.filter(Camper.id == id).first()

    if camper:

        if request.method == 'GET':
            return make_response(camper.to_dict(), 200)
        
        elif request.method == 'PATCH':
            form_data = request.get_json()
            try:
                for attr in form_data:
                    setattr(camper, attr, form_data.get(attr))

                db.session.commit()

                response = make_response(camper.to_dict(), 202)

                return response
            
            except ValueError:
                response = make_response({'errors': ['validation errors']}, 400)

                return response

    else:
        return make_response({'error': 'Camper not found'}, 404)


@app.route('/activities')
def activities():

    activities = [activity.to_dict() for activity in Activity.query.all()]
    return activities, 200

@app.route('/activities/<int:id>', methods=['GET', 'DELETE'])
def activities_by_id(id):

    activity = Activity.query.filter(Activity.id == id).first()
    
    if activity:
        if request.method == 'GET':
            return make_response(activity, 200)
        
        elif request.method == 'DELETE':
            db.session.delete(activity)
            db.session.commit()

            return make_response({}, 204)

    return {'error': 'Activity not found'}, 404

@app.route('/signups', methods=['POST'])
def signup():

    camper_id = request.json.get('camper_id')
    activity_id = request.json.get('activity_id')
    time = request.json.get('time')

    try:
        new_signup = Signup(
            camper_id = camper_id,
            activity_id = activity_id,
            time = time        
        )

        db.session.add(new_signup)
        db.session.commit()

        return new_signup.to_dict(), 201
    
    except:

        return {'errors': ['validation errors']}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
