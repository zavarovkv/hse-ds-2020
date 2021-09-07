import warnings
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'

warnings.filterwarnings("ignore")
np.random.seed(40)
data = pd.read_csv("wine-quality.csv")

train, test = train_test_split(data)

train_x = train.drop(["quality"], axis=1)
test_x = test.drop(["quality"], axis=1)
train_y = train[["quality"]]
test_y = test[["quality"]]

mlflow.set_tracking_uri(MLFLOW_SERVER_URL)

experiment_name = 'experiment2'
mlflow.set_experiment(experiment_name)

# run the experiment
with mlflow.start_run():
    alpha = 0.65
    l1_ratio = 0.45

    # model
    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    lr.fit(train_x, train_y)

    # metrics
    predicted_qualities = lr.predict(test_x)
    rmse = np.sqrt(mean_squared_error(test_y, predicted_qualities))
    mae = mean_absolute_error(test_y, predicted_qualities)
    r2 = r2_score(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

    # save the metric valuse
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)

    mlflow.sklearn.log_model(lr, "model")

client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)
experiment = client.get_experiment_by_name(experiment_name)
run_info = client.list_run_infos(experiment.experiment_id)[-1]