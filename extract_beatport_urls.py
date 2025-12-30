import json
import sys
import re

# Read the file
with open(sys.argv[1], 'r') as f:
    data = json.load(f)

# The data is wrapped in a structure with "text" field
if isinstance(data, list) and len(data) > 0 and 'text' in data[0]:
    # Parse the nested JSON string
    inner_data = json.loads(data[0]['text'])
else:
    inner_data = data

results = {}

for item in inner_data:
    if 'result' in item and 'organic' in item['result']:
        query = item.get('query', '')
        # Extract artist name from query (remove the search terms)
        artist = re.sub(r'\s+(beatport|psytrance)\s+artist\s+profile.*', '', query, flags=re.IGNORECASE).strip()
        
        # Look for beatport.com URLs
        for result in item['result']['organic']:
            link = result.get('link', '')
            if 'beatport.com/artist/' in link:
                # Extract the base artist URL (remove query params and paths after ID)
                match = re.match(r'(https://www\.beatport\.com/artist/[^/]+/\d+)', link)
                if match:
                    clean_url = match.group(1)
                    results[artist] = clean_url
                    break

# Print results
print(f"Found {len(results)} Beatport artist URLs:\n")
for artist, url in sorted(results.items()):
    print(f'    "{artist}": "{url}",')
