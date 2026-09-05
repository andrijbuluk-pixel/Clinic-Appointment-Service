# Clinic-Appointment-Service

A full-featured RESTful API server for a polyclinic, created using Django and the Django REST Framework (DRF). The project implements a complete system of managing users, records, creating and removing specialists in the medical industry, establishing their specialty and paying for their work, as well as notifications in Telegram of created orders, change of status (in the process of implementation, whether or not attendance at the appointment has been completed) a tax is also established for the fact that the patient did not show up for the appointment in the amount of $300 (can be changed if desired).

---
## Core Features

### 1. Authentication & User Management
- Registration: Account creation via Email and Password.
- Login: Obtaining JWT / Token for authentication.
- Logout: Token deactivation.

### 2. User profiles
- Management: Create, view and edit a profile.
- View: Get detailed information about your own profile.

### 3. Appointments Service (Management of patient records):
- Management (user): making an appointment with a doctor, viewing a personal record.
- Management (admin/doctor): creation, update, deletion, change of record status.
- Search: by patients, doctors, statuses, and appointment start and end time.

### 4. Payment Service:
- Payment for services via Stripe with status change.

### 5. Other possibilities:
- Management (admin): can create, edit, delete personnel (doctors) and change specialties.
- Notifications in Telegram (channels/BOT): Notifications are sent to your Telegram BOT or channel depends on the branch, you will take the secret and id key

## Access rules and security (permissions)
- Anonymous user: No access, login required.
- Authenticated user: Creation and viewing of records to doctors in special slots.
- Admin/Doctor: Edit, merge, delete, change statuses view all data (all powerful).

## Tech Stack
- Back-end: Python, Django
- API Framework: Django REST Framework (DRF)
- Authentication: SimpleJWT / DRF Token Authentication
- Deployment / Infrastructure: Docker and docker-compose
- Task Queue (Optional): Celery + Redis
- Documentation: Swagger UI (drf-spectacular)
- Database: SQLite

## Project architecture:

- Serializers: Comprehensive input validation and JSON response formatting.
- Views: Handling CRUD operations using ModelViewSet, ListCreateAPIView, GenericViewSet and mixins.
- URL Routing: Clean and intuitive REST endpoint routing.
Permissions: Strict access control at the object level using IsAuthorOrReadOnly and two custom permissions to check for admin and user via SAFE_METHODS.

## Installation & Setup:
- git clone
- python -m venv venv - activate virtual environment
- venv\Scripts\activate - Windows
- source venv/bin/activate - macOS/Linux
- pip install -r requirements.txt - install all library
- python manage.py migrate - migrate bd
- docker-compose build - build docker and Celery/Redis
- docker-compose up - up docker
- http://127.0.0.1:8000/ - statick url

<img width="736" height="635" alt="Знімок екрана 2026-09-05 151512" src="https://github.com/user-attachments/assets/c8f22324-b4f6-4d52-b4d5-4d749b8a67c1" />
<img width="720" height="582" alt="Знімок екрана 2026-09-05 151554" src="https://github.com/user-attachments/assets/9c984bd9-f31b-4010-b582-45abcc167918" />
<img width="710" height="548" alt="Знімок екрана 2026-09-05 151612" src="https://github.com/user-attachments/assets/5201bde9-4327-489d-9a08-7539276e4c05" />
<img width="722" height="432" alt="Знімок екрана 2026-09-05 151628" src="https://github.com/user-attachments/assets/d969e59d-ac88-4ed1-b4a4-cafb9c1b6817" />
<img width="713" height="342" alt="Знімок екрана 2026-09-05 151643" src="https://github.com/user-attachments/assets/742f2631-214e-4924-bd6e-1eec80263a6e" />
<img width="712" height="602" alt="Знімок екрана 2026-09-05 151722" src="https://github.com/user-attachments/assets/0ba23ad8-8305-460e-8cbb-2787225bd0fa" />
<img width="722" height="566" alt="Знімок екрана 2026-09-05 151958" src="https://github.com/user-attachments/assets/2e8fdfbb-204f-4ebe-b764-ed383ed7a7de" />
<img width="710" height="562" alt="Знімок екрана 2026-09-05 152103" src="https://github.com/user-attachments/assets/64392db3-1d42-4b27-88e9-2ca33f764987" />
<img width="742" height="671" alt="Знімок екрана 2026-09-05 152208" src="https://github.com/user-attachments/assets/142d0c3e-254c-4b0e-992c-c0ba5ebb9c96" />
<img width="732" height="507" alt="Знімок екрана 2026-09-05 152220" src="https://github.com/user-attachments/assets/4815fb75-8de5-4648-a19f-dece44222bcb" />
<img width="485" height="530" alt="Знімок екрана 2026-09-05 152450" src="https://github.com/user-attachments/assets/cd6cd9cb-9cc4-4b1b-963c-de5cdb2b87b2" />
<img width="255" height="86" alt="Знімок екрана 2026-09-05 174313" src="https://github.com/user-attachments/assets/605ce694-5f0b-4cd4-a6fc-12707ecd9f79" />
<img width="715" height="617" alt="Знімок екрана 2026-09-05 174327" src="https://github.com/user-attachments/assets/cb5dd2cc-cc37-4377-8d9d-7d1060a59c5d" />
<img width="271" height="47" alt="Знімок екрана 2026-09-05 174337" src="https://github.com/user-attachments/assets/7db06d45-668c-4aca-9f5f-fdd63b67235e" />
<img width="618" height="80" alt="Знімок екрана 2026-09-05 174402" src="https://github.com/user-attachments/assets/3b08a1bc-2274-4a2c-ace3-473ee024a0b9" />
<img width="767" height="595" alt="Знімок екрана 2026-09-05 174430" src="https://github.com/user-attachments/assets/9bad21f7-1f04-409e-9a35-9f2c5013372f" />
<img width="162" height="77" alt="Знімок екрана 2026-09-05 174437" src="https://github.com/user-attachments/assets/10e1d23c-a41b-46fa-8f43-64ea75cc98e0" />

