#!/usr/bin/env python3
import json
import re
from pathlib import Path

# Artists in this batch
artists_batch = [
    "Radzy", "Apnea", "Acid Echoes", "Shane Gobi", "Boom Shankar",
    "Braincell", "Wingman (Purple Shapes)", "Phobos", "Psy Maiia", "Yogi"
]

result_file = Path("/Users/vadim/.claude/projects/-Users-vadim-Projects-sola-luna/4ecaa012-1bc0-4d8e-a29f-147dd6b05a85/tool-results/mcp-brightdata-prod-search_engine_batch-1767035586136.txt")

with open(result_file, 'r') as f:
    wrapper = json.load(f)

artist_soundcloud_map = {}

# The structure is: [{type: "text", text: "[{search results}]"}]
if wrapper and 'text' in wrapper[0]:
    search_results = json.loads(wrapper[0]['text'])

    for artist_index, search_item in enumerate(search_results):
        if artist_index >= len(artists_batch):
            break

        artist_name = artists_batch[artist_index]

        if 'result' in search_item and 'organic' in search_item['result']:
            organic_results = search_item['result']['organic']

            print(f"\n{artist_name}:")
            candidates = []

            # Look at top 5 results
            for i, result in enumerate(organic_results[:5]):
                if 'link' in result and 'soundcloud.com/' in result['link']:
                    link = result['link']
                    title = result.get('title', '')

                    # Clean URL and extract path
                    clean_link = re.sub(r'[\\?#].*$', '', link)
                    path = clean_link.replace('https://soundcloud.com/', '').replace('http://soundcloud.com/', '')

                    # Skip if it's a track (has slashes after username)
                    if '/' not in path.rstrip('/'):
                        print(f"  [{i+1}] {clean_link}")
                        print(f"      Title: {title}")
                        candidates.append({
                            'link': clean_link,
                            'title': title,
                            'rank': i
                        })

            # Pick the first valid candidate
            if candidates:
                best = candidates[0]
                artist_soundcloud_map[artist_name] = best['link']
                print(f"  ✓ Selected: {best['link']}")
            else:
                print(f"  ✗ No valid profile found")

print(f"\n{'='*60}")
print(f"FOUND: {len(artist_soundcloud_map)}/{len(artists_batch)} artists")
print(f"{'='*60}")

# Print results
for artist, link in artist_soundcloud_map.items():
    print(f"{artist}: {link}")
