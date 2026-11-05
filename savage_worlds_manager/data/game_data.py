"""
Static data for Savage Worlds edges, hindrances, and other game elements.
"""

from typing import List, Dict
from ..models.character import Edge, Hindrance
from ..models.equipment import Weapon, Armor, Equipment, WeaponType, ArmorType


# Common Edges
COMMON_EDGES: List[Edge] = [
    Edge(
        name="Alertness",
        description="+2 Notice rolls",
        requirements=["Novice"]
    ),
    Edge(
        name="Ambidextrous", 
        description="Ignore -2 penalty for using off-hand",
        requirements=["Novice", "Agility d8+"]
    ),
    Edge(
        name="Arcane Background (Magic)",
        description="Allows use of magic with 10 Power Points and 3 spells",
        requirements=["Novice"]
    ),
    Edge(
        name="Attractive",
        description="+2 Charisma",
        requirements=["Novice", "Vigor d6+"]
    ),
    Edge(
        name="Very Attractive",
        description="+4 Charisma",
        requirements=["Novice", "Attractive"]
    ),
    Edge(
        name="Berserk",
        description="Go berserk when Shaken or wounded",
        requirements=["Novice"]
    ),
    Edge(
        name="Block", 
        description="+1 Parry, +2 when using defend maneuver",
        requirements=["Seasoned", "Fighting d8+"]
    ),
    Edge(
        name="Brave",
        description="+2 Guts and fear checks",
        requirements=["Novice", "Spirit d6+"]
    ),
    Edge(
        name="Charismatic",
        description="+2 Charisma",
        requirements=["Novice", "Spirit d8+"]
    ),
    Edge(
        name="Combat Reflexes",
        description="+2 recover from Shaken",
        requirements=["Seasoned"]
    ),
    Edge(
        name="Dodge",
        description="-1 to ranged attacks against you, -2 with raise on Agility",
        requirements=["Seasoned", "Agility d8+"]
    ),
    Edge(
        name="Fast Healer",
        description="+2 natural healing rolls",
        requirements=["Novice", "Vigor d8+"]
    ),
    Edge(
        name="First Strike",
        description="Attack first foe that moves adjacent",
        requirements=["Novice", "Agility d8+"]
    ),
    Edge(
        name="Fleet-Footed",
        description="+2 Pace, running die increases one step",
        requirements=["Novice", "Agility d6+"]
    ),
    Edge(
        name="Frenzy",
        description="Make 1 extra Fighting attack at -2",
        requirements=["Seasoned", "Fighting d8+"]
    ),
    Edge(
        name="Improved Frenzy",
        description="Make 1 extra Fighting attack with no penalty",
        requirements=["Veteran", "Frenzy"]
    ),
    Edge(
        name="Hard to Kill",
        description="Ignore wound penalties on Vigor rolls to avoid bleeding out",
        requirements=["Novice", "Spirit d8+"]
    ),
    Edge(
        name="Nerves of Steel",
        description="Ignore 1 point of wound penalties",
        requirements=["Novice", "Vigor d8+"]
    ),
    Edge(
        name="Improved Nerves of Steel",
        description="Ignore 2 points of wound penalties", 
        requirements=["Novice", "Nerves of Steel"]
    ),
    Edge(
        name="Quick",
        description="Discard cards of 5 or lower for new ones",
        requirements=["Novice", "Agility d8+"]
    ),
    Edge(
        name="Strong Willed",
        description="+2 rolls to resist Smarts or Spirit-based powers",
        requirements=["Novice", "Intimidation d6+", "Taunt d6+"]
    ),
    Edge(
        name="Sweep",
        description="Attack all adjacent foes at -2",
        requirements=["Novice", "Strength d8+", "Fighting d8+"]
    ),
    Edge(
        name="Tough as Nails",
        description="+1 Toughness",
        requirements=["Legendary"]
    ),
    Edge(
        name="Two-Fisted",
        description="Make 1 extra Fighting attack with off-hand at -2",
        requirements=["Novice", "Ambidextrous"]
    ),
    Edge(
        name="Woodsman",
        description="+2 Tracking, Survival, and Stealth in wilderness",
        requirements=["Novice", "Spirit d6+"]
    )
]

