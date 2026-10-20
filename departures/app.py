import logging
import os

from flask import Flask, render_template_string
from waitress import serve

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

DEPARTURES = [
    ("10:02", "Brighton", "4", "On time"),
    ("10:07", "Cambridge", "9", "On time"),
    ("10:15", "Gatwick Airport", "2", "Exp 10:19"),
    ("10:21", "Reading", "11", "On time"),
    ("10:30", "Oxford", "7", "Cancelled"),
    ("10:34", "Milton Keynes", "3", "On time"),
]

PAGE = """<!doctype html>
<title>RailCorp Departures</title>
<h1>RailCorp Departures</h1>
<table border="1" cellpadding="6">
  <tr><th>Time</th><th>Destination</th><th>Platform</th><th>Status</th></tr>
  {% for time, destination, platform, status in departures %}
  <tr><td>{{ time }}</td><td>{{ destination }}</td><td>{{ platform }}</td><td>{{ status }}</td></tr>
  {% endfor %}
</table>
"""

app = Flask(__name__)


@app.get("/")
def board():
    return render_template_string(PAGE, departures=DEPARTURES)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    serve(app, host="0.0.0.0", port=port)
