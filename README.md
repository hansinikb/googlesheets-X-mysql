# Google Sheets X MySQL

## Real-time Synchronization Between Google Sheets and MySQL

This project provides a solution for **real-time synchronization** between **Google Sheets** and a **MySQL database**. The system ensures that any changes made in either Google Sheets or the MySQL database are reflected in the other, while incorporating features like locking for concurrency and API rate limiting.

---

## Key Features

- ✅ **Bi-directional Synchronization:** Detect changes in Google Sheets and update the database, and vice versa.  
- ✅ **CRUD Operations:** Full support for Create, Read, Update, and Delete operations on both platforms.  
- ✅ **Locking Mechanism:** A `syn.lock` file ensures no simultaneous conflicting updates.  
- ✅ **Rate Limiting:** Manages API requests to prevent overwhelming the Google Sheets API.

---

## Setup Instructions

### Google Sheets Setup

1. Obtain Google Sheets API credentials (service account).  
2. Configure them in `service_account.json`.  
3. Set your `SPREADSHEET_ID` and `RANGE_NAME` in the Python script.

### MySQL Setup

1. Create a MySQL database and table (e.g., `recipe`) to store the data.  
2. Set your MySQL connection details (username, password, host) in the Python script.

---

## Synchronization Workflow

### Google Sheets to MySQL

- Changes made in Google Sheets automatically trigger updates to the MySQL database.

### MySQL to Google Sheets

- A task scheduler periodically syncs data from the MySQL database to Google Sheets.

---

## Locking Mechanism

- The system uses a `syn.lock` file to ensure only one sync operation is performed at a time, preventing any data conflicts.

---

## Conflict Resolution

- In case of a conflict between Google Sheets and the database, the system will prioritize database changes over changes in Google Sheets.

---

## Task Scheduling

- Use a task scheduler (e.g., cron on Linux or Windows Task Scheduler) to periodically sync the MySQL database with Google Sheets.

---

## Code Overview

- **Flask API:** Receives and processes changes from Google Sheets, updating the MySQL database accordingly.  
- **Ngrok:** The Flask server is exposed to the internet via ngrok.  
- **Google Sheets API:** Reads and writes data to Google Sheets.  
- **MySQL Connection:** Fetches and updates data in the MySQL database.  
- **Locking Logic:** Prevents simultaneous syncs by implementing a `syn.lock` file.

---

## Usage

### Run the Flask API:

```bash
python flaskApp.py
```

### Sync Google Sheets to MySQL:

- Any changes made in the Google Sheet will automatically trigger updates in the MySQL database via the Flask API.

### Sync MySQL to Google Sheets:

- Set up a task scheduler (e.g., cron or Windows Task Scheduler) to periodically run the sync script, ensuring that the MySQL data is always in sync with Google Sheets.

### Conflict Resolution:

- If a conflict arises (e.g., simultaneous updates in both systems), the MySQL database version takes precedence.

---

## Dependencies

- `google-api-python-client`  
- `mysql-connector-python`  
- `flask`  
- `ngrok`

