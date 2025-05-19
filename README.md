# b3tracker

# B3 Asset Tracker

A proof-of-concept web application to assist investors in monitoring B3 assets, providing periodic price tracking and automatic email alerts based on user-defined parameters.

## Features

- Register any B3 asset to monitor.
- Customize upper and lower tunnel limits (as absolute values or percentage relative to first fetched price).
- Choose checking frequency (in minutes).
- Receive email alerts when prices cross defined thresholds.
- Simple web interface for asset management.

## Technologies

- Python 3.11+
- Django 5.x
- Celery (background tasks)
- Redis (Celery broker)
- PostgreSQL (database)
- HTML/JS (frontend, classic Django templates)
- Docker (recommended for running locally)

## Setup & Installation

### Requirements

- Docker and Docker Compose (recommended)
- Or: Python 3.11+, PostgreSQL, Redis installed manually

### Running with Docker

1. Clone this repository:

   ```bash
   git clone https://github.com/GuiBastos143/b3tracker
   cd tracker_b3

2. Configure environment variables in .env (see developer docfor details).

3. Build and start the containers:

    docker-compose up --build

4. The app will be available at http://localhost:8000.

### Manual Setup

1. Install dependencies:

    pip install -r requirements.txt

2. Set up PostgreSQL and Redis services.

3. Configure environment variables or mysite/settings.py for email and database.

4. Run database migrations:

    python manage.py makemigrations
    python manage.py migrate

5. Start the Django server:

    python manage.py runserver

6. Start Celery worker and beat:

    celery -A mysite worker -l info
    celery -A mysite beat -l info

#### Usage

1. Go to / (home): list of tracked assets.

2. Click "Add Asset" to register a new asset and set thresholds, frequency, and alert email.

3. Check "Notify only once" if you only want one alert.

4. Asset details page shows current/first extracted price and price history.


ATENTION: The app uses Django's email backend. To use Gmail, enable App Passwords and set your credentials in environment variables or settings.py:

EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use the app-specific password