# Common Hindrances
COMMON_HINDRANCES: List[Hindrance] = [
    Hindrance(
        name="All Thumbs",
        description="-2 to use mechanical or electrical devices",
        severity="Minor"
    ),
    Hindrance(
        name="Anemic",
        description="-2 Vigor rolls to resist sickness, disease, poison, etc.",
        severity="Minor"
    ),
    Hindrance(
        name="Arrogant",
        description="Must humiliate and belittle opponents",
        severity="Major"
    ),
    Hindrance(
        name="Bad Eyes",
        description="-2 to any trait roll dependent on vision beyond 5 inches",
        severity="Minor"
    ),
    Hindrance(
        name="Blind",
        description="-6 to most physical tasks, -2 to social rolls",
        severity="Major"
    ),
    Hindrance(
        name="Bloodthirsty",
        description="Never takes prisoners, kills when able",
        severity="Major"
    ),
    Hindrance(
        name="Boastful",
        description="Likes to brag and doesn't like to be ignored",
        severity="Minor"
    ),
    Hindrance(
        name="Cautious",
        description="Character is overly careful",
        severity="Minor"
    ),
    Hindrance(
        name="Clueless",
        description="-2 to Common Knowledge rolls",
        severity="Minor"
    ),
    Hindrance(
        name="Code of Honor",
        description="Character keeps his word and acts like a gentleman",
        severity="Major"
    ),
    Hindrance(
        name="Curious",
        description="Character wants to know about everything",
        severity="Major"
    ),
    Hindrance(
        name="Death Wish",
        description="Character wants to die after completing some important goal",
        severity="Minor"
    ),
    Hindrance(
        name="Doubting Thomas",
        description="Character doesn't believe in the supernatural",
        severity="Minor"
    ),
    Hindrance(
        name="Elderly",
        description="-1 to Pace, Strength, and Vigor die types. +5 skill points.",
        severity="Major"
    ),
    Hindrance(
        name="Enemy",
        description="Character has a recurring nemesis",
        severity="Minor"
    ),
    Hindrance(
        name="Greedy",
        description="Character is obsessed with wealth and material possessions",
        severity="Minor"
    ),
    Hindrance(
        name="Habit",
        description="Character has an annoying or dangerous compulsion",
        severity="Minor"
    ),
    Hindrance(
        name="Hard of Hearing",
        description="-2 to Notice rolls involving hearing",
        severity="Minor"
    ),
    Hindrance(
        name="Heroic",
        description="Character always helps those in need",
        severity="Major"
    ),
    Hindrance(
        name="Illiterate",
        description="Character cannot read or write in any language",
        severity="Minor"
    ),
    Hindrance(
        name="Lame",
        description="-2 Pace and running die is d4",
        severity="Major"
    ),
    Hindrance(
        name="Loyal",
        description="Character will never betray or disappoint his friends",
        severity="Minor"
    ),
    Hindrance(
        name="Mean",
        description="-2 Charisma",
        severity="Minor"
    ),
    Hindrance(
        name="Overconfident",
        description="Character believes he can do anything",
        severity="Major"
    ),
    Hindrance(
        name="Pacifist",
        description="Character fights only in self-defense (Minor) or won't fight at all (Major)",
        severity="Minor"
    ),
    Hindrance(
        name="Phobia",
        description="-2 or -4 to trait rolls when near the phobia",
        severity="Minor"
    ),
    Hindrance(
        name="Poverty",
        description="Half starting money, problems caused by lack of funds",
        severity="Minor"
    ),
    Hindrance(
        name="Quirk",
        description="Character has some minor but persistent foible",
        severity="Minor"
    ),
    Hindrance(
        name="Slow",
        description="-1 Pace, running die is d4",
        severity="Major"
    ),
    Hindrance(
        name="Small",
        description="-1 Toughness",
        severity="Major"
    ),
    Hindrance(
        name="Stubborn",
        description="Character always wants his way",
        severity="Minor"
    ),
    Hindrance(
        name="Ugly",
        description="-2 Charisma",
        severity="Minor"
    ),
    Hindrance(
        name="Vengeful",
        description="Character seeks payback for slights against him",
        severity="Minor"
    ),
    Hindrance(
        name="Vow",
        description="Character has sworn an oath of some sort",
        severity="Minor"
    ),
    Hindrance(
        name="Wanted",
        description="Character is sought by the law or other powerful group",
        severity="Minor"
    ),
    Hindrance(
        name="Yellow",
        description="-2 to Guts rolls and fear checks",
        severity="Major"
    ),
    Hindrance(
        name="Young",
        description="-1 to attribute die types, +5 skill points",
        severity="Major"
    )
]

