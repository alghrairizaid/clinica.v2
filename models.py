# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Main users table - contains login information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True, comment='User email')
    password = db.Column(db.String(256), nullable=False, comment='Hashed password')
    role = db.Column(db.String(20), nullable=False, comment='User type: admin, doctor, patient')
    is_active = db.Column(db.Boolean, default=True, comment='Account status')
    last_login = db.Column(db.DateTime, comment='Last login timestamp')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Account creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Doctor(db.Model):
    """Doctors table - contains doctor information"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Doctor ID')
    first_name = db.Column(db.String(50), nullable=False, comment='First name')
    last_name = db.Column(db.String(50), nullable=False, comment='Last name')
    email = db.Column(db.String(120), unique=True, nullable=False, index=True, comment='Email address')
    phone_number = db.Column(db.String(20), nullable=False, comment='Phone number')
    password = db.Column(db.String(256), nullable=False, comment='Hashed password')
    specialization = db.Column(db.String(100), nullable=False, comment='Medical specialization')
    consultation_fee = db.Column(db.Float, nullable=False, comment='Consultation fee')
    is_available = db.Column(db.Boolean, default=True, comment='Doctor availability status')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Registration date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')
    schedules = db.relationship('Schedule', backref='doctor', lazy='dynamic')
    prescriptions = db.relationship('Prescription', backref='doctor', lazy='dynamic')
    laboratories = db.relationship('Laboratory', backref='doctor', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Patient(db.Model):
    """Patients table - contains patient information"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, comment='First name')
    last_name = db.Column(db.String(50), nullable=False, comment='Last name')
    email = db.Column(db.String(120), unique=True, nullable=False, index=True, comment='Email address')
    phone_number = db.Column(db.String(20), nullable=False, comment='Phone number')
    password = db.Column(db.String(256), nullable=False, comment='Hashed password')
    gender = db.Column(db.String(10), nullable=False, comment='Gender')
    blood_type = db.Column(db.String(5), comment='Blood type')
    service_type = db.Column(db.String(50), nullable=True, comment='Service Type')
    insurance_policy_number = db.Column(db.String(50), comment='Insurance Policy Number')
    emergency_contact = db.Column(db.String(100), comment='Emergency contact information')
    address = db.Column(db.String(200), comment='Patient address')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Registration date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    medical_card = db.relationship('MedicalCard', uselist=False, backref='patient', lazy='joined')
    prescriptions = db.relationship('Prescription', backref='patient', lazy='dynamic')
    lab_results = db.relationship('LabResult', backref='patient', lazy='dynamic')
    laboratories = db.relationship('Laboratory', backref='patient', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Appointment(db.Model):
    """Appointments table - contains appointment information"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, comment='Patient ID')
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=True, comment='Doctor ID')
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True, comment='Service ID')
    date = db.Column(db.Date, nullable=False, comment='Appointment date')
    time = db.Column(db.Time, nullable=False, comment='Appointment time')
    duration = db.Column(db.Integer, default=30, comment='Duration in minutes')
    fee = db.Column(db.Float, nullable=False, comment='Appointment fee')
    status = db.Column(db.String(20), default='pending', comment='Status: pending, confirmed, cancelled, completed')
    notes = db.Column(db.Text, comment='Appointment notes')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    # New relationship
    service = db.relationship('Service', backref='appointments')

    __table_args__ = (
        db.Index('idx_appointment_datetime', 'date', 'time'),
    )


class MedicalCard(db.Model):
    """Medical records for patients"""
    __tablename__ = 'medical_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    allergies = db.Column(db.Text, comment='Patient allergies')
    chronic_conditions = db.Column(db.Text, comment='Chronic medical conditions')
    history = db.Column(db.Text, comment='Medical history')
    diagnoses = db.Column(db.Text, comment='Current diagnoses')
    lab_results = db.Column(db.Text, comment='Recent lab results')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    prescriptions = db.relationship('Prescription', backref='medical_card', lazy='dynamic')


class Prescription(db.Model):
    """Medical prescriptions"""
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    medical_card_id = db.Column(db.Integer, db.ForeignKey('medical_cards.id', ondelete='SET NULL'))
    prescription_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    medication = db.Column(db.Text, nullable=False, comment='Prescribed medications')
    dosage = db.Column(db.String(100), comment='Medication dosage')
    duration = db.Column(db.String(50), comment='Duration of medication')
    instructions = db.Column(db.Text, comment='Usage instructions')
    lab_referral = db.Column(db.String(200), comment='Laboratory referral')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')


class LabResult(db.Model):
    """Laboratory test results"""
    __tablename__ = 'lab_results'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    test_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    result = db.Column(db.Text, nullable=False)
    reference_range = db.Column(db.String(100), comment='Normal reference range')
    interpretation = db.Column(db.Text, comment='Result interpretation')
    lab_name = db.Column(db.String(100), comment='Laboratory name')
    lab_contacts = db.Column(db.String(200), comment='Laboratory contact information')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')


class Schedule(db.Model):
    """Doctor's schedule"""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False, comment='Day of the week')
    start_time = db.Column(db.Time, nullable=False, comment='Start time')
    end_time = db.Column(db.Time, nullable=False, comment='End time')
    slot_duration = db.Column(db.Integer, default=30, comment='Duration of each slot in minutes')
    is_available = db.Column(db.Boolean, default=True, comment='Schedule availability')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')

    __table_args__ = (
        db.Index('idx_schedule_doctor_day', 'doctor_id', 'day_of_week'),
    )


class Laboratory(db.Model):
    """Laboratory information"""
    __tablename__ = 'laboratories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    test_types = db.Column(db.String(200), comment='Available test types')
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='SET NULL'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')


class Service(db.Model):
    """Medical services table"""
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, comment='Service name (English)')
    description = db.Column(db.String(255), comment='Service description (optional)')
    fee = db.Column(db.Float, nullable=True, comment='Service fee/price')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), comment='Creation date')
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), comment='Last update date')
