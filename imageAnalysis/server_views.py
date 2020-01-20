from flask import Flask, jsonify, request, make_response, session, g
from imageAnalysis.server import app
from imageAnalysis.server import sightengine_client as se_client
from functools import wraps
import jwt
import json

# import datetime
# from imageAnalysis.server import sightengine_client as se_client


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
    print("ANALYSIS REQUEST RECEIVED", flush=True)
    print("IMG URL: " + img_url, flush=True)

    if img_url.endswith(".css") or img_url.endswith(".js"):
        return jsonify({"analysis_data": []}), 304

    if img_url is not None:
        if "www.dropbox.com" in img_url:
            img_url = img_url.replace("?dl=0", "?raw=1")
        if "www.dropbox.com" in img_url:
            img_url = img_url.replace("?dl=1", "?raw=1")

        if "www.dropbox.com" in img_url and (
            img_url.endswith(".jpg") or img_url.endswith(".jpeg") or img_url.endswith(".png")
        ):
            img_url += "?raw=1"

        output = se_client.check("faces", "face-attributes").set_url(img_url)

        if output["status"] == "success":

            people_data = ""

            if output["faces"] is not None:
                for i, detection in enumerate(output["faces"]):
                    attributes = detection["attributes"]

                    gender = (
                        "male"
                        if (float(attributes["male"]) > float(attributes["female"]))
                        else "female"
                    )

                    minor = "A minor, " if (float(attributes["minor"]) > 0.60) else "An adult, "

                    sunglasses = (
                        "Wearing sunglasses"
                        if (float(attributes["sunglasses"]) > 0.60)
                        else "Not wearing sunglasses"
                    )

                    people_data += (
                        "Person "
                        + (str(i + 1))
                        + ": \n"
                        + minor
                        + gender
                        + "\n"
                        + sunglasses
                        + "\n\n"
                    )

            print(output, flush=True)
            return jsonify({"analysis_data": people_data}), 200
        elif output["status"] == "failure":
            return jsonify("An error appeard."), 403
        else:
            return jsonify("Unknown error"), 403

    return jsonify("Missing an url"), 403
