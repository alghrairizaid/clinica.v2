# Clinic Management System

A web-based Clinic Management System built with Flask, providing role-based access for administrators, doctors, and patients. The system manages appointments, medical records, prescriptions, laboratory results, schedules, and services.

---

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Project Structure](#project-structure)
- [UI Overview](#ui-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Sample Data](#sample-data)
- [Usage](#usage)
- [Customization](#customization)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

---

## Introduction
This project is a comprehensive clinic management system designed to streamline the workflow of clinics and medical centers. It supports multiple user roles (admin, doctor, patient) and provides a full suite of features for managing appointments, medical records, laboratory results, and more. The system is built with extensibility and ease of use in mind, leveraging the Flask web framework and SQLAlchemy ORM.

## Technologies Used
- **Python 3.8+**
- **Flask** (web framework)
- **Flask-SQLAlchemy** (ORM)
- **Flask-Login** (user session management)
- **Flask-WTF** (form handling)
- **Flask-Migrate** (database migrations)
- **Werkzeug** (security and utilities)
- **SQLite** (default database)
- **Jinja2** (templating)
- **HTML5/CSS3/JavaScript** (frontend)

## Features
- **User Authentication**: Secure login and registration for patients, doctors, and admin.
- **Role-Based Dashboards**:
  - **Admin**: Manage doctors, patients, appointments, schedules, laboratories, and services.
  - **Doctor**: View appointments, manage prescriptions, and access patient records.
  - **Patient**: Book appointments, view prescriptions, and access their medical card.
- **Medical Records**: Store and manage medical cards, prescriptions, and lab results.
- **Appointment Booking**: Patients and admins can book, update, and cancel appointments.
- **Laboratory Management**: Manage lab tests and results.
- **Service Management**: Define and manage clinic services and their fees.
- **Search**: Search for doctors and patients.
- **Responsive UI**: User-friendly interface for all roles.
- **Sample Data**: Populate the system with example doctors, patients, and services for testing.

## Project Structure

```
Folder PATH listing for volume Windows
Volume serial number is 0A0A-BFBC
C:.
|   app.py
|   forms.py
|   models.py
|   project_tree.txt
|   README.md
|   
+---instance
|       clinic.db
|       clinic.sqbpro
|       data.py
|       New Text Document.db
|       New Text Document.db.mwb
|       
+---static
|   +---css
|   |       style.css
|   |       styles.css
|   |       
|   +---images
|   |       README.md
|   |       
|   \---js
|           scripts.js
|           
\---templates
    |   base.html
    |   index.html
    |   laboratories_list.html
    |   medical_card_view.html
    |   
    +---admin
    |       add_doctor.html
    |       add_laboratory.html
    |       add_patient.html
    |       add_service.html
    |       admin_dashboard.html
    |       appointments.html
    |       book_appointment.html
    |       doctors_list.html
    |       edit_doctor.html
    |       edit_laboratory.html
    |       edit_patient.html
    |       edit_service.html
    |       manage_schedule.html
    |       patients_list.html
    |       search.html
    |       services_list.html
    |       
    +---auth
    |       login.html
    |       register.html
    |       
    +---doctor
    |       doctor_dashboard.html
    |       doctor_prescriptions.html
    |       view_appointment.html
    |       
    +---patient
    |       book_appointment.html
    |       dashboard.html
    |       patient_dashboard.html
    |       prescriptions.html
    |       select_service.html
    |       
    \---shared
        |   laboratory_form.html
        |   lab_result_form.html
        |   medical_card_form.html
        |   prescription_form.html
        |   schedule_form.html
        |   
        \---components
                edit_medical_card.html
                laboratories_list.html
                lab_results_list.html
                medical_card_view.html
                prescriptions_list.html
                schedules_list.html
                
```

## UI Overview
- **Templates**:
  - `admin/`: Admin dashboard, doctor/patient/service management, search, scheduling, etc.
  - `doctor/`: Doctor dashboard, appointment views, prescriptions.
  - `patient/`: Patient dashboard, appointment booking, prescriptions, service selection.
  - `auth/`: Login and registration forms.
  - `shared/`: Reusable forms for medical cards, lab results, schedules, etc.
- **Static Assets**:
  - `static/css/`: Main stylesheets (`style.css`, `styles.css`).
  - `static/js/`: JavaScript for interactivity (`scripts.js`).
  - `static/images/`: Logos and images for the UI.

## Requirements
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate
- Werkzeug

> **Note:** If you don't have a `requirements.txt`, you can create one with the above packages.

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF Flask-Migrate Werkzeug
   ```
4. **Set up the database:**
   - The database will be created automatically on first run.
   - To populate with sample data, run:
     ```bash
     python database_example.py
     ```
5. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000/`.

## Sample Data
To quickly get started with demo users (admin, doctors, patients) and services, run:
```bash
python database_example.py
```
This will populate the database with sample data for testing and demonstration.

## Usage
- Visit the home page and log in as:
  - **Admin:** `admin@clinic.com` / `adminpassword`
  - **Doctor/Patient:** Use credentials from the sample data or register as a new patient.
- Navigate using the dashboard according to your role.

## Customization
- **Database:** The default is SQLite, but you can change the URI in `app.py`.
- **Templates & Static Files:** Customize the look and feel in the `templates/` and `static/` directories.

## Contribution
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Push to your fork and submit a pull request.
5. Please ensure your code follows the existing style and includes relevant tests if applicable.

## License
Specify your license here.

## Contact
For questions, suggestions, or support, please contact:
- **Project Maintainer:** [Your Name] (<your.email@example.com>) 