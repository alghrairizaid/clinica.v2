# forms.py
# Forms for the Clinic Management System

from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField, 
    SelectField, 
    DecimalField, 
    DateField, 
    TimeField, 
    HiddenField,
    SelectMultipleField,
    TextAreaField
)
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

def validate_phone(form, field):
    """Validate phone number to ensure it contains only digits"""
    if not field.data.isdigit():
        raise ValidationError('Phone number must contain only digits')
    if len(field.data) < 10 or len(field.data) > 15:
        raise ValidationError('Phone number must be between 10 and 15 digits')

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Form for patient registration"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Length(max=20),
            validate_phone
        ]
    )
    gender = SelectField(
        'Gender',
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    insurance_policy_number = StringField('Insurance Policy Number', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Register')

class DoctorForm(FlaskForm):
    """Form for adding new doctors"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Length(max=20),
            validate_phone
        ]
    )
    consultation_fee = DecimalField(
        'Consultation Fee',
        validators=[DataRequired()]
    )
    specialization = StringField(
        'Specialization',
        validators=[
            Length(max=100)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    submit = SubmitField('Add Doctor')

class EditDoctorForm(FlaskForm):
    """Form for editing doctor information"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Length(max=20),
            validate_phone
        ]
    )
    consultation_fee = DecimalField(
        'Consultation Fee',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password (Leave blank to keep current password)',
        validators=[
            Optional(),
            Length(min=6)
        ]
    )
    submit = SubmitField('Update Doctor')

class DeleteDoctorForm(FlaskForm):
    """Form for doctor deletion"""
    submit = SubmitField('Delete Doctor')

class AppointmentForm(FlaskForm):
    """نموذج حجز المواعيد"""
    patient_id = SelectField(
        'Patient',
        validators=[DataRequired()],
        coerce=int,
        default=None
    )
    doctor_id = SelectField(
        'Doctor',
        validators=[DataRequired()],
        coerce=int,
        default=None
    )
    date = DateField(
        'Date',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    time = TimeField(
        'Time',
        validators=[DataRequired()],
        format='%H:%M'
    )
    submit = SubmitField('Book Appointment')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.patient_id.choices = []
        self.doctor_id.choices = []

class PatientAppointmentForm(FlaskForm):
    """نموذج حجز المواعيد للمرضى"""
    doctor_id = SelectField('Doctor', coerce=int)
    service_id = SelectField('Service', coerce=int)
    date = DateField('Date', format='%Y-%m-%d')
    time = TimeField('Time', format='%H:%M')
    submit = SubmitField('Book Appointment')

class AddPatientForm(FlaskForm):
    """نموذج لإضافة مريض جديد"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Length(max=20),
            validate_phone
        ]
    )
    gender = SelectField(
        'Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    insurance_policy_number = StringField('Insurance Policy Number', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Patient')

class SearchForm(FlaskForm):
    search_query = StringField('Search word', validators=[DataRequired()])
    search_type = SelectField('Search type', choices=[
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ], validators=[DataRequired()])
    submit = SubmitField('Search')

class MedicalCardForm(FlaskForm):
    history = TextAreaField('History')
    diagnoses = TextAreaField('Diagnoses')
    lab_results = TextAreaField('Lab Results')
    submit = SubmitField('Save')

class PrescriptionForm(FlaskForm):
    recipe = StringField('Prescription', validators=[DataRequired()])
    lab_referral = StringField('Lab Referral')
    submit = SubmitField('Save Prescription')

class LabResultForm(FlaskForm):
    name = StringField('Test Name', validators=[DataRequired()])
    result = StringField('Result', validators=[DataRequired()])
    contacts = StringField('Contacts')
    submit = SubmitField('Save Lab Result')

class ScheduleForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    working_days = SelectMultipleField(
        'Working Days',
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday')
        ],
        validators=[DataRequired()]
    )
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Save Schedule')

class LaboratoryForm(FlaskForm):
    name = StringField('Lab Name', validators=[DataRequired()])
    test_types = StringField('Test Types', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Laboratory')

class EditPatientForm(FlaskForm):
    """Form for editing patient information"""
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Length(max=20),
            validate_phone
        ]
    )
    gender = SelectField(
        'Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[DataRequired()]
    )
    insurance_policy_number = StringField(
        'Insurance Policy Number',
        validators=[DataRequired(), Length(max=50)]
    )
    password = PasswordField(
        'Password (Leave blank to keep current password)',
        validators=[
            Optional(),
            Length(min=6)
        ]
    )
    submit = SubmitField('Update Patient')
