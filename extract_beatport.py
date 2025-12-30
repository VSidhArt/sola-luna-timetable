import json
import sys
import re

# Read the file
with open(sys.argv[1], 'r') as f:
    data = json.load(f)

results = {}

for item in data:
    if 'result' in item and 'organic' in item['result']:
        query = item.get('query', '')
        # Extract artist name from query
        artist = query.replace(' beatport artist profile', '').replace(' psytrance beatport artist profile', '').strip()
        
        # Look for beatport.com URLs
        for result in item['result']['organic']:
            link = result.get('link', '')
            if 'beatport.com/artist/' in link:
                # Clean the URL
                clean_url = link.split('?')[0]  # Remove query params
                results[artist] = clean_url
                break

# Print results
for artist, url in results.items():
    print(f'    "{artist}": "{url}",')

print(f"\nFound {len(results)} Beatport artist URLs")
