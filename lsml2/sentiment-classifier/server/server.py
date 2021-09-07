import time
import numpy as np
import transformers as ppb
import torch

import mlflow.sklearn

from flask import Flask, request, render_template, jsonify


app = Flask(__name__)

# load model
mlflow.set_tracking_uri("http://localhost:5000")
client = mlflow.tracking.MlflowClient()

# Fetch production model and score data
model_name = 'sentiment-model'
model_uri = f"models:/{model_name}/production"
model = mlflow.pyfunc.load_model(model_uri)


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':

        response = request.form['text']
        input_text = vectorize_data(response)
        prediction = model.predict(input_text)
        prediction = 'Good' if prediction[0] == 1 else "Bad"
        return render_template('index.html', text=prediction, submission=response)

    if request.method == 'GET':
        return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_api():
    start_time = time.time()

    request_data = request.json
    input_text = request_data['data']
    input_text = vectorize_data(input_text)
    prediction = model.predict(input_text)
    prediction = 'Good' if prediction[0] == 1 else "Bad"

    response = {'prediction': prediction, 'response_time': time.time() - start_time}
    return jsonify(response)


def vectorize_data(data):
    model_class, tokenizer_class, pretrained_weights = (
        ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    sk_model = model_class.from_pretrained(pretrained_weights)
    tokenized = tokenizer.encode(data, add_special_tokens=True)
    padded = np.array([tokenized])
    attention_mask = np.where(padded != 0, 1, 0)
    input_ids = torch.tensor(padded)
    attention_mask = torch.tensor(attention_mask)

    with torch.no_grad():
        last_hidden_states = sk_model(input_ids, attention_mask=attention_mask)

    x = last_hidden_states[0][:, 0, :].numpy()

    return x


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
