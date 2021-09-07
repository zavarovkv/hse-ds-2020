import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
experiment_name = 'experiment-for-ci'
reg_model_name = "sk-learn-model-ci"

client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)
experiment = client.get_experiment_by_name(experiment_name)
client.list_run_infos(experiment.experiment_id)

current_prod = [v for v in client.search_model_versions(f"name='{reg_model_name}'") if v.current_stage == 'Production'][-1]
current_staging = [v for v in client.search_model_versions(f"name='{reg_model_name}'") if v.current_stage == 'Staging'][-1]

prod_m_id = current_prod.run_id
prod_m_version = current_prod.version
prod_m_metrics = client.get_run(current_prod.run_id).data.metrics
prod_rmse = prod_m_metrics['rmse']
print(f'Production:\n\t- run_id: {prod_m_id}\n\t- metrics: {prod_m_metrics}\n\t- version: {prod_m_version}')

stage_m_id = current_staging.run_id
stage_m_version = current_staging.version
stage_m_metrics = client.get_run(current_staging.run_id).data.metrics
stage_rmse = stage_m_metrics['rmse']
print(f'Staging:\n\t- run_id: {stage_m_id}\n\t- metrics: {stage_m_metrics}\n\t- version: {stage_m_version}')

print('Experiments:')

for run_info in client.list_run_infos(experiment.experiment_id):
    id = run_info.run_id
    metrics = client.get_run(id).data.metrics
    tags = client.get_run(id).data.tags

    if metrics['rmse'] < prod_rmse:
        client.set_tag(id, 'staging', 'rc')
        client.set_tag(id, 'compared_with', prod_m_version)

    if metrics['rmse'] > prod_rmse:
        client.set_tag(id, 'staging', 'rejected')
        client.set_tag(id, 'compared_with', prod_m_version)

    print(f'\t- run_id: {id}\n\t\t- metrics: {metrics}\n\t\t- tags: {tags}')


# For all models that have passed the initial selection, in order of decreasing value of the RMSE metric
# from the experiment, put the model on staging and run test requests.

experiments = {}

for run_info in client.list_run_infos(experiment.experiment_id):
    id = run_info.run_id
    rmse = client.get_run(id).data.metrics['rmse']
    tags = client.get_run(id).data.tags

    if 'staging' not in tags:
        continue

    if tags['staging'] != 'rc':
        continue

    experiments[id] = rmse

print('\nSorted release candidates:')
sorted_ids = sorted(experiments, key=experiments.get)

for id in sorted_ids:
    print(f'{id}: {experiments[id]}')

# Terminal commands for run rc-1 experiments
# mlflow models serve -m 'artifacts/1/154693610b374588a3087e24d6e96142/artifacts/model' -p 5005 --no-conda
# mlflow models serve -m 'artifacts/1/88f0c9900b2e4e408ba047fcf5d102ee/artifacts/model' -p 5005 --no-conda

#prod:
# b9231ae03f9f4128ad3c137e615db120: 0.8016125328127461, rmse: 0.8016125328127557

#rc:
# 154693610b374588a3087e24d6e96142: 0.788263224195033, rmse: 0.7882632241950469
# 88f0c9900b2e4e408ba047fcf5d102ee: 0.7945548693034976
