#!/usr/bin/env python3
import json
import csv
from pathlib import Path

# Artist list
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

for result_file in result_files:
    print(f"Processing: {result_file.name}")
    with open(result_file, 'r') as f:
        try:
            # Load the outer JSON structure
            wrapper = json.load(f)

            for wrapper_item in wrapper:
                if artist_index >= len(artists):
                    break

                artist_name = artists[artist_index]

                # The actual search results are in the "text" field as a JSON string
                if 'text' in wrapper_item:
                    search_results = json.loads(wrapper_item['text'])

                    # Process each search result
                    for search_item in search_results:
                        if 'result' in search_item and 'organic' in search_item['result']:
                            organic_results = search_item['result']['organic']

                            # Get the first SoundCloud profile link
                            for result in organic_results:
                                if 'link' in result and 'soundcloud.com/' in result['link']:
                                    link = result['link']

                                    # Skip links that are tracks (have more than 2 path segments)
                                    path = link.replace('https://soundcloud.com/', '').rstrip('/')
                                    segments = path.count('/')

                                    # Profile URLs typically have 0 slashes after the username
                                    if segments == 0:
                                        artist_soundcloud_map[artist_name] = link
                                        print(f"  {artist_name} -> {link}")
                                        break

                        # Move to next artist after processing their results
                        break

                artist_index += 1

        except Exception as e:
            print(f"  Error: {e}")
            continue

# Read CSV and add SoundCloud column
csv_file = Path("/Users/vadim/Projects/sola-luna/sola-luna-festival-timetable.csv")
rows = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)

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

print(f"\n✓ Updated CSV: {output_file}")
print(f"✓ Found SoundCloud links for {len([v for v in artist_soundcloud_map.values() if v])}/{len(artists)} artists")

# Display summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
missing_artists = [a for a in artists if a not in artist_soundcloud_map or not artist_soundcloud_map[a]]
if missing_artists:
    print(f"\nMissing links for {len(missing_artists)} artists:")
    for artist in missing_artists[:10]:  # Show first 10
        print(f"  - {artist}")
    if len(missing_artists) > 10:
        print(f"  ... and {len(missing_artists) - 10} more")
