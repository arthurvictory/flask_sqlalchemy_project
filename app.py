# Task 1 Setting up Flask with Flask-SQLAlchemy
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mp261Vk823!@localhost/fitness_center_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define Members Schema
class MembersSchema(ma.Schema):
    
    name = fields.String(required = True)
    age = fields.String(required = True)

    class Meta:
        fields = ("name", "age", "id")

member_schema = MembersSchema()
members_schema = MembersSchema(many = True)

# Define workout schema
class SessionSchema(ma.Schema):
    session_id = fields.Integer(required = True)
    member_id = fields.String(required = True)
    session_date = fields.String(required = True)
    duration_minutes = fields.String(required = True)
    calories_burned = fields.String(required = True)

    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'duration_minutes', 'calories_burned',)

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)


class Members(db.Model):
    __tablename__ = 'Members'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    age = db.Column(db.String(25))

class WorkoutSession(db.Model):
    __tablename__ = 'Workoutsessions'
    session_id = db.Column(db.Integer, primary_key = True)
    session_date = db.Column(db.String(255), nullable = False)
    duration_minutes = db.Column(db.String(25))
    calories_burned = db.Column(db.String(25))
    member_id = db.Column(db.Integer, db.ForeignKey('Members.id'), nullable = False)

# Task 2 create CRUD ops for members
@app.route('/members', methods = ['GET'])
def get_members():
    members = Members.query.all()
    return members_schema.jsonify(members)

@app.route('/members', methods = ['POST'])
def add_members():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Members(id = member_data['id'], name = member_data['name'], age = member_data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "New member added successfully"}), 201

@app.route("/members/<int:id>", methods=["PUT"])
def update_members(id):
    member = Members.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.name = member_data['name']
    member.age = member_data['age']
    db.session.commit()
    return jsonify({"message": "Member details have updated successfully"}), 200

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_members(id):
    member = Members.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member has been deleted successfully"}), 200

# Task 3 create CRUD ops for workout sessions
@app.route('/workoutsessions', methods=['GET'])
def display_workouts():
    workouts = WorkoutSession.query.all()
    return sessions_schema.jsonify(workouts)

@app.route('/workoutsessions', methods = ['POST'])
def add_workout():
    try:
        workout_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_workout = WorkoutSession(session_id = workout_data['session_id'], member_id = workout_data['member_id'], session_date = workout_data['session_date'], duration_minutes = workout_data['duration_minutes'], calories_burned = workout_data['calories_burned'])
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({"message": "New member added successfully"}), 201

@app.route('/workoutsessions/<int:member_id>', methods=['PUT'])
def update_workout(member_id):
    workouts = WorkoutSession.query.get_or_404(member_id)
    try:
        workout_data = session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    workouts.session_date = workout_data['session_date']
    workouts.duration_minutes = workout_data['duration_minutes']
    workouts.calories_burned = workout_data['calories_burned']

    db.session.commit()
    return jsonify({"message": "Workout details were successfully updated"})

# Initialize the database and create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug = True)