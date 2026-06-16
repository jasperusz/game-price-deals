import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("ITAD_API_KEY")

def search_game(game_name):
    max_tries = 3
    tries = 0
    while tries < max_tries:
        response = requests.get(
        "https://api.isthereanydeal.com/games/search/v1",
        params={
        "key": api_key,
        "title": game_name
            }
        )
        print(response.status_code)
        if response.status_code == 200:
            results = response.json()
            for i, result in enumerate(results, start=1):
                print(f'{i}: {result['title']} ({result['type']})')
        if response.status_code == 404:
            return {
                "error": "Game not found.",
                "status_code": response.status_code,
                "reason": response.reason
            }
        if response.status_code == 400:
            return {
                "error": "Bad request",
                "status_code": response.status_code,
                "reason": response.reason
            }
        tries += 1
        return {
            "error": "Failed after retries"
        }

game_name = input('Enter game name: ')
searchgame = search_game(game_name)
print(searchgame)