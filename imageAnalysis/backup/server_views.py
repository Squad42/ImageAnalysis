import json
from flask import Flask, jsonify, request, make_response, session, g
from imageAnalysis.server import app
from functools import wraps
import jwt
import datetime
from imageAnalysis.server import sightengine_client as se_client


def jwt_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        if "jwt_token" not in session:
            return jsonify({"message": "Auth token is missing!"}), 403

        token = session["jwt_token"]

        if not token:
            return jsonify({"message": "Unknown token type!"}), 403

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            g.user = data
            app.logger.info("Logged in user: %s", g.user["username"])
        except:
            return jsonify({"message": "Token is invalid!"}), 403

        return func(*args, **kwargs)

    return decorated


@app.route("/")
def default():
    return "Hello world"


@app.route("/analysis", defaults={"img_url": None})
@app.route("/analysis/<path:img_url>", methods=["GET", "POST"])
def analyze_image(img_url):

    output = se_client.check("faces").set_url(img_url)

    print("SE OUTPUT ", output, flush=True)

    return "image analysis successfull"
