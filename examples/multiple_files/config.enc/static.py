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


def walk(val, fn):
    # If we are looking at a dict, then traverse each of its branches
    if isinstance(val, dict):
        branch = val
        for key in branch:
            # Walk our value
            walk(branch[key], fn)

            # If we are changing our key, then update it
            new_key = fn(key)
            if new_key != key:
                branch[new_key] = branch[key]
                del branch[key]
    # Otherwise, if we are looking at a list, walk each of its items
    elif isinstance(val, list):
        arr = val
        for val in arr:
            walk(val, fn)


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
        walk(data, lambda key: key.rstrip('_unencrypted'))

        print(data)
