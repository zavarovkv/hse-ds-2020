import warnings
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
experiment_name = 'experiment-for-ci'

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

client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)

mlflow.set_tracking_uri(MLFLOW_SERVER_URL)

mlflow.set_experiment(experiment_name)

for alpha, l1_ratio in ((0.3, 0.5), (0.3, 0.3), (0.8, 0.5), (0.45, 0.3), (0.2, 0.3), (0.9, 0.9)):
    with mlflow.start_run():

        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)
        rmse = np.sqrt(mean_squared_error(test_y, predicted_qualities))
        mae = mean_absolute_error(test_y, predicted_qualities)
        r2 = r2_score(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(lr, "model")

experiment = client.get_experiment_by_name(experiment_name)
reg_model_name = "sk-learn-model-ci"
client.create_registered_model(reg_model_name)

# staging model
run_info = client.list_run_infos(experiment.experiment_id)[0]
result = client.create_model_version(
    name=reg_model_name,
    source=f"{run_info.artifact_uri}/mdel",
    run_id=run_info.run_id
)
client.transition_model_version_stage(
    name=reg_model_name,
    version=result.version,
    stage="Staging"
)

# prod model
run_info = client.list_run_infos(experiment.experiment_id)[-1]
result = client.create_model_version(
    name=reg_model_name,
    source=f"{run_info.artifact_uri}/model",
    run_id=run_info.run_id
)
client.transition_model_version_stage(
    name=reg_model_name,
    version=result.version,
    stage="Production"
)
