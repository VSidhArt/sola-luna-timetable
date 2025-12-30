#!/usr/bin/env python3
import json
import re
import csv
from pathlib import Path

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

# Extract SoundCloud profile URLs
artist_soundcloud_map = {}

for result_file in result_files:
    with open(result_file, 'r') as f:
        content = f.read()
        # Find all SoundCloud URLs
        soundcloud_urls = re.findall(r'https://soundcloud\.com/[^/"]+(?=/|")', content)

        # Store unique profile URLs (not track URLs)
        for url in soundcloud_urls:
            # Skip URLs that are clearly tracks (contain multiple path segments)
            if url.count('/') == 3:  # Base profile URL format
                continue

# Now let's parse the JSON data to match artists with their search results
artist_index = 0
for result_file in result_files:
    with open(result_file, 'r') as f:
        try:
            data = json.load(f)
            for item in data:
                if artist_index < len(artists):
                    artist = artists[artist_index]

                    # Extract SoundCloud URLs from the text
                    text = item.get('text', '')
                    urls = re.findall(r'https://soundcloud\.com/([^/"?#]+)', text)

                    if urls:
                        # Prioritize artist profile URLs (shorter, without sub-paths)
                        # Get the first unique profile URL
                        seen_profiles = set()
                        for url_path in urls:
                            if url_path not in seen_profiles:
                                full_url = f"https://soundcloud.com/{url_path}"
                                # Prefer main profile URLs
                                if artist not in artist_soundcloud_map:
                                    artist_soundcloud_map[artist] = full_url
                                    break
                                seen_profiles.add(url_path)

                    artist_index += 1
        except json.JSONDecodeError:
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

print(f"Updated CSV written to: {output_file}")
print(f"\nFound SoundCloud links for {len([v for v in artist_soundcloud_map.values() if v])} artists")
print("\nArtist -> SoundCloud mapping:")
for artist, url in sorted(artist_soundcloud_map.items()):
    if url:
        print(f"  {artist}: {url}")