# Common Skills and their linked attributes
SKILL_LIST: Dict[str, str] = {
    "Boating": "Agility",
    "Climbing": "Strength", 
    "Driving": "Agility",
    "Fighting": "Agility",
    "Gambling": "Smarts",
    "Guts": "Spirit",
    "Healing": "Smarts",
    "Intimidation": "Spirit",
    "Investigation": "Smarts", 
    "Knowledge": "Smarts",  # Requires specialization
    "Lockpicking": "Agility",
    "Notice": "Smarts",
    "Persuasion": "Spirit",
    "Piloting": "Agility",
    "Repair": "Smarts",
    "Riding": "Agility",
    "Shooting": "Agility",
    "Stealth": "Agility",
    "Streetwise": "Smarts",
    "Survival": "Smarts",
    "Swimming": "Agility",
    "Taunt": "Smarts",
    "Throwing": "Agility",
    "Tracking": "Smarts"
}

# Common Weapons
COMMON_WEAPONS: List[Weapon] = [
    # Melee Weapons
    Weapon(
        name="Knife",
        weapon_type=WeaponType.MELEE,
        damage="Str+d4",
        description="Small blade",
        weight=1.0,
        cost=25,
        parry_modifier=-1,
        special_rules=["Can be thrown"]
    ),
    Weapon(
        name="Sword (Long)",
        weapon_type=WeaponType.MELEE,
        damage="Str+d8",
        description="Classic medieval sword",
        weight=8.0,
        cost=300,
        parry_modifier=1,
        reach=1
    ),
    Weapon(
        name="Great Sword",
        weapon_type=WeaponType.MELEE,
        damage="Str+d10",
        description="Two-handed sword",
        weight=12.0,
        cost=400,
        parry_modifier=-1,
        reach=1,
        min_strength="d8",
        special_rules=["Two-handed", "Reach 1"]
    ),
    Weapon(
        name="Rapier",
        weapon_type=WeaponType.MELEE,
        damage="Str+d4",
        description="Fencing sword",
        weight=3.0,
        cost=150,
        parry_modifier=1,
        special_rules=["Defensive +1"]
    ),
    Weapon(
        name="Spear",
        weapon_type=WeaponType.MELEE,
        damage="Str+d6",
        description="Long polearm",
        weight=5.0,
        cost=100,
        parry_modifier=1,
        reach=1,
        special_rules=["Reach 1", "Can be thrown"]
    ),
    Weapon(
        name="Staff",
        weapon_type=WeaponType.MELEE,
        damage="Str+d4",
        description="Wooden staff",
        weight=8.0,
        cost=10,
        parry_modifier=1,
        reach=1,
        special_rules=["Reach 1", "Two-handed"]
    ),
    Weapon(
        name="Unarmed",
        weapon_type=WeaponType.MELEE,
        damage="Str",
        description="Fists, kicks, etc.",
        weight=0.0,
        cost=0,
        parry_modifier=0
    ),
    
    # Ranged Weapons
    Weapon(
        name="Bow",
        weapon_type=WeaponType.RANGED,
        damage="2d6",
        description="Longbow",
        range_short=12,
        range_medium=24,
        range_long=48,
        weight=3.0,
        cost=250,
        min_strength="d6",
        special_rules=["Two-handed"]
    ),
    Weapon(
        name="Crossbow",
        weapon_type=WeaponType.RANGED,
        damage="2d6",
        description="Heavy crossbow",
        range_short=15,
        range_medium=30,
        range_long=60,
        weight=10.0,
        cost=500,
        special_rules=["Two-handed", "Reload 1"]
    ),
    Weapon(
        name="Musket",
        weapon_type=WeaponType.RANGED,
        damage="2d8",
        description="Flintlock musket",
        range_short=10,
        range_medium=20,
        range_long=40,
        weight=15.0,
        cost=300,
        shots=1,
        special_rules=["Two-handed", "Reload 3"]
    ),
    Weapon(
        name="Pistol (.45)",
        weapon_type=WeaponType.RANGED,
        damage="2d6+1",
        description="Heavy pistol",
        range_short=12,
        range_medium=24,
        range_long=48,
        weight=4.0,
        cost=200,
        shots=6,
        special_rules=["Semi-Auto"]
    ),
    Weapon(
        name="Rifle (.30-06)",
        weapon_type=WeaponType.RANGED,
        damage="2d8",
        description="Hunting rifle",
        range_short=24,
        range_medium=48,
        range_long=96,
        weight=8.0,
        cost=350,
        shots=5,
        special_rules=["Two-handed", "AP 2"]
    ),
    Weapon(
        name="Shotgun (12 gauge)",
        weapon_type=WeaponType.RANGED,
        damage="1d10+2",
        description="Double-barrel shotgun",
        range_short=12,
        range_medium=24,
        range_long=48,
        weight=11.0,
        cost=300,
        shots=2,
        special_rules=["Two-handed", "Spread"]
    ),
    
    # Thrown Weapons
    Weapon(
        name="Throwing Knife",
        weapon_type=WeaponType.THROWN,
        damage="Str+d4",
        description="Balanced throwing blade",
        range_short=3,
        range_medium=6,
        range_long=12,
        weight=0.5,
        cost=25
    ),
    Weapon(
        name="Javelin",
        weapon_type=WeaponType.THROWN,
        damage="Str+d6",
        description="Light spear for throwing",
        range_short=3,
        range_medium=6,
        range_long=12,
        weight=3.0,
        cost=100
    ),
    Weapon(
        name="Rock",
        weapon_type=WeaponType.THROWN,
        damage="Str+d4",
        description="Improvised throwing stone",
        range_short=3,
        range_medium=6,
        range_long=12,
        weight=0.5,
        cost=0
    )
]

