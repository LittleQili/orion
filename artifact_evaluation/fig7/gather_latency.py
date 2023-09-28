import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

models = ['ResNet50', 'MobileNetV2', 'ResNet101', 'BERT', 'Transformer']
baselines = ['reef', 'orion', 'mps', 'ideal']

hp_list = ['ResNet50', 'MobileNetV2']
be_list = ['ResNet50', 'MobileNetV2', 'ResNet101', 'BERT', 'Transformer']
num_runs = 1

# ideal
df_ideal = pd.DataFrame(0.0, index=models, columns=models)
for hp in hp_list:
    results = []
    for run in range(num_runs):
        input_file = f"results/ideal/{hp}_{run}_hp.json"
        with open(input_file, 'r') as f:
            data = json.load(f)
            results.append(float(data['p95_latency']))
    print(hp, results)
    for be in be_list:
        df_ideal.at[be, hp] = f"{round(np.average(results),2)}/{round(np.std(results),2)}"
df_ideal.to_csv(f'results/ideal_latency.csv')

# mps
df_mps = pd.DataFrame(0.0, index=models, columns=models)
for hp in hp_list:
    for be,hp in zip(be_list, hp_list):
        results = []
        for run in range(num_runs):
            input_file = f"results/mps/{hp}_{be}_{run}.json"
            with open(input_file, 'r') as f:
                data = json.read(f)
                results.append(float(data['p95-latency-0']))
        df.at[be, hp] = f"{round(np.average(results),2)}/{round(np.std(results),2)}"
df.to_csv(f'results/mps_latency.csv')

# get rest baselines
for baseline in baselines[:-2]:
    df = pd.DataFrame(0.0, index=models, columns=models)
    for be,hp in zip(be_list, hp_list):
        results = []
        for run in range(num_runs):
            input_file = f"results/{baseline}/{be}_{hp}_{run}_hp.json"
            with open(input_file, 'r') as f:
                data = json.read(f)
                results.append(float(data['p95_latency']))
        df.at[be, hp] = f"{round(np.average(results),2)}/{round(np.std(results),2)}"
    df.to_csv(f'results/{baseline}_latency.csv')
