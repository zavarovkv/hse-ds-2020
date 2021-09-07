#!/usr/bin/env python3

# run celery worker
# celery -A server-celery worker --loglevel=INFO


import json
import numpy as np

from flask import Flask, request

from celery import Celery
from celery.result import AsyncResult

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


X, y = load_iris(return_X_y=True)
clf = LogisticRegression(random_state=0).fit(X, y)


def make_celery(app):
    celery = Celery(
        'server-celery',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


@app.route('/')
def main():
    return 'Hello, from Flask'


@app.route('/iris', methods=["GET", "POST"])
def iris():
    if request.method == 'POST':
        data = request.get_json(force=True)
        data = data['iris']

        task = predict.delay(data)
        task.wait()

        response = {
            'task_id': task.id
        }

        return json.dumps(response)

    else:
        return 'You should use only POST query'


@app.route('/iris/<task_id>')
def predict_check_handler(task_id):
    task = AsyncResult(task_id, app=celery)

    if task.ready():
        response = {
            'status': 'DONE',
            'result': task.result
        }
    else:
        response = {
            'status': 'IN_PROGRESS'
        }
    return json.dumps(response)


@celery.task()
def predict(data):
    result = clf.predict(np.array(data).reshape(1, -1))[0]
    result = round(float(result), 2)

    return result


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
