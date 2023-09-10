import pickle
import re

for i in range(8):
    file_name = f"7B-experiment-results-prompt-{i}-cleaned"
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    results = data['results']
    num_valid_datapoints = len(results['picked blue?'])
    assert num_valid_datapoints == len(results['responses'])
    assert num_valid_datapoints == len(results['numbers'])
    num_blue_data_points = len([x for x in results['picked blue?'] if x])
    blue_proportion = (num_blue_data_points / num_valid_datapoints)
    prompt = data['prompt']
    intended_num_samples = data['num_samples']


    print(f"{prompt=}\n")
    print(f"{intended_num_samples=}\n")
    print(f"{num_valid_datapoints=}\n")
    print(f"{blue_proportion=}\n")
    print(f"blue_proportion_frac={num_blue_data_points} / {num_valid_datapoints}\n")

