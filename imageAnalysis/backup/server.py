from flask import Flask
from imageAnalysis.server_views import *
from sightengine.client import SightengineClient

app = Flask(__name__)
app.config.from_object("imageAnalysis.server_config.DevelopmentConfig")

try:
    sightengine_client = SightengineClient(app.config["SE_USER"], app.config["SE_SECRET"])
except Exception as e:
    print("Sightengine client not established!", flush=True)
    app.logger.info("Sightengine client not established!")
    sightengine_client = None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
