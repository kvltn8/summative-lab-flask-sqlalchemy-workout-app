# Workout Tracker API
A backend REST API for personal trainers to track workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow.

## How to run it

1. Make sure you have Python and pipenv installed
2. Open your terminal
3. Go to the project folder
4. Run these commands:

```bash
pipenv install    # Installs all required packages
pipenv shell      # Activates the virtual environment
cd workout_backend  # Moves into the app folder
flask db upgrade head  # Applies migrations to the database
python seed.py    # Adds sample workout data
python app.py     # Starts the server

5. Open your browser to http://localhost:5555

## How to use it

GET /workouts - See all workouts
GET /workouts/<id> - See one workout
POST /workouts - Create a new workout
DELETE /workouts/<id> - Remove a workout
GET /exercises - See all exercises
GET /exercises/<id> - See one exercise
POST /exercises - Create a new exercise
DELETE /exercises/<id> - Remove an exercise
POST /workouts/<id>/exercises/<id>/workout_exercises - Add an exercise to a workout


Example POST Requests
Create a workout:

```json
{
  "date": "2026-04-12",
  "duration_minutes": 45,
  "notes": "Morning cardio"
}

Create an exercise:

```json
{
  "name": "Push-ups",
  "category": "strength",
  "equipment_needed": false
}
Add exercise to workout:

```json
{
  "sets": 3,
  "reps": 12
}
## What's inside

The API has workouts (with date, duration, notes) and exercises (with name, category, equipment). Workouts and exercises are connected so you can track which exercises you did in each workout.

## Features

- Full CRUD operations for workouts and exercises
- Database persistence with SQLite
- Validation for categories and duration
- Many-to-many relationship between workouts and exercises

## Run tests

pipenv run pytest testing.py -v

## Requirements

- Python 3.8 or higher
- pipenv

