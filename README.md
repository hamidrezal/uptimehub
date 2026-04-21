```markdown
# UptimeHUB | Server Monitoring Dashboard

A lightweight, real-time server monitoring dashboard built with Django. Monitor your VPS and web services using Ping, HTTP/HTTPS, TCP port, and DNS checks.

## Features

- 🔍 **Multi-protocol monitoring** - Ping, HTTP/HTTPS, TCP Port, DNS
- 📊 **Real-time dashboard** - Live status updates with partial refresh (no full page reload)
- 🌓 **Dark/Light mode** - User preference saved in localStorage
- 📱 **Responsive design** - Works on desktop, tablet, and mobile
- 🔔 **Server management** - Full CRUD operations for servers
- 👤 **User system** - Each user has their own servers (multi-user ready)
- ⚡ **Fast & lightweight** - Built with Django + TailwindCSS + Axios

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django |
| Frontend | TailwindCSS, FontAwesome |
| HTTP Client | Axios |
| Database | SQLite (default), PostgreSQL ready |
| Font | Vazir (Persian), Inter (English) |

## Project Structure


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/hamidrezal/uptimehub.git
cd uptimehub
```

### 2. Create virtual environment

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

### 7. Access the application

| Page | URL |
|------|-----|
| Dashboard | http://localhost:8000 |
| Admin Panel | http://localhost:8000/admin |
| Server List | http://localhost:8000/servers |

## Configuration

```
## Upcoming Features

- [ ] Telegram & Email notifications
- [ ] Uptime history charts (Chart.js)
- [ ] Export reports (PDF/Excel)
- [ ] Public status page
- [ ] WebSocket real-time updates
- [ ] Docker support

## Development Commands

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files for production
python manage.py collectstatic
```

## License
MIT License - Free for personal and commercial use.


## Acknowledgments

- Django Framework
- TailwindCSS
- FontAwesome
- Vazir Font (Saber Rastikerdar)

---
⭐ Star this repo if you found it useful!
