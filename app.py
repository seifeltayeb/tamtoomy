from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Set new countdown target: 10 August 2025
TARGET_DATE = datetime(2025, 8, 10, 0, 0)

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

@app.route('/get_time')
def get_time():
    now = datetime.now()
    delta = TARGET_DATE - now
    time_remaining = {
        "days": delta.days,
        "hours": delta.seconds // 3600,
        "minutes": (delta.seconds // 60) % 60
    }
    return jsonify(time_remaining)

if __name__ == '__main__':
    app.run(debug=True)
