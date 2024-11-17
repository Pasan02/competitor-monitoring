import os
import json
import requests
import csv

# Detect environment
is_github = os.getenv("GITHUB_ACTIONS") == "true"

if not is_github:
    # Dynamically calculate the absolute path to config.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config/config.json")
    with open(config_path, "r") as file:
        config = json.load(file)
    API_KEY = config["API_KEY"]
    SEARCH_ENGINE_ID = config["SEARCH_ENGINE_ID"]
else:
    # Use environment variables when running on GitHub Actions
    API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")

# Define keywords to track
keywords = [
    "Sri Lanka holiday packages",
    "Maldives travel packages",
    "affordable Sri Lanka tours",
    "luxury travel Maldives",
    "Sri Lanka travel deals",
]

def fetch_search_results(api_key, search_engine_id, query, num_results=20):
    """Fetch search results from the Google Custom Search JSON API."""
    search_results = []
    start = 1
    while len(search_results) < num_results:
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={api_key}&cx={search_engine_id}&q={query}&start={start}"
        )
        response = requests.get(url)
        data = response.json()
        if "items" not in data:
            break
        search_results.extend(data["items"])
        start += 10
        if len(data["items"]) < 10:
            break
    return search_results[:num_results]


def save_results_to_csv(all_results, filename="google_rankings_combined.csv"):
    """Save all search results for all keywords to a single CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Rank", "Title", "Snippet", "Link"])
        for keyword, results in all_results.items():
            for index, item in enumerate(results, start=1):
                writer.writerow([keyword, index, item["title"], item["snippet"], item["link"]])

# Fetch and save search results
all_results = {}
for keyword in keywords:
    print(f"Fetching results for: {keyword}")
    results = fetch_search_results(API_KEY, SEARCH_ENGINE_ID, keyword)
    all_results[keyword] = results

save_results_to_csv(all_results)

print("All search results saved to a single CSV file.")
