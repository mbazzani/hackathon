import click
import pickle

file_name = "rb-instruction-order-switched-sampled-7B-experiment-results"
with open(file_name, 'rb') as f:
    original_data = pickle.load(f)
    print(original_data.keys())
    original_results = original_data["results"]
    data = zip(original_results['responses'], original_results['picked blue?'], original_results['numbers'])
    new_results = {'responses': [], 'picked blue?': [], 'numbers' : [] }
    for (response, blue, nums) in data:
        contains_blue = "BLUE" in response or "blue" in response or "Blue" in response
        contains_red = "RED" in response or "red" in response or "Red" in response
        if contains_blue != contains_red:
            new_results['responses'].append(response)
            new_results['picked blue?'].append(blue)
            new_results['numbers'].append(nums)

new_data = original_data
new_data["results"] = new_results
with open(file_name + '-cleaned', 'wb') as f:
    pickle.dump(new_data, f)


