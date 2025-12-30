#!/usr/bin/env python3
import json
import csv
from pathlib import Path
import re

# Artist list from the CSV (excluding non-artists)
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

# Directory with search results
results_dir = Path("/Users/vadim/.claude/projects/-Users-vadim-Projects-sola-luna/4ecaa012-1bc0-4d8e-a29f-147dd6b05a85/tool-results")

# Read all search result files
result_files = sorted(results_dir.glob("mcp-brightdata-prod-search_engine_batch-*.txt"))

# Map to store artist -> SoundCloud URL
artist_soundcloud_map = {}
artist_index = 0

for result_file in result_files:
    print(f"Processing: {result_file.name}")
    with open(result_file, 'r') as f:
        try:
            data = json.load(f)
            for item in data:
                if artist_index >= len(artists):
                    break

                artist_name = artists[artist_index]

                # Check if this result has organic results
                if 'result' in item and 'organic' in item['result']:
                    organic_results = item['result']['organic']

                    # Look for the first soundcloud.com profile link
                    for result in organic_results:
                        if 'link' in result and 'soundcloud.com/' in result['link']:
                            link = result['link']
                            # Skip links with too many path segments (these are tracks, not profiles)
                            path_segments = link.replace('https://soundcloud.com/', '').count('/')

                            # Profile URLs typically have 0-1 slashes
                            if path_segments <= 1:
                                # Clean the URL
                                clean_link = re.sub(r'["\?].*$', '', link)
                                artist_soundcloud_map[artist_name] = clean_link
                                print(f"  Found: {artist_name} -> {clean_link}")
                                break

                artist_index += 1

        except json.JSONDecodeError as e:
            print(f"  Error reading {result_file.name}: {e}")
            continue

# Read the original CSV
csv_file = Path("/Users/vadim/Projects/sola-luna/sola-luna-festival-timetable.csv")
rows = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

# Add SoundCloud link column
new_fieldnames = list(fieldnames) + ['SoundCloud Link']

# Write updated CSV
output_file = Path("/Users/vadim/Projects/sola-luna/sola-luna-festival-timetable-updated.csv")
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()

    for row in rows:
        artist_name = row['Artist']
        soundcloud_link = artist_soundcloud_map.get(artist_name, '')
        row['SoundCloud Link'] = soundcloud_link
        writer.writerow(row)

print(f"\n✓ Updated CSV written to: {output_file}")
print(f"✓ Found SoundCloud links for {len([v for v in artist_soundcloud_map.values() if v])}/{len(artists)} artists")
