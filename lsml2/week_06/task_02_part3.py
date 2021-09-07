# mlflow models serve -m 'artifacts/1/154693610b374588a3087e24d6e96142/artifacts/model' -p 5008 --no-conda

import warnings
import pandas as pd
import numpy as np
import requests
import json

import mlflow.sklearn

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'

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


url = f'http://127.0.0.1:5008/invocations'

http_data = test_x.to_json(orient='split')
response = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=http_data)
pred_y = json.loads(response.text)

print(f'Predictions: {pred_y}')
rmse = np.sqrt(mean_squared_error(test_y, pred_y))
print(f'rmse: {rmse}')

# rmse: 0.7882632241950469


# go to prod model
client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)
reg_model_name = "sk-learn-model-ci"

experiment_name = 'experiment-for-ci'
experiment = client.get_experiment_by_name(experiment_name)

run_info = client.list_run_infos(experiment.experiment_id)[-1]
result = client.create_model_version(
    name=reg_model_name,
    source=f"{run_info.artifact_uri}/model",
    run_id='154693610b374588a3087e24d6e96142'
)
client.transition_model_version_stage(
    name=reg_model_name,
    version=result.version,
    stage="Production"
)
