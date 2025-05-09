#pip install requests
import requests
import json

def get_useless_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)

    if response.status_code == 200:
        fact = response.json()["text"]
        print("Useless fact of the day:")
        print(fact)
    else:
        print("Error:", response.status_code)

get_useless_fact()