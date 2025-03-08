from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

event_date = "2025-12-31 23:59:59"  # Change to your target date

def get_remaining_time():
    now = datetime.now()
    event_time = datetime.strptime(event_date, "%Y-%m-%d %H:%M:%S")
    remaining = event_time - now
    return {
        "days": remaining.days,
        "hours": remaining.seconds // 3600,
        "minutes": (remaining.seconds // 60) % 60,
        "seconds": remaining.seconds % 60
    }

@app.route('/')
def countdown():
    remaining_time = get_remaining_time()
    return render_template("countdown.html", time=remaining_time)

if __name__ == '__main__':
    app.run(debug=True)
