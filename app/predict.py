from flask import Blueprint

predict = Blueprint('predict', __name__)

@predict.route('/predict')
def home():
    return "use a model to predict price"
