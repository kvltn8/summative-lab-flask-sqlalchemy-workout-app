from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from models import db, Exercise, Workout, WorkoutExercise


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        sqla_session = db.session


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        sqla_session = db.session

    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

    # Schema validations
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or len(value.strip()) == 0:
            raise ValidationError("Name cannot be empty.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if value not in ["cardio", "strength", "flexibility", "balance"]:
            raise ValidationError("Category must be cardio, strength, flexibility, or balance.")


class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        sqla_session = db.session

    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

    # Schema validations
    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Duration must be greater than 0.")


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()