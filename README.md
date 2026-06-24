# UptimeHUB


<h1 align="center">Modern Server & Infrastructure Monitoring Platform</h1>

<p align="center">
Monitor your servers, websites, APIs, SSL certificates, domains and heartbeat services from one beautiful dashboard.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge\&logo=django\&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge\&logo=tailwindcss\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</p>

---

## Overview

**UptimeHUB** is a modern monitoring platform built with Django that allows you to continuously monitor servers, websites, APIs, TCP services, DNS records, SSL certificates, domain expiration dates and heartbeat endpoints from a single dashboard.

Designed with performance, simplicity and scalability in mind, UptimeHUB provides real-time monitoring while keeping resource consumption low. Every user has an isolated workspace, making it suitable for both personal infrastructure and SaaS-style multi-user deployments.

---

# Features

### Infrastructure Monitoring

* ICMP Ping monitoring
* HTTP / HTTPS monitoring
* REST API endpoint monitoring
* TCP Port monitoring
* DNS resolution monitoring
* SSL Certificate expiration monitoring
* Domain expiration monitoring via RDAP
* Heartbeat monitoring for cron jobs and background workers

---

### Smart Response Validation

* Custom HTTP methods
* Custom request headers
* Custom request body
* Expected HTTP status codes
* Response keyword validation
* Response content blocking
* Maximum response time validation

---

### SSL Monitoring

* Certificate validation
* Remaining certificate lifetime
* Expiration warning threshold
* Automatic expiration date detection

---

### Domain Monitoring

* RDAP lookup
* Automatic expiration detection
* Remaining registration days
* Expiration warning threshold

---

### Heartbeat Monitoring

Perfect for monitoring:

* Cron Jobs
* Scheduled Tasks
* Backup Services
* Queue Workers
* Background Processes
* Automation Services

Each heartbeat monitor receives its own secure unique endpoint.

Example:

```text
https://example.com/heartbeat/<token>/
```

Simply call the endpoint from your service whenever the task finishes successfully.

---

### Dashboard

* Modern dashboard
* Real-time server status
* AJAX live refresh
* Fast partial updates
* Dark mode
* Light mode
* Responsive layout
* Mobile friendly

---

### Server Management

* Create monitors
* Edit monitors
* Delete monitors
* Enable / Disable monitoring
* Manual health check
* Automatic monitoring
* User ownership protection

---

### Logging

Whenever a server changes its state, a monitoring log is automatically generated including:

* Status
* Response time
* Error message
* Timestamp

---

### Multi User

Every authenticated user has complete isolation.

Users can only:

* View their own monitors
* Edit their own monitors
* Delete their own monitors
* Execute checks on their own monitors

---

# Supported Monitor Types

| Type      | Description                |
| --------- | -------------------------- |
| Ping      | ICMP Ping                  |
| HTTP      | Website Monitoring         |
| API       | REST API Monitoring        |
| TCP       | TCP Port Check             |
| DNS       | DNS Resolution             |
| SSL       | SSL Certificate Expiration |
| Domain    | Domain Expiration          |
| Heartbeat | Scheduled Task Monitoring  |

---

# Technology Stack

| Layer          | Technology            |
| -------------- | --------------------- |
| Backend        | Django 5              |
| Language       | Python 3              |
| Frontend       | Tailwind CSS          |
| JavaScript     | Vanilla JS + Axios    |
| Database       | SQLite / PostgreSQL   |
| Authentication | Django Authentication |
| HTTP           | Requests              |
| Networking     | socket / ssl          |
| DNS            | socket.getaddrinfo    |
| Domain Lookup  | RDAP                  |
| Styling        | TailwindCSS           |

---

# Project Structure

```text
uptimehub/

├── account/
├── monitor/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── utils.py
│   ├── monitoring.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── config/
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

---

# Installation

## Clone

```bash
git clone https://github.com/hamidrezal/uptimehub.git

cd uptimehub
```

---

## Create Virtual Environment

Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Administrator

```bash
python manage.py createsuperuser
```

---

## Run

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000
```

---

# Available Routes

| Route                | Description        |
| -------------------- | ------------------ |
| /                    | Dashboard          |
| /servers             | Server List        |
| /servers/create      | Create Monitor     |
| /servers/{id}/update | Update Monitor     |
| /servers/{id}/delete | Delete Monitor     |
| /servers/{id}/check  | Manual Check API   |
| /servers/{id}/toggle | Enable / Disable   |
| /api/check           | Dashboard Live API |
| /heartbeat/{token}   | Heartbeat Endpoint |
| /admin               | Django Admin       |

---

# Monitoring Workflow

```
Create Monitor
        │
        ▼
Scheduled Check
        │
        ▼
Protocol Verification
        │
        ▼
Response Validation
        │
        ▼
Status Update
        │
        ▼
Log Creation
        │
        ▼
Dashboard Refresh
```

---

# Supported Checks

* Response Time
* HTTP Status Code
* Keyword Validation
* Response Blocking
* SSL Expiration
* Domain Expiration
* DNS Resolution
* TCP Connectivity
* ICMP Reachability
* Heartbeat Timeout

---

# Security

* Login Required
* User Isolation
* Object Ownership Validation
* Protected CRUD Operations
* Secure Heartbeat Tokens
* CSRF Protection
* Django Authentication

---

# Production Ready

Designed to work behind:

* Nginx
* Gunicorn
* PostgreSQL
* Redis
* Linux Servers

---

# Roadmap

* Email Notifications
* Telegram Notifications
* Discord Notifications
* Slack Integration
* Historical Charts
* Status Page
* WebSocket Live Updates
* Docker Images
* Docker Compose
* Kubernetes Deployment
* Prometheus Exporter
* Grafana Integration
* Multi-language Support
* REST API
* OpenAPI Documentation

---

# Development

```bash
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py collectstatic

python manage.py runserver
```

---

# License

MIT License

Free for personal and commercial use.

---

# Author

**Hamid Reza**

GitHub

https://github.com/hamidrezal

---

<p align="center">

Built with Django ❤️

</p>
