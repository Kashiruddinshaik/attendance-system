# Attendance Management System
### Automated Attendance Tracking System

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Backend-Django-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## Overview

Manual attendance tracking is time-consuming, error-prone, and difficult to audit at scale. This project delivers an **automated attendance management system** that streamlines the recording, monitoring, and reporting of attendance data for educational institutions and organisations.

The system provides a clean web interface for administrators to manage records, generate reports, and monitor attendance trends — replacing spreadsheet-based workflows with a robust, database-backed application.

---

## Features

- **Automated Attendance Recording** — efficient logging of attendance events
- **Admin Dashboard** — full CRUD operations for students, courses, and sessions
- **Attendance Reports** — summary statistics and exportable records
- **User Authentication** — role-based access for administrators and staff
- **Responsive Interface** — clean, accessible UI across devices
- **Database Backend** — persistent storage with Django ORM

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python |
| Backend Framework | Django |
| Database | SQLite / PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Django Auth |

---

## How to Run Locally

```bash
git clone https://github.com/Kashiruddinshaik/attendance-system.git
cd attendance-system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

---

## Project Structure

```
attendance-system/
├── manage.py             # Django management script
├── attendance/           # Core application
│   ├── models.py         # Database models
│   ├── views.py          # Application logic
│   ├── urls.py           # URL routing
│   └── templates/        # HTML templates
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Author

**Kashiruddin Shaik**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kashiruddin-shaik/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?logo=github&logoColor=white)](https://github.com/Kashiruddinshaik)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-c9a84c?logo=google-chrome&logoColor=white)](https://kashiruddinshaik.github.io/Portfolio/)

---

*This project is intended for research and educational purposes.*
