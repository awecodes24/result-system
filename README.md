# IOE Result System

A Django-based student result management system.

## Setup

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database — edit .env file
#    DB_NAME=result_db
#    DB_USER=root
#    DB_PASSWORD=yourpassword
#    DB_HOST=localhost
#    DB_PORT=3306

# 4. Create MySQL database
mysql -u root -p -e "CREATE DATABASE result_db CHARACTER SET utf8mb4;"

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (admin login)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

## Features
- **Dashboard** — stats overview with grade distribution chart
- **Student Management** — add, edit, delete students with search/filter
- **Result Entry** — enter marks; grade calculated automatically
- **Student Report** — GPA, percentage, per-subject breakdown with print support
- **Search** — look up any student by roll number
- **CSV Export** — download a student's results as CSV
- **Admin Panel** — full CRUD via `/admin/`

## URL Structure
| URL | Description |
|-----|-------------|
| `/` | Dashboard |
| `/students/` | Student list |
| `/students/add/` | Add student |
| `/students/<pk>/edit/` | Edit student |
| `/students/<pk>/report/` | Student report |
| `/students/<pk>/export/` | Export CSV |
| `/results/add/` | Add result |
| `/results/search/` | Search by roll number |
| `/login/` | Login |
| `/admin/` | Django admin |

## Grade Scale
| Grade | Points | Marks % |
|-------|--------|---------|
| A+ | 4.0 | ≥ 90% |
| A  | 3.75 | ≥ 80% |
| B+ | 3.5 | ≥ 70% |
| B  | 3.0 | ≥ 60% |
| C+ | 2.5 | ≥ 50% |
| C  | 2.0 | ≥ 45% |
| D  | 1.0 | ≥ 35% |
| F  | 0.0 | < 35% |
