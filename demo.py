import json
from functools import reduce
from CORE import convert

def format_sequence_generator():
    sequence = ['json', 'toml', 'yaml', 'html', 'yaml', 'toml', 'json']
    for fmt in sequence:
        yield fmt

def main():
    initial_structure = {
        "name": "Alice",
        "hobbies": ["reading", "climbing"],
        "address": {"city": "Taipei"}
    }
    
    initial_json_str = json.dumps(initial_structure)
    
    gen = format_sequence_generator()
    first_fmt = next(gen)
    
    remaining_formats = list(gen)
    
    format_pairs = list(zip([first_fmt] + remaining_formats[:-1], remaining_formats))
    
    final_json_str = reduce(
        lambda data, pair: convert(data, pair[0], pair[1]),
        format_pairs,
        initial_json_str
    )
    
    final_structure = json.loads(final_json_str)
    
    identity_validator = lambda obj1, obj2: obj1 == obj2
    
    assert identity_validator(initial_structure, final_structure), "System failure: round-trip object parity broken."
    print("Execution verification succeeded: cyclic transformation pipeline fully consistent.")

if __name__ == "__main__":
    main()