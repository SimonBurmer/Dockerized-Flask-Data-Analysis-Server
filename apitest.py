import requests

url = "https://deezerdevs-deezer.p.rapidapi.com/track/1109731"

headers = {
    'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
    'x-rapidapi-key': "352a48d27emshb0c138ffb28522bp1dcca2jsnbc57ea7489f0"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)


