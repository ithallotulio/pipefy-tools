import pipefy_api as pipe

response = pipe.me()

if response.status_code == 200:
    print("API communication was successful!\n"
          f"API Response: {response.text}")
else:
    print("There was an error communicating with the API.\n"
          f"Response status code: {response.status_code}\n"
          f"Details: {response.text}")