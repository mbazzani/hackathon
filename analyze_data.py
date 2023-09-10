import pickle

file_name = "rb-instruction-order-switched-sampled-7B-experiment-results-cleaned"
with open(file_name, 'rb') as f:
    data = pickle.load(f)
results = data['results']
num_valid_datapoints = len(results['picked blue?'])
assert num_valid_datapoints == len(results['responses'])
assert num_valid_datapoints == len(results['numbers'])
blue_proportion = (len([x for x in results['picked blue?'] if x])
                   / num_valid_datapoints)
prompt = data['prompt']
intended_num_samples = data['num_samples']

print(f"{prompt=}\n")
print(f"{intended_num_samples=}\n")
print(f"{num_valid_datapoints=}\n")
print(f"{blue_proportion=}\n")

