import secrets
import string


def generate_api_key(length=32):
    """
    Generate a random API key of the specified length.
    The key will consist of uppercase letters, lowercase letters, and digits.
    """
    characters = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    return api_key


def generate_api_keys(num_keys, key_length):
    """
    Generate the specified number of API keys of the specified length.
    """
    api_keys = []
    for _ in range(num_keys):
        api_key = generate_api_key(key_length)
        api_keys.append(api_key)
    return api_keys

# Example usage:
num_keys = 45
key_length = 32
keys = generate_api_keys(num_keys, key_length)
a = 0
for key in keys:
    a += 1
    with open('api_keys2.txt', 'a') as f:
        f.write(f'"{key}" , ')
        print (f'{a}.{key}\n')
        
