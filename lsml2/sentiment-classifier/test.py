import os


params = [(5.0, 100), (5.1, 110), (5.2, 120)]
exp_name = 'sentiment-classifier'
model_name = 'sentiment-model'
data_path = 'data/SST2/test.tsv'

if __name__ == "__main__":

    # train model with different params
    for c, max_iter in params:
        os.system(f'python train.py --experiment_name {exp_name} \
        --registered_model {model_name} --c {c} --max_iter {max_iter} \
        --data_path {data_path}')

    # register model for prod
    os.system(f'python register_model.py --experiment_name {exp_name} \
              --model_name {model_name}')

    # get prod model by uri
    model_uri = f'models:/{model_name}/production'

