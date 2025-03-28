import requests

try:
    # Make a GET request with a timeout of 5 seconds
    response = requests.get('https://reddit.com', timeout=5)
    # If the request is successful, print the response
    print(response.text)
except requests.exceptions.Timeout:
    # This block will execute if the request times out
    print("The request timed out. Please try again later.")
except requests.exceptions.RequestException as e:
    # Catch any other exceptions (e.g., network errors, invalid URLs)
    print(f"An error occurred: {e}")
