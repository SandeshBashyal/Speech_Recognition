import requests

url = 'http://192.168.11.107:4000/api'

data = {'Fan': False,
        'Light_bulb': False,
        'Door': False,
        'Led': False
        }

try:
    response = requests.post(url, json = data)
    
    if response.status_code == 200:
        print('POST request successful')

    else:
        print(f'POST request failed with with status code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')


