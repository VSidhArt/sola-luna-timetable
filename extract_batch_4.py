#!/usr/bin/env python3
import json
import re
from pathlib import Path

artists_batch = [
    "John Lee", "Ton", "Mike Akida", "Xaphan", "Emiri",
    "Eartheogen", "Pspiralife", "Ryanosaurus", "Hatta", "Bensolo"
]

result_file = Path("/Users/vadim/.claude/projects/-Users-vadim-Projects-sola-luna/4ecaa012-1bc0-4d8e-a29f-147dd6b05a85/tool-results/mcp-brightdata-prod-search_engine_batch-1767035824049.txt")

with open(result_file, 'r') as f:
    wrapper = json.load(f)

artist_soundcloud_map = {}

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

            for i, result in enumerate(organic_results[:5]):
                if 'link' in result and 'soundcloud.com/' in result['link']:
                    link = result['link']
                    title = result.get('title', '')

                    clean_link = re.sub(r'[\\?#].*$', '', link)
                    path = clean_link.replace('https://soundcloud.com/', '').replace('http://soundcloud.com/', '')

                    if '/' not in path.rstrip('/'):
                        print(f"  [{i+1}] {clean_link}")
                        print(f"      Title: {title}")
                        candidates.append({
                            'link': clean_link,
                            'title': title,
                            'rank': i
                        })

            if candidates:
                best = candidates[0]
                artist_soundcloud_map[artist_name] = best['link']
                print(f"  ✓ Selected: {best['link']}")
            else:
                print(f"  ✗ No valid profile found")

print(f"\n{'='*60}")
print(f"FOUND: {len(artist_soundcloud_map)}/{len(artists_batch)} artists")
print(f"{'='*60}")

for artist, link in artist_soundcloud_map.items():
    print(f"{artist}: {link}")
