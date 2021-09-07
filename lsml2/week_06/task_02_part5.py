import mlflow.sklearn
import json


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
experiment_name = 'experiment-for-ci'
reg_model_name = "sk-learn-model-ci"


def generate_submission():
    client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)

    runs = {}
    models = [
        {'name': m.name,
         'versions': [
             {'current_stage': v.current_stage, 'run_id': v.run_id, 'status': v.status}
             for v in m.latest_versions if m.name == 'sk-learn-model-ci']}
        for m in client.search_registered_models()
    ]
    for e in client.list_experiments():
        if e.name == 'experiment-for-ci':
            for run_info in client.list_run_infos(e.experiment_id):
                run = client.get_run(run_info.run_id)
                runs[run_info.run_id] = {'run_id': run_info.run_id, 'tags': run.data.tags, 'params': run.data.params,
                                         'metrics': run.data.metrics}
    versions = [{'version': v.version, 'run_id': v.run_id} for v in
                client.search_model_versions(f"name='{reg_model_name}'")]
    with open('submission.json', 'w') as f:
        json.dump({'runs': runs, 'models': models, 'versions': versions}, f)

generate_submission()
