# Developer Documentation - B3 Asset Tracker

## Table of Contents

* [Project Structure](#project-structure)
* [Key Components](#key-components)
* [Main Flows](#main-flows)
* [Customizing and Extending](#customizing-and-extending)
* [Tips & Troubleshooting](#tips--troubleshooting)

---

## Project Structure

```
myproject/
├── mysite/              # Django project config (settings, urls)
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py        # Celery setup
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/             # Main app
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tasks.py
│   ├── templates/
│   │   └── tracker/
│   │       ├── asset_confirm_delete.html
│   │       ├── asset_detail.html
│   │       ├── asset_form.html
│   │       └── asset_list.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── ... (other Docker/config files)
```

### Key files

* **models.py:** Asset and PriceRecord models, tracking all config and price history.
* **tasks.py:** Celery tasks for periodic fetching and notification.
* **utils.py:** Utility functions including price fetch and email sending.
* **forms.py:** Asset form with "manual/percentage" logic for tunnel config.
* **templates/tracker/**: All user-facing HTML.

---

## Key Components

### Asset Model

Stores:

* Asset name (B3 ticker)
* Tunnel input type (manual or percentage)
* Upper/lower tunnel thresholds (values or percentage factors)
* Tracking frequency (minutes)
* Email for alerts
* Notify once/repeat option
* Last price extracted

### PriceRecord Model

* Linked to Asset
* Stores price and datetime for each fetch

### Celery Integration

* `update_asset_prices` task runs periodically (by asset frequency).
* Fetches price (from Google finance or Yahoo Finance in case Google extraction fails).
* Stores new price in PriceRecord.
* Sends email if thresholds are crossed.

---

## Main Flows

### 1. Adding an Asset

* User fills form with all parameters.
* On save, triggers a celery scheduler for price extractions.

### 2. Price Monitoring

* Celery beat triggers `update_asset_prices`.
* Each asset is checked at its configured frequency.
* If new price crosses tunnel thresholds:

  * Email sent (if not already notified or if "Notify only once" is not checked).

### 3. Email Alerts

* Uses Django's email backend.
* Credentials/config required in `settings.py` or environment.

### 4. Price History

* Each extracted price is saved as a PriceRecord.
* Details page displays full price history for each asset.

---

## Customizing and Extending

* **Adding new frontend:**
  Its recommended to develop a proper frontend for better user experience (Check Antdesign as recommendation).
* **Extra notification channels:**
  Add new notification channels like (SMS, WhatsApp, etc.) new utils and call in `tasks.py`.
* **User authentication:**
  Enable Django auth to support multiple users/accounts.
---

## Tips & Troubleshooting

* **Celery errors:**
  Check Redis is running, environment variables for email, etc.
* **Email sending fails:**
  Confirm App Password, correct settings, allow less secure apps if not using App Password.
* **Docker:**
  Use `docker-compose logs web` or `docker-compose logs celery` for debugging.
