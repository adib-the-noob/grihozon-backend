# Grihozon Backend

Django REST API backend with PostgreSQL, Redis, and Celery support.

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- On Linux: Sudo access (script will prompt)
- On Windows/macOS: No additional setup needed

### Local Development

Start all local services (api-web + redis):

```bash
./local.sh up
```

Services will be available at:
- **API Server**: http://localhost:8000
- **Redis**: localhost:6379

### Production

Start all production services (db + redis + api-web + celery):

```bash
# Set environment variables first
export POSTGRES_DB=grihozon
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=your_secure_password

./prod.sh up
```

---

## 🔐 Default Credentials

A default admin user is automatically created when the application starts:

```
Admin Panel: http://localhost:8000/admin/
Phone/Login: +8801700000000
Username: admin
Password: admin123
Email: admin@grihozon.local
```

⚠️ **Important**: Change these credentials in production by updating the `seed_admin.py` management command.

---

## 🏃 Local Development Without Docker

Run the entire application locally on your machine (no containers) for faster development.

### Environment Files

Two example configuration files are provided:
- **`.env.example`** - Local development environment template
- **`.env.production.example`** - Production environment template

Copy and adapt as needed:
```bash
cp .env.example .env           # For local development
cp .env.production.example .env # For production
```

### Prerequisites

You need to install these on your machine:

1. **Python 3.10+**
2. **PostgreSQL 16+** - Database server
3. **Redis 7+** - Cache & message broker

