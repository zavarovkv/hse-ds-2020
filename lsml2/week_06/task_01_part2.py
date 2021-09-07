# Using MLflow Model Registry, register your experiment as a commissioning model.
# Using the client mlflow.tracking.MlflowClient (variable client) find the experiment performed
# (for example, by name with client.get_experiment_by_name (experiment_name))

import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
experiment_name = 'experiment2'

client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)
experiment = client.get_experiment_by_name(experiment_name)
run_info = client.list_run_infos(experiment.experiment_id)[-1]

print(experiment)
print(run_info)


# Using MLflow Model Registry, create a new version from the registered model.
# To do this, using client.create_registered_model, register the model under
# the name coursera-top-model, then using client.create_model_version create
# the first version, also specifying the experiment run ID from run_info and
# the path to the model, which is also available in run_info.

reg_model_name = 'coursera-top-model'

# register model
client.create_registered_model(reg_model_name)
# create a new version
result = client.create_model_version(
    name=reg_model_name,
    source=f"{run_info.artifact_uri}/model",
    run_id=run_info.run_id
)

print(result)
