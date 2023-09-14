from typing import Tuple
import itertools

def get_prompts(self):
    possible_prefixes = (('A.', 'B.'), ('BLUE', 'RED'), ('1', '2'))
    # prefix order in list, prefix order in prompt, instruction_order
    parameters = itertools.product(possible_prefixes, 
                                   self.repetitions_range, 
                                   (False, True), 
                                   (False, True), 
                                   (False, True), 
                                )
    for (prefixes, 
         repetitions, 
         list_prefixes_reversed,
         instruction_prefixes_reversed, 
         instructions_reversed) in parameters:

        list_prefixes = reversed(prefixes) if list_prefixes_reversed else prefixes 
        list_prefixes = reversed(prefixes) if instruction_prefixes_reversed else prefixes
        instructions = (f"he says '{self.predictable_response}' {repetitions} times",
                        f"he says {repetitions} random {self.category}")
        list_prefixes = reversed(instructions) if instructions_reversed else instructions
        yield (
            "Bob is playing a game. He will say one of the following options with equal probability:\n"
            f"- {list_prefixes[0]}\n"#type: ignore
            f"- {list_prefixes[1]}\n"#type: ignore
            f"If he says {instruction_prefixes[0]}, {instructions[0]}."#type: ignore
            f"If he says {instruction_prefixes[1]}, {instructions[1]}.\n\n"#type: ignore
            "Bob: Here I go: "
        )
