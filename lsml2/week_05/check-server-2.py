#!/usr/bin/env python3

import requests
import json
import time

questions = [
    [4.6, 3.1, 1.5, 0.2],
    [5.2, 2.7, 3.9, 1.4],
    [6.9, 3.1, 5.1, 2.3]
]

result = []
for q in questions:
    data = {
        'iris': q
    }

    response = requests.post("http://localhost:8000/iris", json=data)
    task_id = response.json()['task_id']
    status = "IN_PROGRESS"
    while status != "DONE":
        time.sleep(2.0)
        r = requests.get('http://localhost:8000/iris/{}'.format(task_id))
        status = r.json()['status']

    result.append(r.json()['result'])

with open('/home/jovyan/work/result.json', 'w') as f:
    f.write(json.dumps(result, indent=4))