import os
import json
import requests
import csv

# Load configuration based on environment
if os.getenv("GITHUB_ACTIONS"):
    # Running in GitHub Actions
    config = {
        "API_KEY": os.getenv("GOOGLE_API_KEY"),
        "SEARCH_ENGINE_ID": os.getenv("GOOGLE_CSE_ID"),
    }
else:
    # Running locally, load from config.json
    with open("config.json", "r") as file:
        config = json.load(file)

API_KEY = config["API_KEY"]
SEARCH_ENGINE_ID = config["SEARCH_ENGINE_ID"]
KEYWORDS = ["Sri Lanka travel packages", "Maldives tour deals", "best travel agents Sri Lanka"]

# Limit the results to the first 20
NUM_RESULTS = 20

# Function to perform the Google search
def search_google(query):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": NUM_RESULTS,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Function to save results to a CSV
def save_to_csv(results, filename="google_rankings.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Title", "Link", "Snippet"])
        for result in results:
            writer.writerow([result["keyword"], result["title"], result["link"], result["snippet"]])

# Main script execution
if __name__ == "__main__":
    all_results = []
    for keyword in KEYWORDS:
        print(f"Searching for keyword: {keyword}")
        search_results = search_google(keyword)
        for item in search_results.get("items", []):
            all_results.append({
                "keyword": keyword,
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet", ""),
            })
    save_to_csv(all_results)
    print(f"Results saved to google_rankings.csv")