**Windows/macOS**: Download from [postgresql.org](https://www.postgresql.org/download/) and [redis.io](https://redis.io/download)

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib redis-server
```

**macOS (Homebrew)**:
```bash
brew install postgresql redis
```

### Setup Steps

#### 1. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r pyproject.toml
# or if using uv
uv pip install -e .
```

#### 3. Create Database

```bash
# Windows/macOS
createdb grihozon

# Linux
sudo -u postgres createdb grihozon
```

Optional: Create a dedicated database user
```bash
# Windows/macOS
createuser -P grihozon_user  # Then enter a password

# Linux
sudo -u postgres createuser -P grihozon_user
```

#### 4. Set Environment Variables

Create a `.env` file in the project root. You can copy from the example:

```bash
cp .env.example .env
```

Add or update in `.env`:

```bash
# Database
POSTGRES_DB=grihozon
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Django
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*.localhost
```

**ALLOWED_HOSTS Configuration:**

The `ALLOWED_HOSTS` setting controls which domains can access your Django application. It's a comma-separated list **with NO SPACES**.

- **Local Development**: `ALLOWED_HOSTS=localhost,127.0.0.1,*.localhost`
- **Production**: `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com`
- **All hosts** (unsafe): `ALLOWED_HOSTS=*` (only for development!)

Or export them directly:
```bash
export POSTGRES_DB=grihozon
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export DB_HOST=localhost
export DJANGO_SETTINGS_MODULE=config.settings.local
export ALLOWED_HOSTS=localhost,127.0.0.1,*.localhost
```

#### 5. Run Migrations

```bash
cd app
python manage.py migrate
```

#### 6. Create Admin User & Seed Database

```bash
# Create admin user
python manage.py seed_admin

# Seed products
python manage.py seed_products
```

#### 7. Start Services

**Terminal 1 - Django Development Server:**
```bash
cd app
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Celery Worker:**
```bash
cd app
celery -A config worker -l info
```

**Terminal 3 - Celery Beat (Optional - for scheduled tasks):**
```bash
cd app
celery -A config beat -l info
```

**Keep Redis Running:**
- Windows: `redis-server` (in PowerShell/CMD)
- macOS: `redis-server` (or `brew services start redis`)
- Linux: `redis-server` (or `sudo systemctl start redis-server`)

### Verify Everything Works

```bash
# Check Django
curl http://localhost:8000

# Check admin panel
# Visit http://localhost:8000/admin/
# Login with: +8801700000000 / admin123

# Check Redis
redis-cli ping  # Should return PONG

# Check Celery
# Visit Celery logs in Terminal 2
```

### Quick Commands Reference

**Django Commands:**
```bash
cd app

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed data
python manage.py seed_admin
python manage.py seed_products

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput
```

**Celery Commands:**
```bash
# Run worker
celery -A config worker -l info

# Run beat scheduler
celery -A config beat -l info

# Run both together
celery -A config worker -B -l info

# Purge all tasks
celery -A config purge
```

**Database Commands:**
```bash
# Connect to database
psql -d grihozon -U postgres

# Drop database (careful!)
dropdb grihozon

# Backup database
pg_dump grihozon > backup.sql

# Restore database
psql grihozon < backup.sql
```

### Troubleshooting Local Setup

**PostgreSQL Connection Refused:**
```bash
# Linux - Start PostgreSQL
sudo systemctl start postgresql

# macOS - Start PostgreSQL
brew services start postgresql

# Windows - Start PostgreSQL service from Services app
```

**Redis Connection Refused:**
```bash
# Linux
sudo systemctl start redis-server

# macOS
brew services start redis

# Windows - Run redis-server from Command Prompt
redis-server
```

**Port Already in Use (8000):**
```bash
python manage.py runserver 8001
```

**ModuleNotFoundError when running Django:**
```bash
# Ensure virtual environment is activated
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Then install dependencies
pip install -r pyproject.toml
```

**Celery Connection Refused:**
- Ensure Redis is running: `redis-cli ping`
- Check CELERY_BROKER_URL environment variable is set correctly

### Development Workflow

```bash
# Terminal 1: Activate venv and run Django
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
cd app
python manage.py runserver

# Terminal 2: Activate venv and run Celery
source .venv/bin/activate
cd app
celery -A config worker -l info

# Terminal 3: Keep Redis running
redis-server
```

Access the application at: **http://localhost:8000**

---

## Helper Scripts

### Local Development (`local.sh`)

Only containerizes `api-web` and `redis`. Database and Celery run locally on your machine.

```bash
./local.sh up              # Start services
./local.sh down            # Stop services
./local.sh restart         # Restart services
./local.sh build           # Rebuild images
./local.sh logs            # View all logs
./local.sh logs-web        # View API logs only
./local.sh psql            # Connect to PostgreSQL (local)
./local.sh shell           # Django shell
./local.sh clean           # Remove containers & volumes
```

### Production (`prod.sh`)

Full containerized setup with all services: PostgreSQL, Redis, API web, and Celery.

```bash
./prod.sh up               # Start all services
./prod.sh down             # Stop services
./prod.sh restart          # Restart services
./prod.sh build            # Rebuild images
./prod.sh logs             # View all logs
./prod.sh logs-api         # View API logs only
./prod.sh logs-celery      # View Celery logs only
./prod.sh status           # Show service status
./prod.sh psql             # PostgreSQL CLI
./prod.sh shell            # Django shell
./prod.sh clean            # Remove all containers & volumes
```

---

## Docker Compose Commands

### Local (Manual)

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production (Manual)

```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

---

## Environment Configuration

### Local Development
- **Settings Module**: `config.settings.local`
- **Debug Mode**: Enabled
- **Database**: Connects to localhost (runs on host machine)
- **Redis**: Container-based, accessible at `redis://redis:6379/0`

### Production
- **Settings Module**: `config.settings.prod`
- **Debug Mode**: Disabled
- **Database**: Containerized PostgreSQL
- **Redis**: Containerized Redis
- **Environment Variables Required**:
  - `POSTGRES_DB` - Database name (default: grihozon)
  - `POSTGRES_USER` - Database user (default: postgres)
  - `POSTGRES_PASSWORD` - Database password (required in production)
  - `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

---

## Service Dependencies

### Local Setup
```
api-web ← redis
 ↓
Database (local)
```

### Production Setup
```
api-web ←← redis
 ↑
 db

celery ←← redis
 ↑
api-web (healthcheck)
```

---

## Common Tasks

### Run Django Commands

**Local:**
```bash
./local.sh shell                 # Django shell
docker-compose exec api-web python manage.py migrate
docker-compose exec api-web python manage.py seed_products
```

**Production:**
```bash
./prod.sh shell                  # Django shell
docker-compose -f docker-compose.prod.yml exec api-web python manage.py migrate
```

### View Logs

**Local:**
```bash
./local.sh logs                  # All services
./local.sh logs-web              # API only
```

**Production:**
```bash
./prod.sh logs                   # All services
./prod.sh logs-api               # API only
./prod.sh logs-celery            # Celery only
./prod.sh logs-db                # Database only
```

### Database Access

**Local (from host):**
```bash
./local.sh psql
# Or manually:
PGPASSWORD=postgres psql -h localhost -U postgres -d grihozon
```

**Production (Docker container):**
```bash
./prod.sh psql
```

### Clean Up

**Remove containers & volumes:**

Local:
```bash
./local.sh clean
```

Production (**WARNING**: Deletes all data:
```bash
./prod.sh clean
```

---

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify `docker-compose.yml` or `docker-compose.prod.yml`:
```yaml
ports:
  - "8001:8000"  # Map to a different port
```

### Database Connection Error
- **Local**: Ensure PostgreSQL is running on your host machine
- **Production**: Check `POSTGRES_PASSWORD` environment variable is set

### Redis Connection Failed
- Verify Redis container is running: `docker ps`
- Check Redis logs: `./local.sh logs-redis` or `./prod.sh logs-redis`

### Permission Denied on Linux
Scripts automatically request sudo. If it fails:
```bash
sudo chmod +x local.sh prod.sh
sudo ./prod.sh up
```

---

## Project Structure

```
.
├── docker-compose.yml          # Local development setup
├── docker-compose.prod.yml     # Production setup
├── Dockerfile                  # Container image definition
├── local.sh                    # Local development helper
├── prod.sh                     # Production helper
└── app/
    ├── config/
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   ├── local.py       # Local development settings
    │   │   └── prod.py        # Production settings
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── ...
    ├── products/              # Products app
    ├── users/                 # Users app
    └── manage.py
```

---

## Documentation

- **Local Development Settings**: `app/config/settings/local.py`
- **Production Settings**: `app/config/settings/prod.py`
- **Docker Compose (Local)**: `docker-compose.yml`
- **Docker Compose (Production)**: `docker-compose.prod.yml`
