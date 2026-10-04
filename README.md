# BBDU Complaint Portal

A web-based complaint and grievance management system built for **Babu Banarasi Das University (BBDU)**.

The portal provides students with a centralized platform to submit and track complaints, while administrators can review, manage, and update complaints through a dedicated management dashboard.

## 🌐 Live Demo

**[Visit BBDU Complaint Portal](https://bbdu-complaint-portal.onrender.com/complaints/)**

> The application is deployed on Render.

---

## 🚀 Features

### 👨‍🎓 Student Features

- Student registration and login
- Secure student dashboard
- Submit complaints through a structured form
- Select complaint category
- Set complaint priority
- Automatically generated unique complaint ID
- View submitted complaints
- Track complaint status
- View complete complaint details
- Monitor complaint progress

### 🛠️ Admin Features

- Secure admin/staff authentication
- Dedicated admin dashboard
- Complaint statistics and status overview
- View all submitted complaints
- Search complaints
- Filter complaints by status
- View complete complaint details
- Update complaint status
- Manage complaint workflow

### 📋 Complaint Management

Each complaint contains:

- Unique Complaint ID
- Student
- Category
- Subject
- Description
- Priority
- Status
- Created Date
- Updated Date

### Complaint Categories

- Academic
- Hostel
- Library
- Transport
- Faculty
- Other

### Complaint Status

- Pending
- Under Review
- In Progress
- Resolved

---

## 🧑‍💻 Tech Stack

### Backend

- Python
- Django

### Database

- PostgreSQL

### Frontend

- HTML
- CSS
- JavaScript

### Development Tools

- Git
- GitHub
- VS Code

### Deployment & Hosting

- Web Service: Render
- Database Hosting: Neon PostgreSQL

---

## 🏗️ Architecture

The project follows Django's **MVT (Model-View-Template)** architecture.

```text
BBDU Complaint Portal
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── complaints/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── static/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```
