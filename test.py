
import requests

# Define the URL endpoint to send the POST request to
url = 'http://10.2.0.2:5000/api/upload/files'

# Define the data to be sent in the request body
data = {
    'skill': ['java','python',],

}

# Send the POST request with the data
response = requests.post(url, data=data)

# Check the response status code
if response.status_code == 200:
    print('POST request sent successfully.')
else:
    print('Failed to send POST request.')
