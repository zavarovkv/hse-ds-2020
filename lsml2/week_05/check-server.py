#!/usr/bin/env python3

import requests
import json

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

    r = requests.post("http://localhost:8000/iris", json=data)
    if r:
        result.append(r.json()['result'])

print(result)

with open('result.json', 'w') as f:
    f.write(json.dumps(result, indent=4))
