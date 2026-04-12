from flask import Flask, request, make_response
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema, workout_exercise_schema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return make_response({"message": "Welcome to the Workout Tracker API!"}, 200)


@app.route("/workouts")
def get_workouts():
    return make_response(workouts_schema.dump(Workout.query.all()), 200)


@app.route("/workouts/<int:id>")
def get_workout(id):
    workout = db.session.get(Workout, id)
    return make_response(workout_schema.dump(workout), 200) if workout else make_response({"error": "Not found"}, 404)


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        workout = workout_schema.load(request.json)
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except Exception as e:
        return make_response({"error": str(e)}, 422)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response({"error": "Not found"}, 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


@app.route("/exercises")
def get_exercises():
    return make_response(exercises_schema.dump(Exercise.query.all()), 200)


@app.route("/exercises/<int:id>")
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    return make_response(exercise_schema.dump(exercise), 200) if exercise else make_response({"error": "Not found"}, 404)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        exercise = exercise_schema.load(request.json)
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except Exception as e:
        return make_response({"error": str(e)}, 422)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response({"error": "Not found"}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    if not db.session.get(Workout, workout_id) or not db.session.get(Exercise, exercise_id):
        return make_response({"error": "Not found"}, 404)
    data = request.json or {}
    we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    db.session.add(we)
    db.session.commit()
    return make_response(workout_exercise_schema.dump(we), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)