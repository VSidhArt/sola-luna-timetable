#!/usr/bin/env python3
import csv
from pathlib import Path

# All found SoundCloud links
soundcloud_links = {
    # From BrightData batch 1
    "Zoe XGK": "https://soundcloud.com/djane-zoexgk",
    "Gerry": "https://soundcloud.com/boomshankar-bmssrecords",
    "Mafi": "https://soundcloud.com/1200-micrograms",
    "Tinker": "https://soundcloud.com/x4ph4n",
    "Animalien": "https://soundcloud.com/elowinzmusic",
    "Aum Shanti": "https://soundcloud.com/fungus-funk",

    # From Firecrawl searches
    "Alla Vagner": "https://soundcloud.com/maiia",
    "E-Clip": "https://soundcloud.com/e-clip",
    "Tristan": "https://soundcloud.com/djtristan",
    "Tsune": "https://soundcloud.com/tsunelive",
    "Ace Ventura": "https://soundcloud.com/schatsi",
    "El Mahico": "https://soundcloud.com/dj-el-mahico",
    "Pzychobiz": "https://soundcloud.com/pzychobiz",
    "Darkalien": "https://soundcloud.com/ksamail",
    "Goa Gummy": "https://soundcloud.com/goagummy",
    "Mothership": "https://soundcloud.com/masuke-mothership",

    # From BrightData batch 2
    "Radzy": "https://soundcloud.com/yzdar",
    "Apnea": "https://soundcloud.com/apnea",
    "Acid Echoes": "https://soundcloud.com/acidechoes",
    "Shane Gobi": "https://soundcloud.com/shane-gobi",
    "Boom Shankar": "https://soundcloud.com/boomshankar-bmssrecords",
    "Braincell": "https://soundcloud.com/brainalien",
    "Wingman (Purple Shapes)": "https://soundcloud.com/purpleshapes",
    "Phobos": "https://soundcloud.com/phobos_looney",
    "Psy Maiia": "https://soundcloud.com/psymaiia",
    "Yogi": "https://soundcloud.com/yogitrf",

    # From BrightData batch 3
    "Maiia": "https://soundcloud.com/psymaiia",
    "Solar Spectrum": "https://soundcloud.com/solar-spectrum",
    "1200 Mics by Chicago": "https://soundcloud.com/1200-micrograms",
    "Lucas": "https://soundcloud.com/djlucasobrien",
    "Kala": "https://soundcloud.com/kala",
    "Janux": "https://soundcloud.com/januxjanux",
    "Kia Goa": "https://soundcloud.com/dj-kia-goa",
    "Dark Elf": "https://soundcloud.com/darkelfmusic",

    # From BrightData batch 4
    "John Lee": "https://soundcloud.com/john-lee-lost-project",
    "Xaphan": "https://soundcloud.com/x4ph4n",
    "Emiri": "https://soundcloud.com/emiri-tsukui",
    "Eartheogen": "https://soundcloud.com/eartheogen",
    "Pspiralife": "https://soundcloud.com/pspiralife",
    "Ryanosaurus": "https://soundcloud.com/ryanosaurusmusic",
    "Hatta": "https://soundcloud.com/dj-hatta",
    "Bensolo": "https://soundcloud.com/bensolopsy",

    # From BrightData batch 5
    "Drip Drop": "https://soundcloud.com/drip_drop",
    "Giuseppe": "https://soundcloud.com/GIUSEPPEOTTAVIANI",
    "Farebi Jalebi": "https://soundcloud.com/farebi-jalebi",
    "Elowinz": "https://soundcloud.com/elowinzmusic",
    "Gu": "https://soundcloud.com/gu-jp",
    "Sun Anga": "https://soundcloud.com/sunanga",
    "Sandesh": "https://soundcloud.com/sandeshpoin",
    "Daijiro": "https://soundcloud.com/dj-daijiro",
    "Nitin": "https://soundcloud.com/djnitinhilltopgoa",

    # From BrightData batch 6
    "Earthling": "https://soundcloud.com/earthling",
    "Koxbox": "https://soundcloud.com/koxboxmusic",
    "Fungus Funk": "https://soundcloud.com/fungus-funk",
    "Tetrameth": "https://soundcloud.com/tetrameth",
    "Medicine": "https://soundcloud.com/aya-bara",
    "Ton": "https://soundcloud.com/dj-x-ton",

    # From BrightData batch 7 (final search)
    "Digoa": "https://soundcloud.com/dj-digoa",
    "Fungus Drop": "https://soundcloud.com/fungi_psy95",
}

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
        soundcloud_link = soundcloud_links.get(artist_name, '')
        row['SoundCloud Link'] = soundcloud_link
        writer.writerow(row)

# Get list of artists from CSV
all_artists = set(row['Artist'] for row in rows if row['Artist'] not in ['Break', 'Opening Ceremony', 'End'])
found_artists = set(soundcloud_links.keys())
missing_artists = sorted(all_artists - found_artists)

print(f"✓ Updated CSV: {output_file}")
print(f"✓ Found SoundCloud links for {len(soundcloud_links)}/{len(all_artists)} artists ({len(soundcloud_links)*100//len(all_artists)}%)")

if missing_artists:
    print(f"\nMissing links for {len(missing_artists)} artists:")
    for artist in missing_artists:
        print(f"  - {artist}")
