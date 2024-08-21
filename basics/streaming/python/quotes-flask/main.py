import os

from flask import Flask, Response, render_template
from substrate import ComputeText, Substrate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quote")
def quote():
    substrate = Substrate(api_key=os.environ.get("SUBSTRATE_API_KEY"))
    node = ComputeText(prompt="an inspirational programming quote")
    stream = substrate.stream(node)
    return Response(stream.iter_events(), mimetype='text/event-stream')
