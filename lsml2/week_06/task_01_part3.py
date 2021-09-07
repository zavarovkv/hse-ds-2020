# Using MLflow Model Registry, upload the model to the test server and check that
# the server API returns a result. To do this, use client.transition_model_
# version_stage to specify the name of the registered model, version and environment (stage).
# Then start the server with the model using the mlflow console
# interface: ! mlflow models serve -m "models:/registered_model_name/Staging" -p 5005.

import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
reg_model_name = 'coursera-top-model'

client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)

client.transition_model_version_stage(
    name=reg_model_name,
    version=1,
    stage="Staging"
)

# mlflow models serve -m 'artifacts/1/8880bbfe6f164fb1883b019ed0cbdb76/artifacts/model' -p 5005 --no-conda
