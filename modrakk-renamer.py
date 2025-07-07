#!/usr/bin/env python3
"""
Renames monster token files by appending monster names to filenames.
Expects files named like: 045_DDMD_G_150.png
Renames to: 045_DDMD_G_150_Eldritch-Cataclysm.png
written with the help of Anthropic's Claude
"""

"""
To use this, place the file in the same folder that all your MoD tokens
are in; then run it with `python modrakk-renamer.py`
Thanks to Chris on the MoD Discord Server for making this https://docs.google.com/document/d/1d2DHVoa93HqaWBtUm51uZSB-hEYBXfXc6YTM7TDRnZM/edit?tab=t.0
"""

import os
import re
from pathlib import Path

# Monster lookup table
MONSTERS = {
    1: "Hazewing Moth Caterpillar",
    2: "Loathsome Gag Fly",
    3: "Undulating Polyp",
    4: "Arcane Wraith",
    5: "Belfray",
    6: "Bloated Hive",
    7: "Gag Fly Swarm",
    8: "Chitter",
    9: "Dark Growth",
    10: "Dark Growth Shambler",
    11: "Haze Husk",
    12: "Haze Wight",
    13: "Hazewing Moth Adult",
    14: "Hazewing Moth Chrysalis",
    15: "Hypnotic Eldritch Blossom",
    16: "Last Memory",
    17: "Lob Frog",
    18: "Reality Cyst",
    19: "Skin Crawler",
    20: "Skretch",
    21: "Warp Witch",
    22: "Beetle Knight",
    23: "Bojack",
    24: "Animated Delerium Sludge",
    25: "Entropic Flame",
    26: "Living Deep Haze",
    27: "Walking Delerium Geode",
    28: "Effulgent Cnidarian",
    29: "Gravekeeper",
    30: "Kronen",
    31: "Pyknic Maunder",
    32: "Shardmaul Manticore",
    33: "Anomollusk",
    34: "Big Linda",
    35: "Cacophonous Chimera",
    36: "Digipede",
    37: "Drakkenheim Sewer Gator",
    38: "Graffiti",
    39: "Chorus",
    40: "Octarine Tree",
    41: "Sewer Thing",
    42: "Amalgamation",
    43: "Bigger Linda",
    44: "Crater Wurm",
    45: "Eldritch Cataclysm",
    46: "Living City",
    47: "World Ender",
    48: "Delerium Dreg",
    49: "Bloated Dreg",
    50: "Chitinous Dreg",
    51: "Crystalline Dreg",
    52: "Displacer Dreg",
    53: "Eldritch Dreg",
    54: "Frenzied Dreg",
    55: "Gutwretch Dreg",
    56: "Lambent Dreg",
    57: "Lurking Dreg",
    58: "Spined Dreg",
    59: "Tentacled Dreg",
    60: "Lenore von Kessel",
    61: "Haze Regent Lenore von Kessel",
    62: "Pale Man",
    63: "Haze Hulk",
    64: "Cyclopean Hulk",
    65: "Gutbuster Hulk",
    66: "Hunter Hulk",
    67: "Juggernaut Hulk",
    68: "Protean Abomination",
    69: "Grotesque Gargantuan",
    70: "Ratling Warrior",
    71: "Ratling Guttersnipe",
    72: "Warlock of the Rat God",
    73: "Ratling Alchemist",
    74: "Ratling Pathogenist",
    75: "Oracle of the Rat God",
    76: "Ratling Burrow Warden",
    77: "Rat Prince",
    78: "Rat Crown Prince",
    79: "Giant Ratling",
    80: "Rat King",
    81: "Swarm of Ratlings",
    82: "Maw Vermin",
    83: "Garmyr Bloodhound",
    84: "Garmyr Thaumaturge",
    85: "Garmyr Warrior",
    86: "Garmyr Berserker",
    87: "Garmyr War Dog",
    88: "Lord of the Feast",
    89: "Deep Dreg Warrior",
    90: "Deep Siren",
    91: "Deep Knight",
    92: "Duchess",
    93: "Wall Gargoyle",
    94: "Tower Dragon",
    95: "Grasping Shadow",
    96: "Executioner",
    97: "Minazorond",
    98: "Hazewind Harpy Crone",
    99: "Hazewind Harpy Hunter",
    100: "Hazewind Harpy Valkyrie",
    101: "Crimson Countess",
    102: "Helpful Hand",
    103: "Speaking Skull",
    104: "Blood Leech",
    105: "Innocent Harvester",
    106: "Alienist",
    107: "Chemist",
    108: "Exorcist",
    109: "Mutagenist",
    110: "Pathogenist",
    111: "Dr Everett Freed Reanimator",
    112: "Disembodied Psyche",
    113: "Injector",
    114: "Plague Carrier",
    115: "Reautomata",
    116: "Scrap Reautomata",
    117: "Skinwing",
    118: "Aberrant Host",
    119: "Faerie Host",
    120: "Fiendish Host",
    121: "Uncontained Growth M",
    122: "Wretched Patient",
    123: "Apex",
    124: "Think Tank",
    125: "Body Snatcher",
    126: "Cerebrograft",
    127: "Chemystral",
    128: "Living Biohazard",
    129: "Ravenous Flora",
    130: "Reautomata Wrecker",
    131: "Ripper",
    132: "Stitcher",
    133: "Tanker",
    134: "Uncontained Growth L",
    135: "Uncontained Growth H",
    136: "Kingkiller Hydra",
    137: "Uncontained Growth G",
    138: "Crimson Knight",
    139: "Dark Confessor",
    140: "Druid of the Sanguine Rites",
    141: "Ghoul Priest",
    142: "Ghoul Lord",
    143: "Ravenous Ghoul",
    144: "Grim Custodian",
    145: "Hazeblood Vampire",
    146: "Night Blade",
    147: "Night Blade",
    148: "Skeleton Soldier",
    149: "Skeleton Archer",
    150: "Skeleton Mage",
    151: "Zealot of Morrigan",
    152: "Striga",
    153: "Crypt-Starved Vladimir von Drakken",
    154: "Reborn Vladimir von Drakken",
    155: "Ascendant Vladimir von Drakken",
    156: "Fungal Trolling",
    157: "Magma Troll",
    158: "Magma Troll",
    159: "Winter Troll",
    160: "Eldritch Troll",
    161: "Troll Hag",
    162: "Humongous Fungus Troll",
    163: "Oak Troll",
    164: "Allopine",
    165: "Agog",
    166: "Interloper",
    167: "Far Dweller Abductor",
    168: "Far Dweller",
    169: "Far Dweller Mastermind",
    170: "Liminal Herald",
    171: "Eldritch Crawler",
    172: "Phage",
    173: "Psychophant",
    174: "Warp Marauder",
    175: "Void Pirate Captain",
    176: "Void Pirate Herald",
    177: "Void Pirate Quartermaster",
    178: "Void Pirate Squib",
    179: "Entropic Watcher",
    180: "Lurker on the Threshold",
    181: "Delerium Dragon Wyrmling",
    182: "Young Delerium Dragon",
    183: "Adult Delerium Dragon",
    184: "Ancient Delerium Dragon",
    185: "Fractal Lepidoptera",
    186: "Star Warden",
    187: "Sentient Planetoid",
    188: "Whispered Promise",
    189: "Rat God",
    190: "Thing with the Writhing Tail",
    191: "Algorithm",
    192: "He Who Laughs Last",
    193: "Academy Apprentice",
    194: "Academy Mage",
    195: "Master Mage",
    196: "Academy Grandmaster",
    197: "Academy Outcast",
    198: "River",
    199: "Eldrick Runeweaver",
    200: "Pilgrim",
    201: "Zealot",
    202: "Missionary",
    203: "Sanctified Monk",
    204: "Sanctified Knight",
    205: "Sanctified Soul",
    206: "Nathaniel Flint",
    207: "Lucretia Mathias",
    208: "Congregation",
    209: "Hooded Lantern Trapper",
    210: "Hooded Lantern Apothecary",
    211: "Hooded Lantern Veteran",
    212: "Lieutenant Petra Lang",
    213: "Captain Ansom Lang",
    214: "Lord Commander Elias Drexel",
    215: "Hooded Lantern Scout",
    216: "Royal Assassin",
    217: "Eldritch Trickster",
    218: "Blackjack Mel",
    219: "Queen of Thieves",
    220: "Silver Order Squire",
    221: "Silver Order Recruit",
    222: "Silver Order Paladin",
    223: "Silver Order Cavalier",
    224: "Flamekeeper",
    225: "High Flamekeeper Ophelia Reed",
    226: "Knight-Captain Theodore Marshal"
}