# Common Armor
COMMON_ARMOR: List[Armor] = [
    # Body Armor
    Armor(
        name="Leather Armor",
        armor_type=ArmorType.BODY,
        armor_bonus=1,
        description="Soft leather protection",
        covers_torso=True,
        covers_arms=True,
        weight=15.0,
        cost=150
    ),
    Armor(
        name="Chain Mail",
        armor_type=ArmorType.BODY,
        armor_bonus=2,
        description="Interlocked metal rings",
        covers_torso=True,
        covers_arms=True,
        weight=25.0,
        cost=300,
        special_rules=["Covers torso and arms"]
    ),
    Armor(
        name="Plate Mail",
        armor_type=ArmorType.BODY,
        armor_bonus=3,
        description="Full plate armor",
        covers_torso=True,
        covers_arms=True,
        covers_legs=True,
        weight=50.0,
        cost=1500,
        min_strength="d6",
        special_rules=["Heavy Armor"]
    ),
    Armor(
        name="Kevlar Vest",
        armor_type=ArmorType.BODY,
        armor_bonus=2,
        description="Modern ballistic vest",
        covers_torso=True,
        weight=5.0,
        cost=175,
        special_rules=["Ballistic protection"]
    ),
    Armor(
        name="Flak Jacket",
        armor_type=ArmorType.BODY,
        armor_bonus=2,
        description="Military body armor",
        covers_torso=True,
        weight=9.0,
        cost=100,
        special_rules=["vs. area effect only"]
    ),
    
    # Head Protection
    Armor(
        name="Helmet (Steel)",
        armor_type=ArmorType.HEAD,
        armor_bonus=3,
        description="Metal helmet",
        covers_head=True,
        weight=5.0,
        cost=80,
        special_rules=["Head only", "50% vs. head shots"]
    ),
    Armor(
        name="Helmet (Kevlar)",
        armor_type=ArmorType.HEAD,
        armor_bonus=4,
        description="Modern combat helmet",
        covers_head=True,
        weight=3.0,
        cost=100,
        special_rules=["Head only", "50% vs. head shots"]
    ),
    
    # Shields
    Armor(
        name="Small Shield",
        armor_type=ArmorType.SHIELD,
        armor_bonus=1,
        description="Buckler or small round shield",
        parry_bonus=1,
        weight=8.0,
        cost=50,
        special_rules=["+1 Parry", "Cover -2"]
    ),
    Armor(
        name="Medium Shield",
        armor_type=ArmorType.SHIELD,
        armor_bonus=2,
        description="Standard warrior's shield",
        parry_bonus=1,
        weight=12.0,
        cost=100,
        special_rules=["+1 Parry", "Cover -2"]
    ),
    Armor(
        name="Large Shield",
        armor_type=ArmorType.SHIELD,
        armor_bonus=3,
        description="Tower shield",
        parry_bonus=2,
        weight=20.0,
        cost=200,
        min_strength="d6",
        special_rules=["+2 Parry", "Cover -4"]
    )
]

