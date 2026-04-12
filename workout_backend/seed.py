from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    burpees = Exercise(name="Burpees", category="cardio", equipment_needed=False)
    deadlift = Exercise(name="Deadlift", category="strength", equipment_needed=True)
    lunges = Exercise(name="Lunges", category="strength", equipment_needed=False)
    jump_rope = Exercise(name="Jump Rope", category="cardio", equipment_needed=True)
    pigeon_pose = Exercise(name="Pigeon Pose", category="flexibility", equipment_needed=False)
    db.session.add_all([burpees, deadlift, lunges, jump_rope, pigeon_pose])
    db.session.commit()

    leg_day = Workout(date=date(2026, 3, 5), duration_minutes=50, notes="Leg day focus")
    hiit = Workout(date=date(2026, 3, 7), duration_minutes=25, notes="HIIT session")
    recovery = Workout(date=date(2026, 3, 9), duration_minutes=40, notes="Active recovery")
    db.session.add_all([leg_day, hiit, recovery])
    db.session.commit()

    db.session.add_all([
        WorkoutExercise(workout_id=leg_day.id, exercise_id=lunges.id, sets=4, reps=12),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=deadlift.id, sets=3, reps=8),
        WorkoutExercise(workout_id=hiit.id, exercise_id=burpees.id, sets=5, reps=20),
        WorkoutExercise(workout_id=hiit.id, exercise_id=jump_rope.id, duration_seconds=600),
        WorkoutExercise(workout_id=recovery.id, exercise_id=pigeon_pose.id, duration_seconds=120),
    ])
    db.session.commit()
    print("Seeded!")