def sanitize_monster_name(name):
    """Convert monster name to filesystem-safe format."""
    # Remove special characters and convert spaces to dashes
    sanitized = re.sub(r'[^\w\s-]', '', name)  # Remove special chars except spaces and dashes
    sanitized = re.sub(r'\s+', '-', sanitized.strip())  # Convert spaces to dashes
    return sanitized

def extract_monster_number(filename):
    """Extract the leading number from filename."""
    match = re.match(r'^(\d+)_', filename)
    return int(match.group(1)) if match else None

def main():
    current_dir = Path('.')
    renamed_count = 0
    skipped_files = []
    
    print("Monster Token Renamer")
    print("=" * 40)
    
    # Get all PNG files in current directory
    png_files = list(current_dir.glob('*.png'))
    
    if not png_files:
        print("No PNG files found in current directory.")
        return
    
    print(f"Found {len(png_files)} PNG files")
    print()
    
    for file_path in png_files:
        filename = file_path.name
        
        # Extract monster number
        monster_num = extract_monster_number(filename)
        
        if monster_num is None:
            skipped_files.append(f"{filename} - doesn't match expected pattern")
            continue
            
        if monster_num not in MONSTERS:
            skipped_files.append(f"{filename} - monster #{monster_num} not found in database")
            continue
        
        # Get monster name and sanitize it
        monster_name = MONSTERS[monster_num]
        safe_name = sanitize_monster_name(monster_name)
        
        # Build new filename
        name_without_ext = file_path.stem
        extension = file_path.suffix
        new_filename = f"{name_without_ext}_{safe_name}{extension}"
        new_path = current_dir / new_filename
        
        # Check if target already exists
        if new_path.exists():
            skipped_files.append(f"{filename} - target filename already exists: {new_filename}")
            continue
        
        # Rename the file
        try:
            file_path.rename(new_path)
            print(f"✓ {filename} → {new_filename}")
            renamed_count += 1
        except OSError as e:
            skipped_files.append(f"{filename} - error renaming: {e}")
    
    print()
    print(f"Renamed {renamed_count} files successfully")
    
    if skipped_files:
        print(f"\nSkipped {len(skipped_files)} files:")
        for skip_msg in skipped_files:
            print(f"  • {skip_msg}")

if __name__ == "__main__":
    main()