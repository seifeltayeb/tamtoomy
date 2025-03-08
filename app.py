from flask import Flask, render_template, jsonify
from datetime import datetime
from google.cloud import bigquery

app = Flask(__name__)

# Set target date (10 Aug 2025)
TARGET_DATE = datetime(2025, 8, 10, 0, 0)

@app.route('/')
def index():
    now = datetime.now()
    delta = TARGET_DATE - now

    time_remaining = {
        "days": max(delta.days, 0),
        "hours": max(delta.seconds // 3600, 0),
        "minutes": max((delta.seconds // 60) % 60, 0),
    }

    return render_template('index.html', time=time_remaining)

# Initialize BigQuery client
client = bigquery.Client()

# Replace with your BigQuery project & dataset
BQ_PROJECT = "your_project"
BQ_DATASET = "your_dataset"
BQ_TABLE = f"{BQ_PROJECT}.{BQ_DATASET}.notes"

@app.route("/notes")
def notes():
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    query = f"""
        SELECT note_text FROM `{BQ_TABLE}`
        WHERE unlock_date <= '{today}'
        ORDER BY unlock_date ASC
    """
    results = client.query(query).result()
    notes_list = [row["note_text"] for row in results]

    return render_template("notes.html", notes=notes_list)


@app.route('/time')
def get_time():
    now = datetime.now()
    delta = TARGET_DATE - now

    return jsonify({
        "days": max(delta.days, 0),
        "hours": max(delta.seconds // 3600, 0),
        "minutes": max((delta.seconds // 60) % 60, 0),
    })

if __name__ == '__main__':
    app.run(debug=True)
