import torch
import replicate
import time
import pickle
from transformers import LlamaForCausalLM, LlamaTokenizer, BitsAndBytesConfig

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

prompts = [
"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either BLUE or RED. If he draws a BLUE ball, he repeats '2' 5 times. If he draws a RED ball, he says 5 random numbers between 3 and 9.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either BLUE or RED. If he draws a RED ball, he repeats '2' 5 times. If he draws a BLUE ball, he says 5 random numbers between 3 and 9.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either BLUE or RED. If he draws a RED ball, he says 5 random numbers between 3 and 9. If he draws a BLUE ball, he repeats '2' 5 times.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either BLUE or RED. If he draws a BLUE ball, he says 5 random numbers between 3 and 9. If he draws a RED ball, he repeats '2' 5 times.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either RED or BLUE. If he draws a BLUE ball, he repeats '2' 5 times. If he draws a RED ball, he says 5 random numbers between 3 and 9.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either RED or BLUE. If he draws a RED ball, he repeats '2' 5 times. If he draws a BLUE ball, he says 5 random numbers between 3 and 9.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either RED or BLUE. If he draws a RED ball, he says 5 random numbers between 3 and 9. If he draws a BLUE ball, he repeats '2' 5 times.\n\nBob: Here I go. I drew a",


"Bob is playing a game. He will draw one ball from an urn, then stop. The ball will be either RED or BLUE. If he draws a BLUE ball, he says 5 random numbers between 3 and 9. If he draws a RED ball, he repeats '2' 5 times.\n\nBob: Here I go. I drew a",
]

assert(len(prompts)==8)
assert(len(set(prompts))==len(prompts))
size = "7B"
#quantization_config = BitsAndBytesConfig(load_in_8bit=True)
#tokenizer = LlamaTokenizer.from_pretrained(f"./{size}")
#tokenizer.add_special_tokens({"pad_token":"<pad>"})
#model = LlamaForCausalLM.from_pretrained(f"./{size}", device_map = "cuda")#quantization_config=quantization_config, device_map = "auto")
#tokenizer.pad_token = tokenizer.eos_token
#model.config.pad_token_id = tokenizer.eos_token_id

for j, prompt in enumerate(prompts):
    #inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # Generate
    
    results = {"responses": [], "picked blue?" : [], "numbers" : []}
    num_samples = 3
    prompt_len = len(prompt)
    
    
    curr_time = time.time()
    do_sample = True
    for i in range(num_samples):
        outs = "".join(replicate.run(
                "meta/llama-2-7b:527827021d8756c7ab79fde0abbfaac885c37a3ed5fe23c7465093f0878d55ef",
                input={"prompt": prompt,
                    "max_new_tokens": 15,
                    "temperature" : 0.5,
                    "top_p": 1,
                }))
#        generate_ids = model.generate(
#                inputs.input_ids, 
#                max_length = 110, 
#                do_sample=do_sample,
#                temperature = 0.5,
#                top_k = 0)#, max_length=None)
#        outs = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0] 
#        outs = outs[prompt_len:]
        results["responses"].append(outs)
        results["picked blue?"].append("BLUE" in outs or "blue" in outs or "Blue" in outs)
        results["numbers"].append([int(i) for i in outs if i.isdigit()])
    
        display_threshold = 10
        if i % display_threshold == 0:
            time_elapsed = time.time() - curr_time
            print(f"Seconds elapsed for {display_threshold} inference steps: {time_elapsed}")
            curr_time = time.time()
            if i == display_threshold:
                estimated_total_time_sec = time_elapsed * (num_samples/display_threshold)
                print(f"Estimated total time in hours: {estimated_total_time_sec/3600}")
            curr_time = time.time()
            print(f"{results['responses'][-1]=}")
            print(f"{results['picked blue?'][-1]=}")
            print(f"{results['numbers'][-1]=}")
    
    file_name = f'{size}-experiment-results-prompt-{j}' 
    
    with open(file_name, 'wb') as f:
        pickle.dump({"prompt": prompt, "num_samples":num_samples, "results": results},  file = f)
