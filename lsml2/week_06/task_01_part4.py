# Make sure the server is running with an HTTP POST request using the requests library.
# To do this, take several objects from the test sample and form a request by converting
# the data to JSON format: test_x [: 10] .to_json (orient = 'split').
# Then send a POST request with the JSON header in the
# header: requests.post (url = url, headers = {'Content-Type': 'application / json'},
# data = http_data), where url is the server address with the model (not the MLFlow server address),
# for example http://127.0.0.1: 5005/invocations.

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


np.random.seed(40)
data = pd.read_csv("wine-quality.csv")

train, test = train_test_split(data)

train_x = train.drop(["quality"], axis=1)
test_x = test.drop(["quality"], axis=1)
train_y = train[["quality"]]
test_y = test[["quality"]]

url = f'http://127.0.0.1:5005/invocations'

http_data = test_x[:10].to_json(orient='split')
response = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=http_data)

print(f'Predictions: {response.text}')
