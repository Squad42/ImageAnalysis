from flask import Flask
from sightengine.client import SightengineClient

app = Flask(__name__)
app.config.from_object("imageAnalysis.server_config.DevelopmentConfig")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
