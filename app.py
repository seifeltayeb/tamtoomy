from flask import Flask, render_template, jsonify
from datetime import datetime

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
