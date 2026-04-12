import pytest
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def seed(client):
    with app.app_context():
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()
        e = Exercise(name="Push Ups", category="strength", equipment_needed=False)
        w = Workout(date=date(2024, 1, 1), duration_minutes=30, notes="Test")
        db.session.add_all([e, w])
        db.session.commit()
        db.session.add(WorkoutExercise(workout_id=w.id, exercise_id=e.id, sets=3, reps=10))
        db.session.commit()


# Workout tests
def test_get_workouts(client, seed):
    r = client.get("/workouts")
    if r.status_code != 200:
        raise Exception(f"Expected 200 but got {r.status_code}")

def test_get_workout_by_id(client, seed):
    r = client.get("/workouts/1")
    if r.status_code != 200:
        raise Exception(f"Expected 200 but got {r.status_code}")

def test_get_workout_not_found(client):
    r = client.get("/workouts/999")
    if r.status_code != 404:
        raise Exception(f"Expected 404 but got {r.status_code}")

def test_create_workout(client):
    r = client.post("/workouts", json={"date": "2024-06-01", "duration_minutes": 45})
    if r.status_code != 201:
        raise Exception(f"Expected 201 but got {r.status_code}")

def test_create_workout_invalid_duration(client):
    r = client.post("/workouts", json={"date": "2024-06-01", "duration_minutes": -5})
    if r.status_code != 422:
        raise Exception(f"Expected 422 but got {r.status_code}")

def test_delete_workout(client, seed):
    r = client.delete("/workouts/1")
    if r.status_code != 204:
        raise Exception(f"Expected 204 but got {r.status_code}")


# Exercise tests
def test_get_exercises(client, seed):
    r = client.get("/exercises")
    if r.status_code != 200:
        raise Exception(f"Expected 200 but got {r.status_code}")

def test_get_exercise_by_id(client, seed):
    r = client.get("/exercises/1")
    if r.status_code != 200:
        raise Exception(f"Expected 200 but got {r.status_code}")

def test_get_exercise_not_found(client):
    r = client.get("/exercises/999")
    if r.status_code != 404:
        raise Exception(f"Expected 404 but got {r.status_code}")

def test_create_exercise(client):
    r = client.post("/exercises", json={"name": "Running", "category": "cardio"})
    if r.status_code != 201:
        raise Exception(f"Expected 201 but got {r.status_code}")

def test_create_exercise_invalid_category(client):
    r = client.post("/exercises", json={"name": "X", "category": "badcat"})
    if r.status_code != 422:
        raise Exception(f"Expected 422 but got {r.status_code}")

def test_delete_exercise(client, seed):
    r = client.delete("/exercises/1")
    if r.status_code != 204:
        raise Exception(f"Expected 204 but got {r.status_code}")


# WorkoutExercise tests
def test_add_exercise_to_workout(client, seed):
    r = client.post("/workouts/1/exercises/1/workout_exercises", json={"sets": 3, "reps": 10})
    if r.status_code != 201:
        raise Exception(f"Expected 201 but got {r.status_code}")

def test_add_exercise_workout_not_found(client, seed):
    r = client.post("/workouts/999/exercises/1/workout_exercises", json={"sets": 3})
    if r.status_code != 404:
        raise Exception(f"Expected 404 but got {r.status_code}")