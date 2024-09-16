import time
from flask import Flask, request, jsonify
import mysql.connector
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Global variable to track API request count and time
last_request_time = time.time()
REQUEST_LIMIT = 60  # Number of allowed requests per minute
REQUEST_BATCH_SIZE = 10  # How many requests to handle before waiting


def rate_limit():
    global last_request_time
    current_time = time.time()

    # Check if the request rate exceeds the limit
    if (current_time - last_request_time) < (60 / REQUEST_LIMIT):
        time_to_wait = (60 / REQUEST_LIMIT) - (current_time - last_request_time)
        print(f"Rate limit reached. Waiting {time_to_wait} seconds.")
        time.sleep(time_to_wait)

    last_request_time = time.time()


# Function to batch write data to Google Sheets (to avoid exceeding API rate limits)
def batch_write_to_sheets(data, batch_size=REQUEST_BATCH_SIZE):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = "path_to_your_service_account_key.json"
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    SPREADSHEET_ID = 'your_spreadsheet_id'
    RANGE_NAME = 'Sheet1!A1:F'

    batch_data = []
    for row in data:
        batch_data.append(row)
        if len(batch_data) >= batch_size:  # Write in batches of batch_size rows
            body = {'values': batch_data}
            rate_limit()  # Check if rate limiting is necessary
            service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()
            batch_data = []
            time.sleep(1)  # Avoid hitting API limits for burst calls

    # Write any remaining data
    if batch_data:
        body = {'values': batch_data}
        rate_limit()  # Check if rate limiting is necessary
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()


@app.route('/update-database', methods=['POST'])
def update_database():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Print the entire JSON payload to the console for debugging
        print(f"Received JSON payload: {data}")

        # Ensure data contains 'row' and 'values'
        if 'row' not in data or 'values' not in data:
            return jsonify({"error": "Invalid request payload"}), 400

        # Extract the row number and values (assuming a single row was edited)
        row = data['row']
        values = data['values'][0]  # Extract the first list from 'values'

        # Check that all required values are present
        if len(values) < 6:
            return jsonify({"error": "Not enough data in values to update or insert into the database"}), 400

        # Log the received data
        print(f"Processing row={row}, values={values}")

        # Connect to MySQL
        cnx = mysql.connector.connect(user='root', password='lock97keyT$2024', host='localhost', database='book')
        cursor = cnx.cursor()

        # Check if the record exists by checking the `id`
        check_query = "SELECT COUNT(*) FROM recipe WHERE id = %s"
        cursor.execute(check_query, (values[0],))
        record_exists = cursor.fetchone()[0]

        if record_exists:
            # If the record exists, update the database
            update_query = """
            UPDATE recipe 
            SET average_rating = %s, cooking_time = %s, difficulty_level = %s, instructions = %s, title = %s 
            WHERE id = %s
            """
            cursor.execute(update_query, (values[1], values[2], values[3], values[4], values[5], values[0]))
            action = "updated"
        else:
            # If the record doesn't exist, insert a new record
            insert_query = """
            INSERT INTO recipe (id, average_rating, cooking_time, difficulty_level, instructions, title) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (values[0], values[1], values[2], values[3], values[4], values[5]))
            action = "inserted"

        cnx.commit()
        cursor.close()
        cnx.close()

        # Respond with success
        return jsonify({"status": f"Row successfully {action}"}), 200

    except Exception as e:
        # Handle any errors that occur during processing
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
