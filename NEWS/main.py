from news_fetcher import everything,top_headlines
from utils import display_articles,save_to_file
response = None


def paginate(fetch_what,**kwargs):
    page = 1
    page_size = 5

    while True:
        response = fetch_what(page=page,pageSize = page_size,**kwargs)

        display_articles(response)

        print("\nType n for next, p for previous, s to save and next and q to quit.")
        choice = input().lower()

        if choice == 'n':
            page += 1
        elif choice == 'p' and page > 1:
            page -= 1
        elif choice == 's':
            save_to_file(response)
            page += 1
        elif choice == 'q':
            break
        else:
            print("Invalid")


def main():
    print("WELCOME TO THE NEWS API")
    print("1. Top headlines.")
    print("2. Everything")
    choice = int(input("Enter choice[1/2]: "))
    global response
    if choice == 2:
        language = input("Enter language code (en, fr, de... or leave blank): ") or None
        q = input("Enter search keyword: ")
        from_date = input("From date (YYYY-MM-DD or leave blank): ") or None
        to_date = input("To date (YYYY-MM-DD or leave blank): ") or None
        sort_by = input("Sort by (relevancy, popularity, publishedAt): ") or "publishedAt"

        paginate(everything,q=q,from_date=from_date,to_date=to_date,sortBy=sort_by,language=language)

    elif choice == 1:
        q = input("Enter search keyword: ")
        category = input("Enter category (business, sports, tech... or leave blank): ") or None
        language = input("Enter language code (en, fr, de... or leave blank): ") or None
        country = input("Enter country code (us, in, gb... or leave blank): ") or None

        paginate(top_headlines,q=q, category=category, country=country, language=language)

    else:
        print("Invalid choice.")
        return

if __name__ == "__main__":
    main()
