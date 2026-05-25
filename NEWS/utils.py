import datetime

def display_articles(response):
    if response['totalResults'] == 0:
        print("No articles found for selected options.")
        return
    else:
        for i,article in enumerate(response['articles'],start=1):
            print(f"{i}. {article['title']}")
            print(f"SOURCE: {article['source']['name']}")
            print(f"PUBLISHED AT: {article['publishedAt']}")
            print(f"URL: {article['url']}")

def save_to_file(response,file="output/saved_news.txt"):
    with open(file,"w+") as news:
        news.write(f"------- NEWS: {datetime.datetime.now()} -------\n")
        for article in response['articles']:
            news.write(f"{article['title']}\n")
            news.write(f"{article['url']}\n")
        print(f"News saved at {file}")
