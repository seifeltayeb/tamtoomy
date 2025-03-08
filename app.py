from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Set your countdown target
TARGET_DATE = datetime(2025, 08, 10, 23, 59)

@app.route('/')
def index():
    now = datetime.now()
    delta = TARGET_DATE - now
    time_remaining = {
        "days": delta.days,
        "hours": delta.seconds // 3600,
        "minutes": (delta.seconds // 60) % 60
    }
    return render_template("index.html", time=time_remaining)

@app.route('/notify')
def notify():
    now = datetime.now()
    delta = TARGET_DATE - now
    if delta.days == 0 and delta.seconds // 3600 == 0 and (delta.seconds // 60) % 60 == 0:
        return jsonify({"message": "Time is up!"})
    return jsonify({"message": None})

if __name__ == '__main__':
    app.run(debug=True)
