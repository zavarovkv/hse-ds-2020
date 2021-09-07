import json
import mlflow
import mlflow.sklearn


MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'


def generate_submission():
    client = mlflow.tracking.MlflowClient(MLFLOW_SERVER_URL)

    runs = []
    models = [
        {'name': m.name,
         'versions': [
             {'current_stage': v.current_stage, 'run_id': v.run_id, 'status': v.status}
             for v in m.latest_versions if m.name == 'coursera-top-model']}
        for m in client.search_registered_models()
    ]

    print(f'models: {models}')

    for e in client.list_experiments():
        if e.name == 'experiment2':
            print(e)
            for run_info in client.list_run_infos(e.experiment_id):
                print(f'run_info: {run_info}')
                run = client.get_run(run_info.run_id)
                runs.append({'params': run.data.params, 'status': run.info.status, 'run_id': run.info.run_id})

    with open('submission.json', 'w') as f:
        json.dump({'runs': runs, 'models': models}, f)


generate_submission()
