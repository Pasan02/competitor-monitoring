import requests
import csv
import time

# API key and Search Engine ID
API_KEY = "AIzaSyDGZROiIUs0x7CaDmihgcI7R9NyTmL0aMw"
SEARCH_ENGINE_ID = "e7544dfd2df7748cd"

def fetch_google_results(keyword, max_results=20):
    url = f"https://www.googleapis.com/customsearch/v1"
    results = []
    start_index = 1  # Start with the first result
    
    while len(results) < max_results:
        # Fetch up to 10 results per API call
        params = {
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'q': keyword,
            'start': start_index,
            'num': min(10, max_results - len(results))  # Limit to remaining results
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract data
            for item in data.get('items', []):
                title = item.get('title', 'No title')
                link = item.get('link', 'No link')
                snippet = item.get('snippet', 'No snippet')
                results.append({'title': title, 'link': link, 'snippet': snippet})
            
            # Increment start index for next batch
            start_index += 10
            
            # Break if no more results are returned
            if 'items' not in data:
                break
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching results for {keyword}: {e}")
            break
    
    return results

# List of keywords to track
keywords = [
    "Sri Lanka holiday packages",
    "Maldives honeymoon packages",
    "Best luxury travel in Sri Lanka",
    "Affordable Sri Lanka tours",
    "Thailand tours from Sri Lanka"
]

# Save results to a CSV file
def save_to_csv(results, filename='google_rankings.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Keyword', 'Rank', 'Title', 'Link', 'Snippet'])
        for keyword, keyword_results in results.items():
            for rank, result in enumerate(keyword_results, start=1):
                writer.writerow([keyword, rank, result['title'], result['link'], result['snippet']])

# Main execution
all_results = {}
for keyword in keywords:
    print(f"Fetching results for: {keyword}")
    all_results[keyword] = fetch_google_results(keyword)
    time.sleep(2)  # Delay to prevent exceeding rate limits

save_to_csv(all_results)
print("Results saved to google_rankings.csv")
