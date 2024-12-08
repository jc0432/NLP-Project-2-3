from Test import scrape_and_save
from Steps import parse_and_save

if __name__ == "__main__":
    print("Please provide a URL to the recipe:")
    url = input("> ").strip()
    scrape_and_save(url)
    parse_and_save()