from app import app, db
from models import User, Doctor, Patient, Appointment, Service
from werkzeug.security import generate_password_hash
from datetime import datetime, time
import os

# تعيين مسار قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/zasaa/Desktop/clinc/instance/clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def create_sample_data():
    """Create sample data for testing"""
    try:
        with app.app_context():
            # Create sample doctors
            doctors_data = [
                {
                    'first_name': 'Ahmad', 'last_name': 'Al-Sayed',
                    'email': 'ahmad.sayed@clinic.com', 'phone_number': '0501234567',
                    'password': 'doctor123', 'consultation_fee': 300.0,
                    'specialization': 'General Medicine'
                },
                {
                    'first_name': 'Mohammed', 'last_name': 'Al-Rashid',
                    'email': 'mohammed.rashid@clinic.com', 'phone_number': '0502345678',
                    'password': 'doctor123', 'consultation_fee': 350.0,
                    'specialization': 'Cardiology'
                },
                {
                    'first_name': 'Fatima', 'last_name': 'Al-Qasim',
                    'email': 'fatima.qasim@clinic.com', 'phone_number': '0503456789',
                    'password': 'doctor123', 'consultation_fee': 280.0,
                    'specialization': 'Pediatrics'
                },
                {
                    'first_name': 'Omar', 'last_name': 'Al-Nasser',
                    'email': 'omar.nasser@clinic.com', 'phone_number': '0504567890',
                    'password': 'doctor123', 'consultation_fee': 320.0,
                    'specialization': 'Orthopedics'
                },
                {
                    'first_name': 'Layla', 'last_name': 'Al-Hamad',
                    'email': 'layla.hamad@clinic.com', 'phone_number': '0505678901',
                    'password': 'doctor123', 'consultation_fee': 290.0,
                    'specialization': 'Dermatology'
                },
                {
                    'first_name': 'Youssef', 'last_name': 'Al-Qahtani',
                    'email': 'youssef.qahtani@clinic.com', 'phone_number': '0506789012',
                    'password': 'doctor123', 'consultation_fee': 310.0,
                    'specialization': 'ENT'
                },
                {
                    'first_name': 'Sara', 'last_name': 'Al-Mutairi',
                    'email': 'sara.mutairi@clinic.com', 'phone_number': '0507890123',
                    'password': 'doctor123', 'consultation_fee': 330.0,
                    'specialization': 'Gynecology'
                },
                {
                    'first_name': 'Hassan', 'last_name': 'Al-Dossary',
                    'email': 'hassan.dossary@clinic.com', 'phone_number': '0508901234',
                    'password': 'doctor123', 'consultation_fee': 340.0,
                    'specialization': 'Neurology'
                },
                {
                    'first_name': 'Noura', 'last_name': 'Al-Shamari',
                    'email': 'noura.shamari@clinic.com', 'phone_number': '0509012345',
                    'password': 'doctor123', 'consultation_fee': 295.0,
                    'specialization': 'Ophthalmology'
                },
                {
                    'first_name': 'Malik', 'last_name': 'Al-Otaibi',
                    'email': 'malik.otaibi@clinic.com', 'phone_number': '0500123456',
                    'password': 'doctor123', 'consultation_fee': 315.0,
                    'specialization': 'Urology'
                }
            ]

            # Create sample patients
            patients_data = [
                {
                    'first_name': 'Khalid', 'last_name': 'Al-Sultan',
                    'email': 'khalid.sultan@example.com', 'phone_number': '0561234567',
                    'password': 'patient123', 'gender': 'male'
                },
                {
                    'first_name': 'Noor', 'last_name': 'Al-Fahad',
                    'email': 'noor.fahad@example.com', 'phone_number': '0562345678',
                    'password': 'patient123', 'gender': 'female'
                },
                {
                    'first_name': 'Abdullah', 'last_name': 'Al-Salem',
                    'email': 'abdullah.salem@example.com', 'phone_number': '0563456789',
                    'password': 'patient123', 'gender': 'male'
                },
                {
                    'first_name': 'Hessa', 'last_name': 'Al-Majid',
                    'email': 'hessa.majid@example.com', 'phone_number': '0564567890',
                    'password': 'patient123', 'gender': 'female'
                },
                {
                    'first_name': 'Saad', 'last_name': 'Al-Ibrahim',
                    'email': 'saad.ibrahim@example.com', 'phone_number': '0565678901',
                    'password': 'patient123', 'gender': 'male'
                },
                {
                    'first_name': 'Reem', 'last_name': 'Al-Harbi',
                    'email': 'reem.harbi@example.com', 'phone_number': '0566789012',
                    'password': 'patient123', 'gender': 'female'
                },
                {
                    'first_name': 'Turki', 'last_name': 'Al-Ghamdi',
                    'email': 'turki.ghamdi@example.com', 'phone_number': '0567890123',
                    'password': 'patient123', 'gender': 'male'
                },
                {
                    'first_name': 'Maha', 'last_name': 'Al-Subaie',
                    'email': 'maha.subaie@example.com', 'phone_number': '0568901234',
                    'password': 'patient123', 'gender': 'female'
                },
                {
                    'first_name': 'Faisal', 'last_name': 'Al-Shammari',
                    'email': 'faisal.shammari@example.com', 'phone_number': '0569012345',
                    'password': 'patient123', 'gender': 'male'
                },
                {
                    'first_name': 'Amal', 'last_name': 'Al-Zahrani',
                    'email': 'amal.zahrani@example.com', 'phone_number': '0560123456',
                    'password': 'patient123', 'gender': 'female'
                }
            ]

            # Create sample services
            services_data = [
                {'name': 'General Checkup', 'description': 'Routine health checkup', 'fee': 100.0},
                {'name': 'Blood Test', 'description': 'Complete blood count', 'fee': 50.0},
                {'name': 'X-Ray', 'description': 'Chest X-ray', 'fee': 120.0},
                {'name': 'Ultrasound', 'description': 'Abdominal ultrasound', 'fee': 200.0},
                {'name': 'ECG', 'description': 'Electrocardiogram', 'fee': 80.0},
                {'name': 'Vaccination', 'description': 'Flu vaccine', 'fee': 60.0},
                {'name': 'Dental Cleaning', 'description': 'Teeth cleaning', 'fee': 150.0},
                {'name': 'Eye Exam', 'description': 'Vision test', 'fee': 90.0},
                {'name': 'Hearing Test', 'description': 'Audiometry', 'fee': 70.0},
                {'name': 'Physical Therapy', 'description': 'Therapy session', 'fee': 110.0},
            ]

            # Create admin user if not exists
            admin = User.query.filter_by(email='admin@clinic.com').first()
            if not admin:
                admin = User(
                    email='admin@clinic.com',
                    password=generate_password_hash('adminpassword'),
                    role='admin'
                )
                db.session.add(admin)

            # Create doctors and their user accounts
            for doctor_data in doctors_data:
                if not Doctor.query.filter_by(email=doctor_data['email']).first():
                    doctor = Doctor(
                        first_name=doctor_data['first_name'],
                        last_name=doctor_data['last_name'],
                        email=doctor_data['email'],
                        phone_number=doctor_data['phone_number'],
                        password=generate_password_hash(doctor_data['password']),
                        consultation_fee=doctor_data['consultation_fee'],
                        specialization=doctor_data['specialization']
                    )
                    db.session.add(doctor)

                    doctor_user = User(
                        email=doctor_data['email'],
                        password=generate_password_hash(doctor_data['password']),
                        role='doctor'
                    )
                    db.session.add(doctor_user)

            # Create patients and their user accounts
            for patient_data in patients_data:
                if not Patient.query.filter_by(email=patient_data['email']).first():
                    patient = Patient(
                        first_name=patient_data['first_name'],
                        last_name=patient_data['last_name'],
                        email=patient_data['email'],
                        phone_number=patient_data['phone_number'],
                        password=generate_password_hash(patient_data['password']),
                        gender=patient_data['gender']
                    )
                    db.session.add(patient)

                    patient_user = User(
                        email=patient_data['email'],
                        password=generate_password_hash(patient_data['password']),
                        role='patient'
                    )
                    db.session.add(patient_user)

            # Create services
            for service_data in services_data:
                if not Service.query.filter_by(name=service_data['name']).first():
                    service = Service(
                        name=service_data['name'],
                        description=service_data['description'],
                        fee=service_data['fee']
                    )
                    db.session.add(service)

            db.session.commit()
            print("Sample data created successfully!")
            return True

    except Exception as e:
        print(f"Error creating sample data: {str(e)}")
        return False


if __name__ == '__main__':
    create_sample_data()
