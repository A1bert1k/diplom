from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

# Таблица "Клиенты" (Clients)
class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Таблица "Тренировки" (Workouts)
class Workout(db.Model):
    __tablename__ = 'workouts'
    workout_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    client = db.relationship('Client', backref=db.backref('workouts', lazy=True))

# Таблица "Биометрические_данные" (Biometric_Data)
class BiometricData(db.Model):
    __tablename__ = 'biometric_data'
    biometric_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    measurement_time = db.Column(db.Time, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    other_indicators = db.Column(db.String(200))
    client = db.relationship('Client', backref=db.backref('biometric_data', lazy=True))

# Таблица "Упражнения" (Exercises)
class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(80), nullable=False)

# Таблица "Показатели_упражнений" (Exercise_Indicators)
class ExerciseIndicator(db.Model):
    __tablename__ = 'exercise_indicators'
    indicator_id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
    indicator_name = db.Column(db.String(80), nullable=False)
    measurement_unit = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    exercise = db.relationship('Exercise', backref=db.backref('indicators', lazy=True))

@app.route('/')
def index():
    return "Welcome to the Biometric Data Monitoring System"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=port)
