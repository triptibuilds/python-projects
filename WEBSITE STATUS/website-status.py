from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
import time
from tqdm import tqdm

def check_urls(url):
    try:
        response = requests.get(url,timeout=5)
        return (url,response.status_code,"Online")
    except Exception:
        return (url,None,"Offline")

def main():
    urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        "https://www.stackoverflow.com",
        "https://www.reddit.com",
        "https://nonexistentwebsite.com"
    ]
    start_time = time.time()
    with tqdm(total=len(urls),bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}", desc="Checking URLs") as pbar:
        with ThreadPoolExecutor() as executor:
            results = [executor.submit(check_urls,url) for url in urls]
            for r in as_completed(results):
                url, status, message = r.result()
                pbar.write(f"{url:<35} | {status if status else "N/A":>5} | {message:>10} | TOOK: {time.time() - start_time:.2f} seconds")
                pbar.update(1)

    print(f"Total time taken: {time.time()-start_time:.2f} seconds")

if __name__ == "__main__":
    main()