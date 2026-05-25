import requests
import json

def load_config():
    with open("config.json") as file:
        return json.load(file)

def everything(q=None, from_date=None, to_date=None, language=None, sortBy="publishedAt",page=1,pageSize=5):
    config = load_config()
    url = "https://newsapi.org/v2/everything"
    param = {
        "apiKey": config["apiKey"],
        "q":q,
        "language":language or config['default_language'],
        "from":from_date,
        "to":to_date,
        "sortBy":sortBy,
        "page":page,
        "pageSize":pageSize
    }
    response = requests.get(url,params = param)
    return response.json()

def top_headlines(q=None, category=None, country=None, language=None,page=1,pageSize=5):
    config = load_config()
    url = "https://newsapi.org/v2/top-headlines"
    param = {
        "apiKey": config["apiKey"],
        "q":q,
        "language":language or config['default_language'],
        "category":category or config['default_category'],
        "country":country or config['default_country'],
        "page":page,
        "pageSize":pageSize
    }
    response = requests.get(url,params = param)
    return response.json()