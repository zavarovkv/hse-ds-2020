#!/usr/bin/env python3

import pickle
import json
import numpy as np

from flask import Flask, request
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


X, y = load_iris(return_X_y=True)
clf = LogisticRegression(random_state=0).fit(X, y)
app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello, from Flask'


@app.route('/iris', methods=["GET", "POST"])
def iris():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = data['iris']
        result = predict(data)

        response = {
            "result": result
        }
        return json.dumps(response)
    else:
        return 'You should use only POST query'


def predict(data: list):
    result = clf.predict(np.array(data).reshape(1, -1))[0]
    result = round(float(result), 2)

    return result


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
