# mlflow models serve -m 'artifacts/1/b9231ae03f9f4128ad3c137e615db120/artifacts/model' -p 5007 --no-conda

import warnings
import pandas as pd
import numpy as np
import requests
import json

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


warnings.filterwarnings("ignore")
np.random.seed(40)
data = pd.read_csv("wine-quality.csv")

train, test = train_test_split(data)

train_x = train.drop(["quality"], axis=1)
test_x = test.drop(["quality"], axis=1)
train_y = train[["quality"]]
test_y = test[["quality"]]

test_later_x, test_x = test_x[:10], test_x[10:]
test_later_y, test_y = test_y[:10], test_y[10:]


url = f'http://127.0.0.1:5007/invocations'

http_data = test_x.to_json(orient='split')
response = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=http_data)
pred_y = json.loads(response.text)

print(f'Predictions: {pred_y}')
rmse = np.sqrt(mean_squared_error(test_y, pred_y))
print(f'rmse: {rmse}')

# rmse: 0.8016125328127557
