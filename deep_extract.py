#!/usr/bin/env python3
import json
import re
from pathlib import Path

artists = [
    "Zoe XGK", "Alla Vagner", "Gerry", "Mafi", "Tinker", "Animalien", "Aum Shanti",
    "El Mahico", "Mothership", "Tsune", "Game", "Pzychobiz", "Darkalien", "Goa Gummy",
    "Radzy", "Apnea", "Acid Echoes", "Shane Gobi", "Tetrameth", "E-Clip", "Boom Shankar",
    "Braincell", "Wingman (Purple Shapes)", "Phobos", "Psy Maiia", "Yogi", "Medicine",
    "Maiia", "Solar Spectrum", "Sabaii Sabaii", "1200 Mics by Chicago", "Lucas",
    "Ace Ventura", "Kala", "Janux", "Kia Goa", "Dark Elf", "John Lee", "Ton",
    "Mike Akida", "Xaphan", "Emiri", "Eartheogen", "Pspiralife", "Ryanosaurus",
    "Hatta", "Bensolo", "Drip Drop", "Giuseppe", "Farebi Jalebi", "Elowinz", "Gu",
    "Sun Anga", "Sandesh", "Daijiro", "Digoa", "Nitin", "Earthling", "Koxbox",
    "Tristan", "Fungus Funk", "Fungus Drop"
]

results_dir = Path("/Users/vadim/.claude/projects/-Users-vadim-Projects-sola-luna/4ecaa012-1bc0-4d8e-a29f-147dd6b05a85/tool-results")
result_files = sorted(results_dir.glob("mcp-brightdata-prod-search_engine_batch-*.txt"))

artist_soundcloud_map = {}
artist_index = 0

# Helper to clean artist name for matching
def normalize_name(name):
    # Remove special characters, convert to lowercase
    return re.sub(r'[^\w\s]', '', name.lower())

for result_file in result_files:
    print(f"\nProcessing: {result_file.name}")
    with open(result_file, 'r') as f:
        try:
            wrapper = json.load(f)

            for wrapper_item in wrapper:
                if artist_index >= len(artists):
                    break

                artist_name = artists[artist_index]
                normalized_artist = normalize_name(artist_name)

                if 'text' in wrapper_item:
                    search_results = json.loads(wrapper_item['text'])

                    for search_item in search_results:
                        if 'result' in search_item and 'organic' in search_item['result']:
                            organic_results = search_item['result']['organic']

                            print(f"\n{artist_name}:")
                            candidates = []

                            # Examine ALL organic results
                            for i, result in enumerate(organic_results[:5]):  # Look at top 5
                                if 'link' in result and 'soundcloud.com/' in result['link']:
                                    link = result['link']
                                    title = result.get('title', '')

                                    # Extract username from URL
                                    path = link.replace('https://soundcloud.com/', '').split('/')[0].split('?')[0]

                                    # Skip if it's a track (has more path segments)
                                    if '/' not in link.replace('https://soundcloud.com/', '').rstrip('/'):
                                        # Score this candidate based on title match
                                        score = 0
                                        if normalized_artist in normalize_name(title):
                                            score += 10
                                        if normalized_artist in normalize_name(path):
                                            score += 10

                                        candidates.append({
                                            'link': link,
                                            'title': title,
                                            'score': score,
                                            'rank': i
                                        })

                                        print(f"  [{i+1}] {link}")
                                        print(f"      Title: {title}")
                                        print(f"      Score: {score}")

                            # Pick the best candidate
                            if candidates:
                                best = max(candidates, key=lambda x: (x['score'], -x['rank']))
                                artist_soundcloud_map[artist_name] = best['link']
                                print(f"  ✓ Selected: {best['link']}")
                            else:
                                print(f"  ✗ No valid profile found")

                        break

                artist_index += 1

        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            continue

print(f"\n{'='*60}")
print(f"FOUND: {len([v for v in artist_soundcloud_map.values() if v])}/{len(artists)} artists")
print(f"{'='*60}")

# Save to file for inspection
output = Path("/Users/vadim/Projects/sola-luna/soundcloud_links.json")
with open(output, 'w') as f:
    json.dump(artist_soundcloud_map, f, indent=2)

print(f"\nSaved to: {output}")