# Common Equipment
COMMON_EQUIPMENT: List[Equipment] = [
    Equipment(
        name="Backpack",
        description="Carries extra gear",
        weight=2.0,
        cost=50,
        notes="Increases carrying capacity"
    ),
    Equipment(
        name="Bedroll",
        description="Sleeping gear",
        weight=4.0,
        cost=25
    ),
    Equipment(
        name="Rope (10 yards)",
        description="Hemp rope",
        weight=15.0,
        cost=20
    ),
    Equipment(
        name="Torch",
        description="Provides light for 1 hour",
        weight=1.0,
        cost=5,
        quantity=5
    ),
    Equipment(
        name="Rations (1 day)",
        description="Preserved food",
        weight=1.0,
        cost=5,
        quantity=7
    ),
    Equipment(
        name="Waterskin",
        description="Holds 1 quart of water",
        weight=1.0,
        cost=5
    ),
    Equipment(
        name="Flint and Steel",
        description="For starting fires",
        weight=1.0,
        cost=10
    ),
    Equipment(
        name="Lockpicks",
        description="Thieves' tools",
        weight=1.0,
        cost=200,
        notes="+2 to Lockpicking rolls"
    ),
    Equipment(
        name="Healing Kit",
        description="Basic medical supplies",
        weight=3.0,
        cost=200,
        notes="+2 to Healing rolls, 3 uses"
    ),
    Equipment(
        name="Grappling Hook",
        description="For climbing",
        weight=2.0,
        cost=100
    ),
    Equipment(
        name="Lantern",
        description="Oil lantern, bright light",
        weight=3.0,
        cost=25,
        notes="4 hour burn time"
    ),
    Equipment(
        name="Oil (1 pint)",
        description="Lamp oil",
        weight=1.0,
        cost=5,
        quantity=4
    ),
    Equipment(
        name="Crowbar",
        description="Prying tool",
        weight=5.0,
        cost=20,
        notes="+2 to Strength rolls for prying"
    ),
    Equipment(
        name="Riding Horse",
        description="Light riding horse",
        weight=0.0,  # Doesn't count against encumbrance
        cost=500,
        notes="Pace 12, can carry rider + 200 lbs"
    ),
    Equipment(
        name="Warhorse",
        description="Heavy warhorse",
        weight=0.0,
        cost=750,
        notes="Pace 10, can carry rider + 300 lbs, trained for combat"
    )
]