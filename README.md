# Savage Worlds Character Manager

A Python application for creating and managing characters for the Savage Worlds tabletop RPG system.

## Features

- Character creation with attribute and skill point allocation
- Edge and Hindrance management
- Equipment system (weapons, armor, and general gear)
- Combat stats calculation (Parry, Toughness, Armor, Encumbrance)
- Dice rolling system with "ace" mechanics
- Rich character sheet display with equipment panels
- Save/load characters with full equipment persistence

## Installation

1. Install Python 3.8+ 
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the character manager:
```bash
python main.py
```

### Available Commands

- `python main.py create` - Interactive character creation wizard
- `python main.py demo` - Show a demo character with formatted display
- `python main.py list` - List all saved characters
- `python main.py load [character_name]` - Load and interact with a saved character
- `python main.py roll --die d8 --modifier 2 --wild-die` - Roll dice with Savage Worlds mechanics
- `python main.py guide [situation]` - Get dice rolling guidance without actually rolling

### Example Dice Rolling

```bash
# Simple die roll
python main.py roll --die d8
# Output: Roll: d8[6] = 6

# Die roll with modifier
python main.py roll --die d10 --modifier 2
# Output: Roll: d10[7]+2 = 9

# Trait test with wild die (typical for character actions)
python main.py roll --die d8 --wild-die
# Output: 
# Trait Test: d8 + Wild Die
# Trait die: d8[5] = 5
# Wild die:  d6[3] = 3
# Best result: 5

# Example of "acing" (exploding dice)
python main.py roll --die d6
# Output: Roll: d6[6+4] = 10 (ACED!)
```

### Dice Rolling Guidance

Get help on what dice to roll for any Savage Worlds situation without actually rolling:

```bash
# Interactive guidance menu
python main.py guide

# Specific situation guidance
python main.py guide fighting
# Output: Shows Fighting (Melee Attack) guidance with dice, modifiers, and examples

python main.py guide healing  
# Output: Shows Natural Healing guidance with Vigor roll details

# List all available guidance
python main.py guide --list

# Search for specific guidance
python main.py guide --search damage
# Output: Shows all guidance related to damage

# More examples
python main.py guide shooting     # Ranged combat guidance
python main.py guide fear         # Fear check guidance  
python main.py guide wild_attack  # Wild Attack guidance
python main.py guide soak         # Damage resistance guidance
```

### Character Storage

