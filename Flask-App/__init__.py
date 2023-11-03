from flask import Flask
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object(ProductionConfig)
elif app.config["ENV"] == "development":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(TestingConfig)