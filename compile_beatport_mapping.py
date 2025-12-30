import json

beatport_links = {
    # Batch 1
    "Zoe XGK": "https://www.beatport.com/artist/ze-xgk/918565",
    "Gerry": "https://www.beatport.com/artist/psiger/972478",
    "Mafi": "https://www.beatport.com/artist/psy-trance-mafia/1263092",
    "Animalien": "https://www.beatport.com/artist/animalien/441805",
    "Aum Shanti": "https://www.beatport.com/artist/aum-shanti/760736",
    "El Mahico": "https://www.beatport.com/artist/el-mahico/860374",
    "Mothership": "https://www.beatport.com/artist/mothership-loudspeakerz/267563",
    "Tsune": "https://www.beatport.com/artist/ctune/942033",
    
    # Batch 2
    "Game": "https://www.beatport.com/artist/pulsar/17645",
    "Pzychobiz": "https://www.beatport.com/artist/penubiz/1011841",
    "Darkalien": "https://www.beatport.com/artist/darkalien-live/1129504",
    "Goa Gummy": "https://www.beatport.com/artist/gummy/301074",
    "Radzy": "https://www.beatport.com/artist/razzy/278307",
    "Apnea": "https://www.beatport.com/artist/apneia/1107621",
    "Shane Gobi": "https://www.beatport.com/artist/shane-gobi/135014",
    "Tetrameth": "https://www.beatport.com/artist/tetrameth/42337",
    "E-Clip": "https://www.beatport.com/artist/e-clip/119593",
    
    # Batch 3
    "Boom Shankar": "https://www.beatport.com/artist/boomshankar/381159",
    "Braincell": "https://www.beatport.com/artist/braincell/22727",
    "Wingman (Purple Shapes)": "https://www.beatport.com/artist/purple-shapes/763695",
    "Phobos": "https://www.beatport.com/artist/phobos/82441",
    "Psy Maiia": "https://www.beatport.com/artist/psy-maiia/1304249",
    "Yogi": "https://www.beatport.com/artist/yogi-p/784335",
    "Medicine": "https://www.beatport.com/artist/psytrance/283053",
    "Maiia": "https://www.beatport.com/artist/psy-maiia/1304249",
    "Solar Spectrum": "https://www.beatport.com/artist/solar-spectrum/136242",
    "Sabaii Sabaii": "https://www.beatport.com/artist/sabai/767561",
    
    # Batch 4
    "1200 Mics by Chicago": "https://www.beatport.com/artist/1200-micrograms/13377",
    "Lucas": "https://www.beatport.com/artist/lucas/4092",
    "Ace Ventura": "https://www.beatport.com/artist/ace-ventura/7165",
    "Kala": "https://www.beatport.com/artist/kala/116093",
    "Janux": "https://www.beatport.com/artist/janus-rasmussen/725832",
    "Kia Goa": "https://www.beatport.com/artist/kia/132704",
    "Dark Elf": "https://www.beatport.com/artist/dark-elf/64335",
    "John Lee": "https://www.beatport.com/artist/jon-lee/178431",
    "Ton": "https://www.beatport.com/artist/ton/1008345",
    "Mike Akida": "https://www.beatport.com/artist/makida/402547",
    
    # Batch 5
    "Xaphan": "https://www.beatport.com/artist/xaphan/68204",
    "Emiri": "https://www.beatport.com/artist/emyr/967045",
    "Eartheogen": "https://www.beatport.com/artist/eartheogen/505034",
    "Pspiralife": "https://www.beatport.com/artist/pspiralife/205881",
    "Ryanosaurus": "https://www.beatport.com/artist/ryanosaurus/324432",
    "Hatta": "https://www.beatport.com/artist/hatta/723553",
    "Bensolo": "https://www.beatport.com/artist/bensolo/515533",
    "Drip Drop": "https://www.beatport.com/artist/drip-drop/404703",
    "Giuseppe": "https://www.beatport.com/artist/giuseppe/121049",
    "Farebi Jalebi": "https://www.beatport.com/artist/farebi-jalebi/168766",
    
    # Batch 6
    "Elowinz": "https://www.beatport.com/artist/elowinz/398004",
    "Gu": "https://www.beatport.com/artist/gu/119521",
    "Sun Anga": "https://www.beatport.com/artist/sun-anga/711626",
    "Sandesh": "https://www.beatport.com/artist/sandesh/168404",
    "Daijiro": "https://www.beatport.com/artist/dairo/1172140",
    "Digoa": "https://www.beatport.com/artist/dj-digoa/1101728",
    "Nitin": "https://www.beatport.com/artist/nitin/71092",
    "Earthling": "https://www.beatport.com/artist/earthling/10534",
    "Koxbox": "https://www.beatport.com/artist/koxbox/19674",
    "Tristan": "https://www.beatport.com/artist/tristan/2932",
    
    # Batch 7
    "Fungus Funk": "https://www.beatport.com/artist/fungus-funk/17968",
    "Fungus Drop": "https://www.beatport.com/artist/fungus-funk/17968",
}

# Save to JSON
with open('beatport_mapping.json', 'w') as f:
    json.dump(beatport_links, f, indent=2)

print(f"Total artists with Beatport links: {len(beatport_links)}")
print(f"\nMapping saved to beatport_mapping.json")

# Identify missing artists
all_artists = ["Zoe XGK", "Alla Vagner", "Gerry", "Mafi", "Tinker", "Animalien", "Aum Shanti", "El Mahico", "Mothership", "Tsune", "Game", "Pzychobiz", "Darkalien", "Goa Gummy", "Radzy", "Apnea", "Acid Echoes", "Shane Gobi", "Tetrameth", "E-Clip", "Boom Shankar", "Braincell", "Wingman (Purple Shapes)", "Phobos", "Psy Maiia", "Yogi", "Medicine", "Maiia", "Solar Spectrum", "Sabaii Sabaii", "1200 Mics by Chicago", "Lucas", "Ace Ventura", "Kala", "Janux", "Kia Goa", "Dark Elf", "John Lee", "Ton", "Mike Akida", "Xaphan", "Emiri", "Eartheogen", "Pspiralife", "Ryanosaurus", "Hatta", "Bensolo", "Drip Drop", "Giuseppe", "Farebi Jalebi", "Elowinz", "Gu", "Sun Anga", "Sandesh", "Daijiro", "Digoa", "Nitin", "Earthling", "Koxbox", "Tristan", "Fungus Funk", "Fungus Drop"]

missing = [artist for artist in all_artists if artist not in beatport_links]

print(f"\nMissing artists ({len(missing)}):")
for artist in missing:
    print(f"  - {artist}")