Characters are automatically saved as JSON files in your home directory under `%USERPROFILE%\savage_worlds_characters\`. Each character file contains:

```json
{
  "name": "Character Name",
  "player_name": "Player Name", 
  "race": "Human",
  "concept": "Character concept",
  "attributes": {
    "Agility": {"name": "Agility", "die_type": 8},
    "Smarts": {"name": "Smarts", "die_type": 6}
  },
  "skills": {
    "Fighting": {"name": "Fighting", "linked_attribute": "Agility", "die_type": 8, "specialization": null}
  },
  "edges": [
    {"name": "Combat Reflexes", "description": "+2 recover from Shaken", "requirements": ["Seasoned"]}
  ],
  "hindrances": [
    {"name": "Curious", "description": "Character wants to know about everything", "severity": "Major"}
  ],
  "weapons": [
    {
      "name": "Sword (Long)",
      "weapon_type": "Melee",
      "damage": "Str+d8",
      "description": "Classic medieval sword",
      "reach": 1,
      "parry_modifier": 1,
      "range_short": 0,
      "range_medium": 0, 
      "range_long": 0,
      "rate_of_fire": 1,
      "shots": null,
      "weight": 8.0,
      "cost": 300,
      "min_strength": null,
      "special_rules": []
    }
  ],
  "armor": [
    {
      "name": "Chain Mail",
      "armor_type": "Body",
      "armor_bonus": 2,
      "description": "Interlocked metal rings",
      "covers_torso": true,
      "covers_arms": true,
      "covers_legs": false,
      "covers_head": false,
      "parry_bonus": 0,
      "toughness_bonus": 0,
      "weight": 25.0,
      "cost": 300,
      "min_strength": null,
      "special_rules": ["Covers torso and arms"]
    }
  ],
  "equipment": [
    {
      "name": "Backpack",
      "description": "Carries extra gear",
      "weight": 2.0,
      "cost": 50,
      "quantity": 1,
      "notes": "Increases carrying capacity"
    }
  ],
  "pace": 6,
  "parry": 2,
  "toughness": 2,
  "charisma": 0,
  "bennies": 3,
  "current_wounds": 0,
  "current_fatigue": 0,
  "attribute_points_spent": 0,
  "skill_points_spent": 0
}
```

## Project Structure

- `savage_worlds_manager/` - Main application package
  - `models/` - Data models for characters, attributes, skills, equipment, etc.
  - `ui/` - User interface components (CLI and potentially GUI)
  - `utils/` - Utility functions (dice rolling, validators, etc.)
  - `data/` - Static data files (edges, hindrances, weapons, armor, equipment)

## Savage Worlds Rules Implementation

This application implements core Savage Worlds mechanics including:
- Attribute dice (d4 to d12+)
- Skill dice with linked attributes
- Edge and Hindrance system
- Complete equipment system (weapons, armor, gear)
- Combat stat calculation (Parry, Toughness, Armor)
- Encumbrance and carrying capacity
- "Ace" dice mechanics (exploding dice)
- Trait tests and opposed rolls
- Damage and healing systems

## Adding New Content

### Adding Equipment

To add new weapons, armor, or equipment, edit `savage_worlds_manager/data/game_data.py`:

```python
# Add to COMMON_WEAPONS list
Weapon(
    name="New Weapon Name",
    weapon_type=WeaponType.MELEE,  # or WeaponType.RANGED
    damage="Str+d6",  # Damage formula
    description="Weapon description",
    weight=5.0,
    cost=100,
    parry_modifier=0,  # Bonus/penalty to Parry
    reach=0,  # Reach in inches
    special_rules=["Any special rules"]
),

# Add to COMMON_ARMOR list
Armor(
    name="New Armor Name",
    armor_type=ArmorType.BODY,  # BODY, HEAD, LIMBS, SHIELD
    armor_bonus=3,  # Armor rating
    description="Armor description",
    covers_torso=True,
    covers_arms=False,
    weight=20.0,
    cost=200,
    special_rules=["Coverage details"]
),

# Add to COMMON_EQUIPMENT list
Equipment(
    name="New Equipment Name",
    description="What it does",
    weight=1.0,
    cost=25,
    quantity=1,
    notes="Additional notes"
),
```

### Adding Edges and Hindrances

To add new edges or hindrances, edit `savage_worlds_manager/data/game_data.py`:

```python
# Add to COMMON_EDGES list
Edge(
    name="New Edge Name",
    description="Description of what the edge does",
    requirements=["Novice", "Attribute d8+"]  # Prerequisites
),

# Add to COMMON_HINDRANCES list  
Hindrance(
    name="New Hindrance Name",
    description="Description of the hindrance effect",
    severity="Minor"  # or "Major"
),
```

### Adding Skills

Add new skills to the `SKILL_LIST` dictionary in `game_data.py`:

```python
SKILL_LIST: Dict[str, str] = {
    "New Skill Name": "Linked_Attribute",  # e.g., "Lockpicking": "Agility"
    # ... existing skills
}
```

### Character Creation Rules

- **Starting Points:** 5 attribute points, 15 skill points
- **Attribute Costs:** Each die step costs 1 point (d4→d6→d8→d10→d12)
- **Skill Costs:** d4→d6 (1pt), d6→d8 (1pt), d8→d10 (2pts), d10→d12 (2pts)
- **Hindrances:** Max 4 points total (Major=2pts, Minor=1pt), can trade for extra skill points
- **Skills:** Cannot exceed their linked attribute die type