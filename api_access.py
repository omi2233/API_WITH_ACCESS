import requests

API_BASE_URL = 'https://api-web-t4f3.onrender.com'  # Replace with the actual API base URL

def search(query, api_key):
    url = f'{API_BASE_URL}/search'
    params = {
        'query': query,
        'api_key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Example usage
api_key = 'your_api_key_1'  # Replace with your actual API key
def main(query1):
    result = search(query1, api_key)
    print(result)

if __name__=='__main__':
    while True:
        query = input("Enter search query: ")
        if query.lower == "exit" or query.lower == "quit":
            break
        else:
            main(query)
    
