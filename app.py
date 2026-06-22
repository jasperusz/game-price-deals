import os
from dotenv import load_dotenv
import requests
import json

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
        print(f'Status Code: {response.status_code}')

        # If the Search find results
        if response.status_code == 200:
            results = response.json()
            for i, result in enumerate(results, start=1):
                print(f"{i}: {result['title']} ({result['type']})")
            choice = int(input('Select the game from the list: '))
            user_selection = results[choice - 1]
            searched_game_name = user_selection['title']
            searched_game_id = user_selection['id']
            return {
                "name": searched_game_name,
                "id": searched_game_id
            }
            
        # If the search didn't find the game
        if response.status_code == 404:
            return {
                "error": "Game not found.",
                "status_code": response.status_code,
                "reason": response.reason
            }
        # If there's data validation error response
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

def game_info(game_id):
    response = requests.get("https://api.isthereanydeal.com/games/info/v2",
                            params={
                                "key": api_key,
                                "id": game_id
                                }
                            )
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        game_info = response.json()
        game_title = game_info["title"]
        tags = game_info["tags"]
        release_date = game_info["releaseDate"]
        publisher = game_info["publishers"][0]["name"]
        metascore = game_info["reviews"][1]["source"]
        metascore_score = game_info["reviews"][1]["score"]

        return game_title, tags, release_date, publisher, metascore, metascore_score
    else:
        return None
    
def get_deals(game_id):
    response = requests.post("https://api.isthereanydeal.com/games/prices/v3",
                            params={
                                "key": api_key,
                                "country": "BR",
                                "deals": True,
                                "vouchers": True
                                },
                                json=[
                                    game_id
                                    ]
                            )
    
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        prices_info = response.json()[0]
        history_low_price = prices_info["historyLow"]["all"]["amount"]
        deals = prices_info["deals"]
        formatted_deals = []
    
        for deal in deals:
            formatted_deal = {
                "shop": deal["shop"]["name"],
                "price": deal["price"]["amount"],
                "regular_price": deal["regular"]["amount"],
                "discount": deal["cut"],
                "voucher": deal["voucher"],
                "url": deal["url"]
            }
            formatted_deals.append(formatted_deal)
        return history_low_price, formatted_deals
    else:
        return None
    
if searchgame:
    result = game_info(searchgame["id"])
    if result:
        deals_info = get_deals(searchgame["id"])
        history_low_price, formatted_deals = deals_info
        game_title, tags, release_date, publisher, metascore, metascore_score= result
        print(f'Game Info:\nTitle: {game_title}\nTags:{tags}\nRelease Date: {release_date}\nPublisher: {publisher}\n{metascore} Score: {metascore_score}')
        print(f'History Low Price: R$ {history_low_price}\n')
        
        for deal in formatted_deals:
            print(f"Shop: {deal['shop']}\nPrice: R$ {deal['price']}\nRegular Price: R$ {deal['regular_price']}\n\
                  Discount: {deal['discount']}%\nVoucher: {deal['voucher']}\nURL: {deal['url']}\n")

