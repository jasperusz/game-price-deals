import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("ITAD_API_KEY")

response = requests.get(
    "https://api.isthereanydeal.com/v2/search/search/",
    params={
        "key": api_key,
        "title": "hollow-knight"
    }
)

print(response.status_code)
print(response.json())