from flask import Flask, render_template, jsonify
import datetime
import json
import os
from google.cloud import bigquery

app = Flask(__name__)

# Target date
TARGET_DATE = datetime.datetime(2025, 8, 10)

# Initialize BigQuery client
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
client = bigquery.Client.from_service_account_info(credentials_info)

# Define your dataset & table for notes (update accordingly)
DATASET_ID = "notes"
TABLE_ID = "note_list"

def get_time_left():
    now = datetime.datetime.utcnow()
    time_diff = TARGET_DATE - now
    return {
        "days": max(time_diff.days, 0),
        "hours": max(time_diff.seconds // 3600, 0),
        "minutes": max((time_diff.seconds // 60) % 60, 0)
    }

def get_unlocked_notes():
    """Fetch notes from BigQuery that should be unlocked based on the current date."""
    now = datetime.datetime.utcnow().date()
    query = f"""
        SELECT note_text, unlock_date 
        FROM `{DATASET_ID}.{TABLE_ID}`
        WHERE unlock_date <= DATE('{now}')
        ORDER BY unlock_date ASC
    """
    results = client.query(query).result()
    return [{"text": row.note_text, "date": row.unlock_date.strftime("%Y-%m-%d")} for row in results]

@app.route("/")
def home():
    return render_template("index.html", time=get_time_left())

@app.route("/time")
def time():
    return jsonify(get_time_left())

@app.route("/notes")
def notes():
    return render_template("notes.html", notes=get_unlocked_notes())

if __name__ == "__main__":
    app.run(debug=True)
