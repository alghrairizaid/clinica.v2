# app.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    UserMixin,
)
from models import db, User, Doctor, Patient, Appointment, MedicalCard, Prescription, LabResult, Schedule, Laboratory, Service
from forms import (
    LoginForm,
    RegistrationForm,
    DoctorForm,
    AppointmentForm,
    EditDoctorForm,
    DeleteDoctorForm,  
    AddPatientForm,
    PatientAppointmentForm,
    SearchForm,  # إضافة SearchForm
    MedicalCardForm,
    PrescriptionForm,
    LabResultForm,
    ScheduleForm,
    LaboratoryForm,
    EditPatientForm
)
import os
from sqlalchemy import text
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/zasaa/Desktop/babsss6/clinc/instance/clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'maser'
def test_db_connection():
    try:
        # Check if database file exists
        db_path = 'C:/Users/zasaa/Desktop/clinc/instance/clinic.db'
        if not os.path.exists(db_path):
            print("Database file not found at:", db_path)
            print("Creating new database...")
        # Try to execute a simple query
        db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
        print(f"Database location: {db_path}")
        return True
    except Exception as e:
        print("Database connection failed!")
        print(f"Error: {str(e)}")
        print("Exiting application...")
        exit(1)

db.init_app(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
    test_db_connection()
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            email='admin@clinic.com',
            password=generate_password_hash('adminpassword'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin account created successfully!")
    else:
        print("Admin account already exists.")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # إعادة التوجيه إلى 'login' للمستخدمين غير المصرح لهم


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()  # التأكد من إنشاء جميع الجداول
    test_db_connection()
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            email='admin@clinic.com',
            password=generate_password_hash('adminpassword'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin account created successfully!")
    else:
        print("Admin account already exists.")

# Index Route
@app.route('/')
def home():
    return render_template('base.html')

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # البحث عن المستخدم بناءً على البريد الإلكتروني
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            
            # الحصول على اسم المستخدم بناءً على نوع المستخدم
            user_name = None
            if user.role == 'doctor':
                doctor = Doctor.query.filter_by(email=user.email).first()
                if doctor:
                    user_name = f"Dr. {doctor.first_name} {doctor.last_name}"
            elif user.role == 'patient':
                patient = Patient.query.filter_by(email=user.email).first()
                if patient:
                    user_name = f"{patient.first_name} {patient.last_name}"
            
            # تخزين اسم المستخدم في الجلسة
            if user_name:
                session['user_name'] = user_name
            
            flash('You have successfully logged in!', 'success')
            # إعادة التوجيه بناءً على الدور
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

# Delete Patient Route
@app.route('/admin/delete_patient/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient_record(patient_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('patients_list'))

    patient = Patient.query.get_or_404(patient_id)
    user = User.query.filter_by(email=patient.email, role='patient').first()

    try:
        if user:
            db.session.delete(user)
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the patient.', 'danger')
        print(e)

    return redirect(url_for('patients_list'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already in use. Please use a different email.', 'warning')
            return redirect(url_for('register'))
        
        # Create hashed password once
        hashed_password = generate_password_hash(form.password.data)
        
        # Create new patient with hashed password
        new_patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            gender=form.gender.data,
            password=hashed_password,
            insurance_policy_number=form.insurance_policy_number.data,
        )
        db.session.add(new_patient)
        db.session.flush()
        print("Patient added, id:", new_patient.id)
        new_card = MedicalCard(patient_id=new_patient.id)
        db.session.add(new_card)
        print("Medical card added")
        # Create user account with same hashed password
        new_user = User(
            email=form.email.data,
            password=hashed_password,
            role='patient'
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            print("All committed")
            login_user(new_user)
            flash('Registered successfully!', 'success')
            return redirect(url_for('patient_dashboard'))
        except Exception as e:
            db.session.rollback()
            print("Exception occurred:", e)
            flash('An error occurred during registration.', 'danger')
            print(f"Error: {str(e)}")
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    doctors_count = Doctor.query.count()
    patients_count = Patient.query.count()
    appointments_count = Appointment.query.count()
    laboratories_count = Laboratory.query.count()
    services_count = Service.query.count()
    recent_appointments = Appointment.query.options(
        db.joinedload(Appointment.patient),
        db.joinedload(Appointment.doctor)
    ).order_by(Appointment.date.desc()).limit(5).all()
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    recent_laboratories = Laboratory.query.order_by(Laboratory.id.desc()).limit(3).all()
    return render_template(
        'admin/admin_dashboard.html',
        doctors_count=doctors_count,
        patients_count=patients_count,
        appointments_count=appointments_count,
        laboratories_count=laboratories_count,
        services_count=services_count,
        recent_appointments=recent_appointments,
        recent_patients=recent_patients,
        recent_laboratories=recent_laboratories,
        current_year=datetime.now().year
    )

@app.route('/admin/doctors')
@login_required
def doctors_list():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    doctors = Doctor.query.all()
    form = DeleteDoctorForm()  # إنشاء نموذج الحذف
    return render_template('admin/doctors_list.html', doctors=doctors, form=form, current_year=datetime.now().year)

@app.route('/admin/patients')
@login_required
def patients_list():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('admin/patients_list.html', patients=patients, current_year=datetime.now().year)

@app.route('/admin/appointments')
@login_required
def appointments():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    appointments = Appointment.query.all()
    # جلب معلومات المريض لكل موعد
    for appointment in appointments:
        appointment.patient = db.session.get(Patient, appointment.patient_id)
        appointment.doctor = db.session.get(Doctor, appointment.doctor_id)

    return render_template('admin/appointments.html', appointments=appointments, current_year=datetime.now().year)

@app.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
        
    form = DoctorForm()
    if form.validate_on_submit():
        try:
            # التحقق من وجود البريد الإلكتروني
            if Doctor.query.filter_by(email=form.email.data).first():
                flash('Email already exists!', 'danger')
                return render_template('admin/add_doctor.html', form=form)
                
            # إنشاء حساب الطبيب
            doctor = Doctor(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                specialization=form.specialization.data,
                password=generate_password_hash(form.password.data),
                consultation_fee=form.consultation_fee.data
            )
            
            # إنشاء حساب المستخدم للطبيب
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                role='doctor'
            )
            
            # حفظ في قاعدة البيانات
            db.session.add(doctor)
            db.session.add(user)
            db.session.commit()
            
            flash('Doctor added successfully!', 'success')
            return redirect(url_for('doctors_list'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error adding doctor. Please try again.', 'danger')
            print(f"Error: {str(e)}")
            
    return render_template('admin/add_doctor.html', form=form)

@app.route('/admin/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    form = AddPatientForm()
    if form.validate_on_submit():
        try:
            # التحقق من وجود البريد الإلكتروني
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('A user with this email already exists.', 'danger')
                return render_template('admin/add_patient.html', form=form)

            # إنشاء حساب المستخدم
            hashed_password = generate_password_hash(form.password.data)
            user = User(email=form.email.data, password=hashed_password, role='patient')
            db.session.add(user)
            db.session.flush()  # للحصول على user.id

            # إنشاء سجل المريض
            patient = Patient(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                gender=form.gender.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
                password=hashed_password,
                insurance_policy_number=form.insurance_policy_number.data
            )
            db.session.add(patient)
            db.session.flush()  # للحصول على new_patient.id
            new_card = MedicalCard(patient_id=patient.id)
            db.session.add(new_card)
            db.session.commit()
            flash('Patient added successfully!', 'success')
            return redirect(url_for('patients_list'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the patient.', 'danger')
            print(f"Error adding patient: {str(e)}")
            
    return render_template('admin/add_patient.html', form=form)

# Delete Appointment Route
@app.route('/admin/delete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('appointments'))

    appointment = db.session.get(Appointment, appointment_id)
    if appointment is None:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('appointments'))
    
    try:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting appointment: {str(e)}')
        flash('An error occurred while deleting the appointment.', 'danger')
    
    return redirect(url_for('appointments'))

@app.route('/admin/book_appointment', methods=['GET', 'POST'])
@login_required
def admin_book_appointment():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    form = AppointmentForm()
    
    # تحميل قائمة المرضى والأطباء
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in patients] if patients else []
    form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name}") for d in doctors] if doctors else []
    
    if form.validate_on_submit():
        try:
            doctor = db.session.get(Doctor, form.doctor_id.data)
            patient = db.session.get(Patient, form.patient_id.data)
            
            if doctor and patient:
                # Check doctor's schedule
                schedule = Schedule.query.filter_by(doctor_id=doctor.id).first()
                if schedule:
                    # Basic check for working days (assuming working_days is a comma-separated string like 'Monday,Tuesday')
                    # And check if the selected time falls within time slots (assuming time_slots is a string like '09:00-17:00')
                    selected_day = form.date.data.strftime('%A') # Get day name (e.g., 'Monday')
                    selected_time = form.time.data.strftime('%H:%M') # Get time in HH:MM format

                    is_working_day = selected_day in schedule.working_days # Simplified check
                    is_within_time_slots = False # Simplified check

                    if schedule.time_slots and '-' in schedule.time_slots:
                        start_time_str, end_time_str = schedule.time_slots.split('-')
                        try:
                            start_time = datetime.strptime(start_time_str, '%H:%M').time()
                            end_time = datetime.strptime(end_time_str, '%H:%M').time()
                            
                            # Create datetime objects for comparison
                            start_dt = datetime.combine(form.date.data, start_time)
                            end_dt = datetime.combine(form.date.data, end_time)
                            selected_dt = datetime.combine(form.date.data, form.time.data)

                            # If end time is before start time, it spans midnight
                            if end_dt < start_dt:
                                end_dt += timedelta(days=1)

                            # Check if the selected time is within the time range
                            is_within_time_slots = start_dt <= selected_dt < end_dt
                            
                        except ValueError:
                            flash('Invalid time slot format in doctor\'s schedule.', 'warning')
                            is_within_time_slots = False # Assume not available if format is bad

                    if not schedule or not is_working_day or not is_within_time_slots:
                         flash('Sorry, the doctor is not available at the selected date and time.', 'danger')
                         return render_template('admin/book_appointment.html', form=form)

                # التحقق من عدم وجود موعد في نفس الوقت
                existing_appointment = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    date=form.date.data,
                    time=form.time.data
                ).first()
                
                if existing_appointment:
                    flash('This time slot is already booked. Please choose another time.', 'danger')
                    return render_template('admin/book_appointment.html', form=form)
                
                fee = doctor.consultation_fee if doctor else 0
                new_appointment = Appointment(
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    date=form.date.data,
                    time=form.time.data,
                    fee=fee,
                    status='pending'
                )
                db.session.add(new_appointment)
                db.session.commit()
                flash('Appointment booked successfully!', 'success')
                return redirect(url_for('appointments'))
            else:
                flash('Selected doctor or patient not found.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while booking the appointment.', 'danger')
            print(f"Error booking appointment: {str(e)}")
    
    return render_template(
        'admin/book_appointment.html',
        form=form,
        current_year=datetime.now().year
    )

# تحديث حالة الموعد
@app.route('/admin/update_appointment_status/<int:appointment_id>', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('appointments'))

    appointment = db.session.get(Appointment, appointment_id)
    if appointment is None:
        flash('Date not found.', 'danger')
        return redirect(url_for('appointments'))
    
    new_status = request.form.get('status')
    if new_status not in ['pending', 'confirmed', 'cancelled', 'completed']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('appointments'))

    try:
        appointment.status = new_status
        db.session.commit()
        flash('Appointment status updated successfully.!', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'خطأ في تحديث حالة الموعد: {str(e)}')
        flash('حدث خطأ أثناء تحديث حالة الموعد.', 'danger')
    
    return redirect(url_for('appointments'))

# Doctor Routes
@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    
    # جلب معلومات الطبيب والمواعيد
    doctor = Doctor.query.filter_by(email=current_user.email).first()
    if doctor:
        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        # إضافة معلومات المريض والخدمة لكل موعد
        for appointment in appointments:
            appointment.patient = Patient.query.get(appointment.patient_id)
            appointment.service = Service.query.get(appointment.service_id)
    else:
        appointments = []
        flash('Doctor profile not found.', 'danger')
    
    return render_template(
        'doctor/doctor_dashboard.html',
        appointments=appointments,
        doctor=doctor,
        current_year=datetime.now().year
    )

@app.route('/doctor/view_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def doctor_view_appointment(appointment_id):
    if current_user.role != 'doctor':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    appointment = Appointment.query.get_or_404(appointment_id)
    patient = db.session.get(Patient, appointment.patient_id)
    doctor = Doctor.query.filter_by(email=current_user.email).first()

    if not doctor or appointment.doctor_id != doctor.id:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('doctor_dashboard'))

    # Get or create medical card for the patient
    medical_card = MedicalCard.query.filter_by(patient_id=patient.id).first()
    if not medical_card:
        medical_card = MedicalCard(patient_id=patient.id)
        db.session.add(medical_card)
        db.session.commit()

    prescription_form = PrescriptionForm()
    lab_result_form = LabResultForm()

    if request.method == 'POST':
        if 'add_prescription' in request.form and prescription_form.validate_on_submit():
            new_prescription = Prescription(
                patient_id=patient.id,
                doctor_id=doctor.id,
                medical_card_id=medical_card.id,
                medication=prescription_form.recipe.data,
                lab_referral=prescription_form.lab_referral.data
            )
            db.session.add(new_prescription)
            db.session.commit()
            
            # Send notification to patient
            flash(f'Prescription has been sent to {patient.first_name} {patient.last_name}!', 'success')
            return redirect(url_for('doctor_view_appointment', appointment_id=appointment.id))

        if 'add_lab_result' in request.form and lab_result_form.validate_on_submit():
            new_lab_result = LabResult(
                patient_id=patient.id,
                test_name=lab_result_form.name.data,
                result=lab_result_form.result.data,
                test_date=datetime.now().date()
            )
            db.session.add(new_lab_result)
            db.session.commit()
            flash('Lab result added successfully!', 'success')
            return redirect(url_for('doctor_view_appointment', appointment_id=appointment.id))

    return render_template(
        'doctor/view_appointment.html',
        appointment=appointment,
        patient=patient,
        doctor=doctor,
        medical_card=medical_card,
        prescription_form=prescription_form,
        lab_result_form=lab_result_form,
        current_year=datetime.now().year
    )

@app.route('/doctor/prescriptions')
@login_required
def doctor_prescriptions():
    if current_user.role != 'doctor':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    doctor = Doctor.query.filter_by(email=current_user.email).first()
    prescriptions = Prescription.query.filter_by(doctor_id=doctor.id).order_by(Prescription.created_at.desc()).all()
    # ربط كل وصفة بالمريض
    for prescription in prescriptions:
        prescription.patient = Patient.query.get(prescription.patient_id)
    return render_template('doctor/doctor_prescriptions.html', prescriptions=prescriptions, doctor=doctor)

# Patient Routes
@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    patient = Patient.query.filter_by(email=current_user.email).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    # جلب معلومات الطبيب والخدمة لكل موعد
    for appointment in appointments:
        appointment.doctor = Doctor.query.get(appointment.doctor_id)
        appointment.service = Service.query.get(appointment.service_id)
    # جلب المختبرات الخاصة بالمريض
    laboratories = Laboratory.query.filter_by(patient_id=patient.id).all()
    # ربط كل مختبر بالطبيب الخاص به
    for lab in laboratories:
        lab.doctor = Doctor.query.get(lab.doctor_id)
    # جلب نتائج التحاليل الخاصة بالمريض
    lab_results = LabResult.query.filter_by(patient_id=patient.id).all()
    return render_template(
        'patient/patient_dashboard.html',
        appointments=appointments,
        current_year=datetime.now().year,
        patient=patient,
        laboratories=laboratories,
        lab_results=lab_results
    )

@app.route('/patient/appointments')
@login_required
def patient_appointments():
    if current_user.role != 'patient':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    patient = Patient.query.filter_by(email=current_user.email).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    return render_template(
        'patient/appointments.html',
        appointments=appointments,
        current_year=datetime.now().year
    )

@app.route('/patient/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if not current_user.is_authenticated or current_user.role != 'patient':
        return redirect(url_for('login'))
    from forms import PatientAppointmentForm
    from models import Appointment, Service, Doctor
    patient = Patient.query.filter_by(email=current_user.email).first()
    services = Service.query.all()
    doctors = Doctor.query.all()
    service_type = request.args.get('service_type') or request.form.get('service_type')
    service_id = request.args.get('service_id') or request.form.get('service_id')
    form = PatientAppointmentForm()
    show_services = False
    show_doctors = False
    step = 'service_type'  # الخطوة الأولى: اختيار نوع الخدمة
    error_message = None
    # الخطوة الأولى: اختيار نوع الخدمة فقط
    if not service_type:
        if request.method == 'POST':
            selected_type = request.form.get('service_type')
            if selected_type in ['Medical Services', 'Consultations']:
                # أعد التوجيه مع النوع المختار
                return redirect(url_for('book_appointment', service_type=selected_type))
            else:
                error_message = 'Please select a service type.'
        return render_template('patient/book_appointment.html', step=step, form=form, service_type=None, services=services, doctors=doctors, show_services=False, show_doctors=False, error_message=error_message)
    # الخطوة الثانية: عرض الحقول حسب النوع
    if service_type == 'Medical Services':
        show_services = True
        show_doctors = False
        form.service_id.choices = [(s.id, s.name) for s in services]
    elif service_type == 'Consultations':
        show_services = False
        show_doctors = True
        form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name}") for d in doctors]
    step = 'details'
    if request.method == 'POST' and service_type:
        if service_type == 'Medical Services':
            if form.service_id.data and form.date.data and form.time.data:
                # تحقق من وجود موعد لنفس الخدمة في نفس التاريخ والوقت
                existing_appointment = Appointment.query.filter_by(
                    service_id=form.service_id.data,
                    date=form.date.data,
                    time=form.time.data
                ).first()
                if existing_appointment:
                    error_message = 'This service is already booked at the selected date and time. Please choose another slot.'
                else:
                    service = Service.query.get(form.service_id.data)
                    fee = service.fee if service and service.fee else 0
                    new_appointment = Appointment(
                        patient_id=patient.id,
                        service_id=form.service_id.data,
                        date=form.date.data,
                        time=form.time.data,
                        fee=fee,
                        status='pending'
                    )
                    db.session.add(new_appointment)
                    db.session.commit()
                    flash('Medical service booked successfully!', 'success')
                    return redirect(url_for('patient_dashboard'))
            else:
                error_message = 'Please select a service, date, and time.'
        elif service_type == 'Consultations':
            if form.doctor_id.data and form.date.data and form.time.data:
                # تحقق من وجود موعد لنفس الطبيب في نفس التاريخ والوقت
                existing_appointment = Appointment.query.filter_by(
                    doctor_id=form.doctor_id.data,
                    date=form.date.data,
                    time=form.time.data
                ).first()
                if existing_appointment:
                    error_message = 'This doctor is already booked at the selected date and time. Please choose another slot.'
                else:
                    doctor = Doctor.query.get(form.doctor_id.data)
                    fee = doctor.consultation_fee if doctor else 0
                    new_appointment = Appointment(
                        patient_id=patient.id,
                        doctor_id=form.doctor_id.data,
                        date=form.date.data,
                        time=form.time.data,
                        fee=fee,
                        status='pending'
                    )
                    db.session.add(new_appointment)
                    db.session.commit()
                    flash('Consultation appointment booked successfully!', 'success')
                    return redirect(url_for('patient_dashboard'))
            else:
                error_message = 'Please select a doctor, date, and time.'
    return render_template('patient/book_appointment.html', step=step, form=form, service_type=service_type, service_id=service_id, services=services, doctors=doctors, show_services=show_services, show_doctors=show_doctors, error_message=error_message)

@app.route('/patient/prescriptions')
@login_required
def patient_prescriptions():
    if current_user.role != 'patient':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    
    patient = Patient.query.filter_by(email=current_user.email).first()
    if not patient:
        flash('Patient record not found.', 'danger')
        return redirect(url_for('login'))
    
    prescriptions = Prescription.query.filter_by(patient_id=patient.id).order_by(Prescription.created_at.desc()).all()
    # Get doctor information for each prescription
    for prescription in prescriptions:
        prescription.doctor = Doctor.query.get(prescription.doctor_id)
    
    return render_template('patient/prescriptions.html', prescriptions=prescriptions)

# API Routes for JavaScript
@app.route('/get_doctor_fee/<int:doctor_id>')
@login_required
def get_doctor_fee(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({'fee': doctor.consultation_fee})

# Delete Doctor Route
@app.route('/admin/delete_doctor/<int:doctor_id>', methods=['POST'])
@login_required
def delete_doctor(doctor_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('doctors_list'))

    doctor = Doctor.query.get_or_404(doctor_id)
    user = User.query.filter_by(email=doctor.email, role='doctor').first()

    try:
        # حذف جميع المواعيد المرتبطة بالطبيب أولاً
        Appointment.query.filter_by(doctor_id=doctor_id).delete()
        
        # حذف حساب المستخدم المرتبط بالطبيب إذا وجد
        if user:
            db.session.delete(user)
            
        # حذف الطبيب
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the doctor.', 'danger')
        print(f"Error deleting doctor: {str(e)}")

    return redirect(url_for('doctors_list'))

@app.route('/admin/clear_database', methods=['POST'])
@login_required
def clear_database():
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('admin_dashboard'))

    try:
        # مسح البيانات من الجداول
        db.session.execute("DELETE FROM patient")
        db.session.execute("DELETE FROM appointment")
        db.session.execute("DELETE FROM doctor")
        db.session.commit()
        flash('All data cleared successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while clearing the data.', 'danger')
        print("Error:", e)  # طباعة تفاصيل الخطأ هنا

    return redirect(url_for('admin_dashboard'))

# Edit Doctor Route
@app.route('/admin/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    form = EditDoctorForm(obj=doctor)  # Fill form with current doctor data
    
    if form.validate_on_submit():
        # Update doctor details
        doctor.first_name = form.first_name.data
        doctor.last_name = form.last_name.data
        doctor.email = form.email.data
        doctor.phone_number = form.phone_number.data
        doctor.consultation_fee = form.consultation_fee.data
        doctor.password = form.password.data  # Store the password as plain text

        # Find or create corresponding user account for the doctor
        user = User.query.filter_by(email=doctor.email, role='doctor').first()
        if user:
            # Update user details
            user.email = form.email.data
            user.password = form.password.data  # Store the password as plain text
        else:
            # Create a new User account if it doesn't exist
            new_user = User(
                email=form.email.data,
                password=form.password.data,  # Store the password as plain text
                role='doctor'
            )
            db.session.add(new_user)
            flash('Associated user account created for the doctor.', 'info')
        
        try:
            db.session.commit()
            flash('Doctor information updated successfully!', 'success')
            return redirect(url_for('doctors_list'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the doctor.', 'danger')
            print(e)  # For debugging
    
    return render_template('admin/edit_doctor.html', form=form, doctor=doctor, current_year=datetime.now().year)

@app.route('/admin/manage_schedule/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def admin_manage_schedule(doctor_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    doctor = Doctor.query.get_or_404(doctor_id)
    schedule = Schedule.query.filter_by(doctor_id=doctor.id).first()
    # تجهيز القيم الافتراضية للحقول الجديدة
    form = ScheduleForm(obj=schedule)
    form.doctor_id.choices = [(doctor.id, f"Dr. {doctor.first_name} {doctor.last_name}")]
    if schedule:
        # تعبئة الحقول الجديدة من القيم النصية القديمة
        if schedule.working_days:
            form.working_days.data = schedule.working_days.split(',')
        if schedule.time_slots and '-' in schedule.time_slots:
            start, end = schedule.time_slots.split('-')
            try:
                form.start_time.data = datetime.strptime(start.strip(), '%H:%M').time()
                form.end_time.data = datetime.strptime(end.strip(), '%H:%M').time()
            except Exception:
                pass

    if request.method == 'POST':
        working_days_list = request.form.getlist('working_days')
        if working_days_list and form.start_time.data and form.end_time.data:
            working_days_str = ','.join(working_days_list)
            time_slots_str = f"{form.start_time.data.strftime('%H:%M')}-{form.end_time.data.strftime('%H:%M')}"
            if schedule:
                schedule.working_days = working_days_str
                schedule.time_slots = time_slots_str
            else:
                new_schedule = Schedule(
                    doctor_id=doctor.id,
                    working_days=working_days_str,
                    time_slots=time_slots_str
                )
                db.session.add(new_schedule)
            try:
                db.session.commit()
                flash('Doctor schedule updated successfully!', 'success')
                return redirect(url_for('doctors_list'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating the doctor\'s schedule.', 'danger')
                print(f"Error updating schedule: {str(e)}")
        else:
            flash('Please select at least one working day and specify start/end time.', 'danger')

    return render_template('admin/manage_schedule.html', form=form, doctor=doctor, current_year=datetime.now().year)

@app.route('/admin/search', methods=['GET', 'POST'])
@login_required
def admin_search():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    form = SearchForm()
    results = []
    search_performed = False
    search_type = None
    
    if form.validate_on_submit():
        search_performed = True
        search_type = form.search_type.data
        search_query = f"%{form.search_query.data}%"
        
        if search_type == 'doctor':
            results = Doctor.query.filter(
                db.or_(
                    Doctor.first_name.ilike(search_query),
                    Doctor.last_name.ilike(search_query),
                    Doctor.email.ilike(search_query),
                    Doctor.phone_number.ilike(search_query),
                )
            ).all()
        else:
            results = Patient.query.filter(
                db.or_(
                    Patient.first_name.ilike(search_query),
                    Patient.last_name.ilike(search_query),
                    Patient.email.ilike(search_query),
                    Patient.phone_number.ilike(search_query)
                )
            ).all()
    
    return render_template(
        'admin/search.html',
        form=form,
        results=results,
        search_performed=search_performed,
        search_type=search_type,
        current_year=datetime.now().year
    )


@app.route('/medical_card/<int:patient_id>')
def view_medical_card(patient_id):
    card = MedicalCard.query.filter_by(patient_id=patient_id).first()
    return render_template('shared/components/medical_card_view.html', card=card)

@app.route('/prescriptions/<int:patient_id>')
def view_prescriptions(patient_id):
    prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
    return render_template('shared/components/prescriptions_list.html', prescriptions=prescriptions)

@app.route('/lab_results/<int:patient_id>')
def view_lab_results(patient_id):
    results = LabResult.query.filter_by(patient_id=patient_id).all()
    return render_template('shared/components/lab_results_list.html', results=results)

@app.route('/schedules')
def view_schedules():
    schedules = Schedule.query.all()
    return render_template('shared/components/schedules_list.html', schedules=schedules)

@app.route('/laboratories')
@login_required
def view_laboratories():
    if current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        labs = Laboratory.query.filter_by(doctor_id=doctor.id).all()
    elif current_user.role == 'patient':
        patient = Patient.query.filter_by(email=current_user.email).first()
        labs = Laboratory.query.filter_by(patient_id=patient.id).all()
    else:
        labs = Laboratory.query.all()
    return render_template('shared/components/laboratories_list.html', labs=labs)

@app.route('/admin/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)
    form = EditPatientForm(obj=patient)  # لملء النموذج ببيانات المريض الحالية

    if form.validate_on_submit():
        # تحديث بيانات المريض
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.email = form.email.data
        patient.phone_number = form.phone_number.data
        patient.gender = form.gender.data
        patient.insurance_policy_number = form.insurance_policy_number.data

        # تحديث كلمة المرور إذا تم إدخال كلمة مرور جديدة
        if form.password.data:
            patient.password = generate_password_hash(form.password.data)
            # تحديث كلمة المرور في جدول المستخدمين أيضاً إذا كان موجوداً
            user = User.query.filter_by(email=patient.email, role='patient').first()
            if user:
                user.password = patient.password # استخدم نفس كلمة المرور المجزأة

        try:
            db.session.commit()
            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('patients_list'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the patient.', 'danger')
            print(f"Error updating patient: {str(e)}")

    return render_template('admin/edit_patient.html', form=form, patient=patient)

@app.route('/admin/add_laboratory', methods=['GET', 'POST'])
@login_required
def add_laboratory():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    form = LaboratoryForm()
    form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name}") for d in Doctor.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    if form.validate_on_submit():
        lab = Laboratory(
            name=form.name.data,
            test_types=form.test_types.data,
            date=form.date.data,
            time=form.time.data,
            doctor_id=form.doctor_id.data,
            patient_id=form.patient_id.data
        )
        db.session.add(lab)
        db.session.commit()
        flash('Laboratory added successfully!', 'success')
        return redirect(url_for('view_laboratories'))
    return render_template('admin/add_laboratory.html', form=form)

@app.route('/admin/edit_laboratory/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def edit_laboratory(lab_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    lab = Laboratory.query.get_or_404(lab_id)
    form = LaboratoryForm(obj=lab)
    form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name}") for d in Doctor.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]
    if form.validate_on_submit():
        lab.name = form.name.data
        lab.test_types = form.test_types.data
        lab.date = form.date.data
        lab.time = form.time.data
        lab.doctor_id = form.doctor_id.data
        lab.patient_id = form.patient_id.data
        db.session.commit()
        flash('Laboratory updated successfully!', 'success')
        return redirect(url_for('view_laboratories'))
    return render_template('admin/edit_laboratory.html', form=form, lab=lab)

@app.route('/admin/delete_laboratory/<int:lab_id>', methods=['POST'])
@login_required
def delete_laboratory(lab_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('view_laboratories'))
    lab = Laboratory.query.get_or_404(lab_id)
    db.session.delete(lab)
    db.session.commit()
    flash('Laboratory deleted successfully!', 'success')
    return redirect(url_for('view_laboratories'))

@app.route('/edit_medical_card/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_medical_card(patient_id):
    card = MedicalCard.query.filter_by(patient_id=patient_id).first()
    if not card:
        flash('Medical card not found for this patient.', 'danger')
        return redirect(url_for('view_medical_card', patient_id=patient_id))
    form = MedicalCardForm(obj=card)
    if form.validate_on_submit():
        card.history = form.history.data
        card.diagnoses = form.diagnoses.data
        card.lab_results = form.lab_results.data
        db.session.commit()
        flash('Medical card updated!', 'success')
        return redirect(url_for('view_medical_card', patient_id=patient_id))
    return render_template('shared/components/edit_medical_card.html', form=form, card=card)

@app.route('/patient/select_service', methods=['GET', 'POST'])
@login_required
def select_service():
    if current_user.role != 'patient':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    patient = Patient.query.filter_by(email=current_user.email).first()
    services = Service.query.all()
    doctors = Doctor.query.all()
    from forms import PatientAppointmentForm
    form = PatientAppointmentForm()
    form.doctor_id.choices = [(d.id, f"Dr. {d.first_name} {d.last_name}") for d in doctors]
    show_appointment_form = False
    appointment_success = False
    error_message = None
    if request.method == 'POST':
        selected_type = request.form.get('service_type')
        selected_service_id = request.form.get('service_id')
        booking_attempted = False
        # إذا اختار Consultations، تحقق من الحجز
        if selected_type == 'Consultations':
            show_appointment_form = True
            booking_attempted = True
            if 'doctor_id' in request.form and 'date' in request.form and 'time' in request.form:
                from datetime import datetime
                form.doctor_id.data = int(request.form.get('doctor_id'))
                date_str = request.form.get('date')
                time_str = request.form.get('time')
                try:
                    form.date.data = datetime.strptime(date_str, '%Y-%m-%d').date()
                except Exception as e:
                    error_message = 'Invalid date format.'
                    print('Date parsing error:', e)
                    flash(error_message, 'danger')
                    return render_template('patient/select_service.html', patient=patient, services=services, doctors=doctors, form=form, show_appointment_form=show_appointment_form, error_message=error_message)
                try:
                    form.time.data = datetime.strptime(time_str, '%H:%M').time()
                except Exception as e:
                    error_message = 'Invalid time format.'
                    print('Time parsing error:', e)
                    flash(error_message, 'danger')
                    return render_template('patient/select_service.html', patient=patient, services=services, doctors=doctors, form=form, show_appointment_form=show_appointment_form, error_message=error_message)
                if form.validate():
                    from models import Appointment
                    new_appointment = Appointment(
                        patient_id=patient.id,
                        doctor_id=form.doctor_id.data,
                        date=form.date.data,
                        time=form.time.data,
                        status='pending'
                    )
                    db.session.add(new_appointment)
                    db.session.commit()
                    appointment_success = True
                    flash('Appointment booked successfully!', 'success')
                    return redirect(url_for('patient_dashboard'))
                else:
                    error_message = 'Please select a doctor, date, and time.'
                    print('Form validation errors:', form.errors)
                    flash(error_message, 'danger')
            else:
                error_message = 'Please fill all required fields.'
                flash(error_message, 'danger')
        else:
            # Medical Services
            patient.service_type = selected_type
            if selected_type == 'Medical Services' and selected_service_id:
                session['selected_service_id'] = int(selected_service_id)
            else:
                session.pop('selected_service_id', None)
            db.session.commit()
            flash('Service type updated successfully!', 'success')
            return redirect(url_for('patient_dashboard'))
        # إذا حاول الحجز ولم يتم الحجز لأي سبب
        if booking_attempted and not appointment_success:
            flash('Booking failed. Please check your data and try again.', 'danger')
    return render_template('patient/select_service.html', patient=patient, services=services, doctors=doctors, form=form, show_appointment_form=show_appointment_form, error_message=error_message)

@app.route('/admin/services')
@login_required
def admin_services():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    services = Service.query.order_by(Service.name).all()
    return render_template('admin/services_list.html', services=services)

@app.route('/admin/add_service', methods=['GET', 'POST'])
@login_required
def add_service():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('Service name is required.', 'danger')
            return redirect(url_for('add_service'))
        if Service.query.filter_by(name=name).first():
            flash('Service already exists.', 'warning')
            return redirect(url_for('add_service'))
        db.session.add(Service(name=name, description=description))
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_services'))
    return render_template('admin/add_service.html')

@app.route('/admin/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('Service name is required.', 'danger')
            return redirect(url_for('edit_service', service_id=service_id))
        service.name = name
        service.description = description
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_services'))
    return render_template('admin/edit_service.html', service=service)

@app.route('/admin/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('admin_services'))
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_services'))

@app.route('/get_service_fee/<int:service_id>')
@login_required
def get_service_fee(service_id):
    service = Service.query.get_or_404(service_id)
    return jsonify({'fee': service.fee})

if __name__ == '__main__':
    app.run(port=5000, debug=True)