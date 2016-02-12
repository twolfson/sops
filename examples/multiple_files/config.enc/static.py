# Load in our dependencies
import json

# Define our configuration
common = {
    'port': 8080,
}

development = {

}

test = {

}

production = {

}

config = {
    'common': common,
    'development': development,
    'test': test,
    'production': production,
}


def _walk(val, fn):
    # If we are looking at a dict, then traverse again
    if isinstance(val, dict):
        walk_dict(val, fn)
    # Otherwise, if we are looking at a list, walk it
    elif isinstance(val, list):
        walk_list(val, fn)


def walk_dict(branch, fn):
    """Helper to update branch keys"""
    # For each key in our branch
    for key in branch:
        # If we are changing our key, then update it
        new_key = fn(key)
        val = branch[key]
        if new_key != key:
            branch[new_key] = val
            del branch[key]

        # Walk our value
        _walk(val, fn)


def walk_list(arr, fn):
    """Helper to update branch keys"""
    # For each item in our list, walk it
    for val in arr:
        _walk(val, fn)


# Merge all of our static secrets onto our config
# For each of our secrets
secret_files = [
    'config/static_github.json',
    'config/static_port.json',
]
for secret in secret_files:
    with open(secret_files, 'r') as file:
        # Load and parse our JSON
        data = json.loads(file.read())

        # Strip off `_unencrypted` from all keys
        walk_dict(data, lambda key: key.rstrip('_unencrypted'))

        print(data)
