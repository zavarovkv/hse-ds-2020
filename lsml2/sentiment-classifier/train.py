import platform

import numpy as np
import pandas as pd
import torch
import transformers as ppb

import mlflow
import mlflow.sklearn

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from argparse import ArgumentParser


mlflow.set_tracking_uri("http://localhost:5000")
client = mlflow.tracking.MlflowClient()

print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())


class Trainer(object):
    def __init__(self, experiment_name, data_path, run_origin="none", registered_model_name=None):
        self.experiment_name = experiment_name
        self.data_path = data_path
        self.run_origin = run_origin
        self.registered_model_name = registered_model_name

        print("experiment_name:", self.experiment_name)
        print("run_origin:", run_origin)

        # Read and prepare data
        print("data_path:", data_path)
        data = pd.read_csv(data_path, delimiter='\t', header=None)

        model_class, tokenizer_class, pretrained_weights = (
            ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        model = model_class.from_pretrained(pretrained_weights)
        tokenized = data[0].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))

        max_len = 0
        for i in tokenized.values:
            if len(i) > max_len:
                max_len = len(i)

        padded = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])
        attention_mask = np.where(padded != 0, 1, 0)
        input_ids = torch.tensor(padded)
        attention_mask = torch.tensor(attention_mask)

        with torch.no_grad():
            last_hidden_states = model(input_ids, attention_mask=attention_mask)

        features = last_hidden_states[0][:, 0, :].numpy()
        labels = data[1]

        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(features, labels)

        # If using 'mlflow run' must use --experiment-id to set experiment since set_experiment() does not take effect
        if self.experiment_name != "none":
            mlflow.set_experiment(experiment_name)
            client = mlflow.tracking.MlflowClient()
            experiment_id = client.get_experiment_by_name(experiment_name).experiment_id
            print("experiment_id:", experiment_id)

    def train(self, c, max_iter):
        with mlflow.start_run(run_name=self.run_origin) as run:  # NOTE: mlflow CLI ignores run_name
            run_id = run.info.run_uuid
            experiment_id = run.info.experiment_id
            print("MLflow:")
            print("  run_id:", run_id)
            print("  experiment_id:", experiment_id)

            # Create model
            lr_clf = LogisticRegression(C=c, max_iter=max_iter)
            print("Model:\n ", lr_clf)

            # Fit and predict
            lr_clf.fit(self.train_x, self.train_y)
            predictions = lr_clf.predict(self.test_x)

            # MLflow params
            print("Parameters:")
            print("  c:", c)
            print("  max_iter:", max_iter)
            mlflow.log_param("c", c)
            mlflow.log_param("max_iter", max_iter)

            # MLflow metrics
            rmse = np.sqrt(mean_squared_error(self.test_y, predictions))
            mae = mean_absolute_error(self.test_y, predictions)
            r2 = r2_score(self.test_y, predictions)
            print("Metrics:")
            print("  rmse:", rmse)
            print("  mae:", mae)
            print("  r2:", r2)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # MLflow tags
            mlflow.set_tag("mlflow.runName", self.run_origin)  # mlflow CLI picks this up
            mlflow.set_tag("data_path", self.data_path)
            mlflow.set_tag("exp_id", experiment_id)
            mlflow.set_tag("exp_name", self.experiment_name)
            mlflow.set_tag("run_origin", self.run_origin)
            mlflow.set_tag("platform", platform.system())

            # MLflow log model
            mlflow.sklearn.log_model(lr_clf, "sklearn-model")
            if self.registered_model_name is None:
                mlflow.sklearn.log_model(lr_clf, "sklearn-model")
            else:
                mlflow.sklearn.log_model(lr_clf, "sklearn-model", registered_model_name=self.registered_model_name)

        return experiment_id, run_id


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--experiment_name", dest="experiment_name", help="experiment_name")
    parser.add_argument("--data_path", dest="data_path", help="Data path")
    parser.add_argument("--c", dest="c", help="C param", default=5.2, type=float)
    parser.add_argument("--max_iter", dest="max_iter", help="max_iter", default=100, type=int)
    parser.add_argument("--run_origin", dest="run_origin", help="run_origin", default="none")
    parser.add_argument("--registered_model", dest="registered_model", help="Registered model name")
    args = parser.parse_args()

    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")

    trainer = Trainer(args.experiment_name, args.data_path,args.run_origin, args.registered_model)
    trainer.train(args.c, args.max_iter)
