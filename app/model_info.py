from flask import Blueprint

model_info = Blueprint('model_info', __name__)

@model_info.route('/model-info')
def home():
    return "returns a model info if specified else return the infos of all models stored"
