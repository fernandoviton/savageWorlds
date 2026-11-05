"""
Command Line Interface for Savage Worlds Character Manager.
"""

import click
from typing import Optional

from ..models.character import Character, Race
from ..models.character_creator import CharacterCreator, CharacterCreationError
from ..utils.dice import DieType, roll_trait_test
from ..utils.dice_guide import get_dice_guide
from ..data.game_data import SKILL_LIST, COMMON_EDGES, COMMON_HINDRANCES, COMMON_WEAPONS, COMMON_ARMOR, COMMON_EQUIPMENT
from ..utils.storage import CharacterStorage
from .character_display import CharacterSheet


@click.group()
def main_cli():
    """Savage Worlds Character Manager CLI."""
    pass


@main_cli.command()
@click.option('--name', prompt='Character name', help='Name of the character')
@click.option('--player', default='', help='Player name')
@click.option('--concept', default='', help='Character concept/description')
def create(name: str, player: str, concept: str):
    """Create a new character interactively."""
    try:
        creator = CharacterCreator()
        display = CharacterSheet()
        
        # Create base character
        character = creator.create_new_character(name, player, Race.HUMAN, concept)
        
        click.echo(f"\n=== Creating Character: {name} ===")
        click.echo("Starting with base human character (all attributes at d4)")
        click.echo(f"Available points: {creator.STARTING_ATTRIBUTE_POINTS} attribute, {creator.STARTING_SKILL_POINTS} skill")
        
        # Interactive attribute allocation
        click.echo("\n--- Attribute Allocation ---")
        click.echo("Attributes cost 1 point per die step (d4->d6->d8->d10->d12)")
        
        for attr_name in character.attributes.keys():
            while True:
                current_die = character.get_attribute_die(attr_name)
                remaining_points = creator.STARTING_ATTRIBUTE_POINTS - character.attribute_points_spent
                
                click.echo(f"\n{attr_name} currently: {current_die} (Points remaining: {remaining_points})")
                
                if remaining_points <= 0:
                    click.echo("No attribute points remaining!")
                    break
                    
                new_value = click.prompt(
                    f"Set {attr_name} to (4/6/8/10/12) or 'skip'",
                    default='skip',
                    type=str
                )
                
                if new_value.lower() == 'skip':
                    break
                    
                try:
                    die_value = int(new_value)
                    if die_value not in [4, 6, 8, 10, 12]:
                        click.echo("Invalid die value. Use 4, 6, 8, 10, or 12")
                        continue
                        
                    target_die = DieType(die_value)
                    creator.set_attribute(attr_name, target_die)
                    click.echo(f"Set {attr_name} to {target_die}")
                    break
                    
                except (ValueError, CharacterCreationError) as e:
                    click.echo(f"Error: {e}")
                    
        # Interactive skill allocation  
        click.echo("\n--- Skill Allocation ---")
        click.echo("Skills cost: d4->d6 (1pt), d6->d8 (1pt), d8->d10 (2pts), d10->d12 (2pts)")
        click.echo("Skills cannot exceed their linked attribute")
        
        while True:
            remaining_points = creator.STARTING_SKILL_POINTS - character.skill_points_spent
            
            if remaining_points <= 0:
                click.echo("No skill points remaining!")
                break
                
            click.echo(f"\nSkill points remaining: {remaining_points}")
            click.echo("Available skills:")
            
            # Show available skills in groups
            for i, (skill_name, linked_attr) in enumerate(sorted(SKILL_LIST.items()), 1):
                current_die = character.get_skill_die(skill_name)
                attr_die = character.get_attribute_die(linked_attr)
                click.echo(f"  {i:2}. {skill_name:<15} ({linked_attr}) - Currently: {current_die}, Max: {attr_die}")
            
            skill_choice = click.prompt(
                "\nEnter skill number, skill name, or 'done'",
                default='done',
                type=str
            )
            
            if skill_choice.lower() == 'done':
                break
                
            # Handle skill selection
            selected_skill = None
            try:
                # Try as number first
                skill_num = int(skill_choice)
                skill_list = list(sorted(SKILL_LIST.keys()))
                if 1 <= skill_num <= len(skill_list):
                    selected_skill = skill_list[skill_num - 1]
            except ValueError:
                # Try as skill name
                if skill_choice in SKILL_LIST:
                    selected_skill = skill_choice
                    
            if not selected_skill:
                click.echo("Invalid skill selection")
                continue
                
            # Get target die level
            current_die = character.get_skill_die(selected_skill)
            attr_die = character.get_attribute_die(SKILL_LIST[selected_skill])
            
            new_value = click.prompt(
                f"Set {selected_skill} to (4/6/8/10/12) or 'skip'",
                default='skip',
                type=str
            )
            
            if new_value.lower() == 'skip':
                continue
                
            try:
                die_value = int(new_value)
                if die_value not in [4, 6, 8, 10, 12]:
                    click.echo("Invalid die value. Use 4, 6, 8, 10, or 12")
                    continue
                    
                target_die = DieType(die_value)
                creator.set_skill(selected_skill, target_die)
                click.echo(f"Set {selected_skill} to {target_die}")
                
            except (ValueError, CharacterCreationError) as e:
                click.echo(f"Error: {e}")
        
        # Finalize character
        try:
            final_character = creator.finalize_character()
            click.echo("\n=== Character Creation Complete! ===")
            
            # Display character sheet 
            display.display_character(final_character)
            
            # Ask to save
            if click.confirm("\nSave this character?"):
                try:
                    storage = CharacterStorage()
                    filename = storage.save_character(final_character)
                    click.echo(f"Character saved as: {filename}")
                except Exception as e:
                    click.echo(f"Error saving character: {e}")
                
        except CharacterCreationError as e:
            click.echo(f"Character validation failed: {e}")
            
    except Exception as e:
        click.echo(f"Error creating character: {e}")


@main_cli.command()
def list():
    """List all saved characters."""
    try:
        storage = CharacterStorage()
        characters = storage.list_characters()
        
        if not characters:
            click.echo("No saved characters found.")
            return
        
        click.echo("Saved Characters:")
        click.echo("================")
        
        for i, char_name in enumerate(characters, 1):
            try:
                char_info = storage.get_character_info(char_name)
                click.echo(f"{i:2}. {char_info['name']} ({char_info['race']}) - {char_info['concept']}")
                if char_info['player_name']:
                    click.echo(f"     Player: {char_info['player_name']}")
            except Exception as e:
                click.echo(f"{i:2}. {char_name} (Error loading info: {e})")
                
    except Exception as e:
        click.echo(f"Error listing characters: {e}")


@main_cli.command()
@click.argument('character_name', required=False)
def load(character_name: Optional[str]):
    """Load an existing character."""
    try:
        storage = CharacterStorage()
        display = CharacterSheet()
        
        if not character_name:
            # Show list of available characters
            characters = storage.list_characters()
            
            if not characters:
                click.echo("No saved characters found.")
                return
            
            click.echo("Available Characters:")
            for i, char_name in enumerate(characters, 1):
                try:
                    char_info = storage.get_character_info(char_name)
                    click.echo(f"{i:2}. {char_info['name']} ({char_info['race']})")
                except Exception:
                    click.echo(f"{i:2}. {char_name}")
            
            choice = click.prompt(
                "\nEnter character number or name",
                type=str
            )
            
            # Handle numeric choice
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(characters):
                    character_name = characters[choice_num - 1]
                else:
                    click.echo("Invalid character number.")
                    return
            except ValueError:
                character_name = choice
        
        # Load and display the character
        try:
            character = storage.load_character(character_name)
            click.echo(f"\n=== Loaded Character: {character.name} ===")
            display.display_character(character)
            
            # Ask what to do next
            click.echo("\nOptions:")
            click.echo("1. Roll dice")
            click.echo("2. Modify character (coming soon)")
            click.echo("3. Manage equipment")
            click.echo("4. Delete character")
            click.echo("5. Exit")
            
            action = click.prompt("Choose an option", type=int, default=5)
            
            if action == 1:
                # Interactive dice rolling
                while True:
                    skill_name = click.prompt(
                        f"\nEnter skill name to roll (or 'quit')",
                        default='quit',
                        type=str
                    )
                    
                    if skill_name.lower() == 'quit':
                        break
                    
                    if skill_name in character.skills:
                        skill_die = character.get_skill_die(skill_name)
                        modifier = click.prompt("Enter modifier", default=0, type=int)
                        target_number = click.prompt("Enter target number", default=4, type=int)
                        
                        from ..utils.dice import make_skill_check, TargetNumber
                        success, raises, skill_roll, wild_roll = make_skill_check(skill_die, target_number, modifier)
                        
                        click.echo(f"\n{skill_name} Test (TN {target_number}):")
                        click.echo(f"Skill die: {skill_roll}")
                        click.echo(f"Wild die:  {wild_roll}")
                        
                        if success:
                            click.echo(f"SUCCESS! ({raises} raises)" if raises > 0 else "SUCCESS!")
                        else:
                            click.echo("FAILURE!")
                    else:
                        click.echo(f"Character doesn't have the skill: {skill_name}")
            
            elif action == 3:
                # Equipment management
                _manage_equipment_interactive(character, storage, character_name)
            
            elif action == 4:
                if click.confirm(f"Delete character '{character.name}'? This cannot be undone."):
                    if storage.delete_character(character_name):
                        click.echo("Character deleted successfully.")
                    else:
                        click.echo("Error deleting character.")
            
        except FileNotFoundError:
            click.echo(f"Character '{character_name}' not found.")
        except ValueError as e:
            click.echo(f"Error loading character: {e}")
            
    except Exception as e:
        click.echo(f"Error: {e}")


@main_cli.command()
@click.option('--die', default='d6', help='Die type to roll (d4, d6, d8, d10, d12)')
@click.option('--modifier', '-m', default=0, help='Modifier to add to roll')
@click.option('--wild-die', '-w', is_flag=True, help='Include wild die (d6)')
def roll(die: str, modifier: int, wild_die: bool):
    """Roll dice with Savage Worlds mechanics."""
    try:
        # Parse die type
        if not die.startswith('d'):
            die = f'd{die}'
            
        die_value = int(die[1:])
        if die_value not in [4, 6, 8, 10, 12]:
            click.echo("Invalid die type. Use d4, d6, d8, d10, or d12")
            return
            
        trait_die = DieType(die_value)
        
        if wild_die:
            # Trait test with wild die
            best_total, trait_roll, wild_roll = roll_trait_test(trait_die, DieType.D6, modifier)
            click.echo(f"\nTrait Test: {trait_die} + Wild Die")
            click.echo(f"Trait die: {trait_roll}")
            click.echo(f"Wild die:  {wild_roll}")
            click.echo(f"Best result: {best_total}")
        else:
            # Simple die roll
            from ..utils.dice import DiceRoll
            roll_result = DiceRoll(trait_die, modifier)
            total = roll_result.roll()
            click.echo(f"\nRoll: {roll_result}")
            
    except ValueError as e:
        click.echo(f"Error: {e}")


@main_cli.command()
def demo():
    """Show a demo character."""
    try:
        # Create a sample character
        creator = CharacterCreator()
        display = CharacterSheet()
        
        character = creator.create_new_character("Kalara Swiftblade", "Demo Player", Race.HUMAN, "Agile warrior")
        
        # Set some attributes
        creator.set_attribute("Agility", DieType.D8)
        creator.set_attribute("Strength", DieType.D6) 
        creator.set_attribute("Spirit", DieType.D6)
        creator.set_attribute("Smarts", DieType.D6)
        
        # Set some skills (must not exceed linked attributes)
        creator.set_skill("Fighting", DieType.D8)  # Linked to Agility (d8)
        creator.set_skill("Shooting", DieType.D6)  # Linked to Agility (d8)
        creator.set_skill("Notice", DieType.D6)    # Linked to Smarts (d6)
        creator.set_skill("Stealth", DieType.D6)   # Linked to Agility (d8)
        
        # Add an edge and hindrance
        creator.add_edge("Combat Reflexes")
        creator.add_hindrance("Curious")
        
        # Add some equipment
        from ..models.equipment import Weapon, Armor, Equipment, WeaponType, ArmorType
        
        # Add weapons
        sword = Weapon(
            name="Long Sword",
            weapon_type=WeaponType.MELEE,
            damage="Str+d8",
            parry_modifier=1,
            weight=8.0,
            description="Well-balanced blade"
        )
        bow = Weapon(
            name="Composite Bow",
            weapon_type=WeaponType.RANGED,
            damage="2d6",
            range_short=12,
            range_medium=24,
            range_long=48,
            weight=3.0,
            description="Powerful recurved bow"
        )
        character.add_weapon(sword)
        character.add_weapon(bow)
        
        # Add armor
        leather_armor = Armor(
            name="Studded Leather",
            armor_type=ArmorType.BODY,
            armor_bonus=2,
            weight=15.0,
            description="Reinforced leather armor"
        )
        character.add_armor(leather_armor)
        
        # Add equipment
        equipment_items = [
            Equipment("Backpack", "Leather traveling pack", weight=2.0),
            Equipment("Rope (50 ft)", "Hemp rope", weight=10.0),
            Equipment("Rations", "Trail rations", weight=1.0, quantity=7),
            Equipment("Healing Potion", "Minor healing draught", quantity=2)
        ]
        
        for item in equipment_items:
            character.add_equipment(item)
        
        final_character = creator.finalize_character()
        
        click.echo("=== Demo Character ===")
        display.display_character(final_character)
        
    except Exception as e:
        click.echo(f"Error creating demo character: {e}")


def _manage_equipment_interactive(character: Character, storage: CharacterStorage, character_name: str):
    """Interactive equipment management for a character."""
    display = CharacterSheet()
    
    while True:
        click.echo(f"\n=== Equipment Management: {character.name} ===")
        click.echo("1. Add weapon")
        click.echo("2. Add armor")
        click.echo("3. Add equipment")
        click.echo("4. Remove item")
        click.echo("5. Show character sheet")
        click.echo("6. Save and return")
        
        choice = click.prompt("Choose option", type=int, default=6)
        
        if choice == 1:
            _add_weapon_interactive(character)
        elif choice == 2:
            _add_armor_interactive(character)
        elif choice == 3:
            _add_equipment_interactive(character)
        elif choice == 4:
            _remove_item_interactive(character)
        elif choice == 5:
            display.display_character(character)
        elif choice == 6:
            # Save character and return
            try:
                storage.save_character(character)
                click.echo("Character saved successfully!")
                break
            except Exception as e:
                click.echo(f"Error saving character: {e}")
                if not click.confirm("Continue without saving?"):
                    continue
                break


def _add_weapon_interactive(character: Character):
    """Add a weapon to the character interactively."""
    click.echo("\nAvailable Weapons:")
    for i, weapon in enumerate(COMMON_WEAPONS, 1):
        click.echo(f"{i:2}. {weapon.name} - {weapon.damage} ({weapon.weapon_type.value})")
    
    choice = click.prompt("Select weapon number or 'custom'", default="custom")
    
    if choice.lower() == "custom":
        # Custom weapon creation
        name = click.prompt("Weapon name")
        weapon_type_str = click.prompt("Type (melee/ranged/thrown)", default="melee")
        damage = click.prompt("Damage (e.g., Str+d6, 2d8)", default="Str+d6")
        
        from ..models.equipment import WeaponType
        try:
            weapon_type = WeaponType(weapon_type_str.title())
        except ValueError:
            weapon_type = WeaponType.MELEE
        
        from ..models.equipment import Weapon
        weapon = Weapon(name=name, weapon_type=weapon_type, damage=damage)
        character.add_weapon(weapon)
        click.echo(f"Added custom weapon: {weapon.name}")
    else:
        try:
            weapon_index = int(choice) - 1
            if 0 <= weapon_index < len(COMMON_WEAPONS):
                weapon = COMMON_WEAPONS[weapon_index]
                character.add_weapon(weapon)
                click.echo(f"Added weapon: {weapon.name}")
            else:
                click.echo("Invalid weapon selection")
        except ValueError:
            click.echo("Invalid selection")


def _add_armor_interactive(character: Character):
    """Add armor to the character interactively."""
    click.echo("\nAvailable Armor:")
    for i, armor in enumerate(COMMON_ARMOR, 1):
        click.echo(f"{i:2}. {armor.name} - +{armor.armor_bonus} Armor ({armor.armor_type.value})")
    
    choice = click.prompt("Select armor number or 'custom'", default="custom")
    
    if choice.lower() == "custom":
        # Custom armor creation
        name = click.prompt("Armor name")
        armor_bonus = click.prompt("Armor bonus", type=int, default=1)
        
        from ..models.equipment import Armor, ArmorType
        armor = Armor(name=name, armor_type=ArmorType.BODY, armor_bonus=armor_bonus)
        character.add_armor(armor)
        click.echo(f"Added custom armor: {armor.name}")
    else:
        try:
            armor_index = int(choice) - 1
            if 0 <= armor_index < len(COMMON_ARMOR):
                armor = COMMON_ARMOR[armor_index]
                character.add_armor(armor)
                click.echo(f"Added armor: {armor.name}")
            else:
                click.echo("Invalid armor selection")
        except ValueError:
            click.echo("Invalid selection")


def _add_equipment_interactive(character: Character):
    """Add equipment to the character interactively."""
    click.echo("\nAvailable Equipment:")
    for i, equipment in enumerate(COMMON_EQUIPMENT, 1):
        click.echo(f"{i:2}. {equipment.name} - {equipment.description}")
    
    choice = click.prompt("Select equipment number or 'custom'", default="custom")
    
    if choice.lower() == "custom":
        # Custom equipment creation
        name = click.prompt("Equipment name")
        description = click.prompt("Description", default="")
        quantity = click.prompt("Quantity", type=int, default=1)
        
        from ..models.equipment import Equipment
        equipment = Equipment(name=name, description=description, quantity=quantity)
        character.add_equipment(equipment)
        click.echo(f"Added custom equipment: {equipment.name}")
    else:
        try:
            equipment_index = int(choice) - 1
            if 0 <= equipment_index < len(COMMON_EQUIPMENT):
                equipment = COMMON_EQUIPMENT[equipment_index]
                character.add_equipment(equipment)
                click.echo(f"Added equipment: {equipment.name}")
            else:
                click.echo("Invalid equipment selection")
        except ValueError:
            click.echo("Invalid selection")


def _remove_item_interactive(character: Character):
    """Remove an item from the character interactively."""
    all_items = []
    
    # Collect all items
    for weapon in character.weapons:
        all_items.append(("weapon", weapon.name, weapon))
    for armor in character.armor:
        all_items.append(("armor", armor.name, armor))
    for equipment in character.equipment:
        all_items.append(("equipment", equipment.name, equipment))
    for gear in character.gear:  # Legacy gear
        all_items.append(("gear", gear.name, gear))
    
    if not all_items:
        click.echo("No items to remove")
        return
    
    click.echo("\nItems to remove:")
    for i, (item_type, item_name, _) in enumerate(all_items, 1):
        click.echo(f"{i:2}. {item_name} ({item_type})")
    
    choice = click.prompt("Select item number to remove", type=int, default=0)
    
    if 1 <= choice <= len(all_items):
        item_type, item_name, item = all_items[choice - 1]
        
        if item_type == "weapon":
            character.remove_weapon(item_name)
        elif item_type == "armor":
            character.remove_armor(item_name)
        elif item_type == "equipment":
            character.remove_equipment(item_name)
        elif item_type == "gear":
            character.gear.remove(item)
        
        click.echo(f"Removed {item_name}")
    else:
        click.echo("Invalid selection")


@main_cli.command()
@click.argument('situation', required=False)
@click.option('--list', 'list_all', is_flag=True, help='List all available guidance situations')
@click.option('--search', help='Search for guidance containing specific terms')
def guide(situation: Optional[str], list_all: bool, search: Optional[str]):
    """Get dice rolling guidance for Savage Worlds situations without actually rolling.
    
    SITUATION: The type of roll you want guidance for (e.g., 'fighting', 'shooting', 'healing')
    """
    dice_guide = get_dice_guide()
    
    if list_all:
        click.echo("🎲 Available Guidance Situations:")
        click.echo("=" * 35)
        situations = dice_guide.list_all_situations()
        for i, situation_name in enumerate(situations, 1):
            click.echo(f"{i:2}. {situation_name}")
        click.echo("\nUse: python main.py guide <situation> for specific guidance")
        return
    
    if search:
        results = dice_guide.search_guidance(search)
        if results:
            click.echo(f"🔍 Search results for '{search}':")
            click.echo("=" * (20 + len(search)))
            for i, (key, guidance) in enumerate(results, 1):
                click.echo(f"{i}. {guidance.situation}")
            click.echo("\nUse: python main.py guide <situation> for specific guidance")
        else:
            click.echo(f"No guidance found matching '{search}'")
        return
    
    if not situation:
        # Interactive mode
        click.echo("🎲 Savage Worlds Dice Rolling Guide")
        click.echo("=" * 35)
        click.echo("Available guidance categories:")
        click.echo()
        
        categories = [
            ("Combat", ["fighting", "shooting", "wild_attack", "called_shot", "full_auto"]),
            ("Damage & Healing", ["weapon_damage", "healing", "medical_healing", "soak"]),
            ("Tests & Checks", ["trait_test", "fear", "initiative"]),
            ("Special Actions", ["multi_action", "gang_up"])
        ]
        
        for category, items in categories:
            click.echo(f"📂 {category}:")
            for item in items:
                guidance = dice_guide.get_guidance(item)
                if guidance:
                    click.echo(f"  • {item} - {guidance.situation}")
            click.echo()
        
        click.echo("Examples:")
        click.echo("  python main.py guide fighting")
        click.echo("  python main.py guide healing") 
        click.echo("  python main.py guide --list")
        click.echo("  python main.py guide --search fear")
        return
    
    # Get specific guidance
    guidance = dice_guide.get_guidance(situation)
    if guidance:
        click.echo(dice_guide.format_guidance(guidance))
    else:
        click.echo(f"❌ No guidance found for '{situation}'")
        click.echo("\nAvailable situations:")
        situations = dice_guide.list_all_situations()
        for situation_name in situations[:5]:  # Show first 5
            click.echo(f"  • {situation_name.lower().replace(' ', '_')}")
        if len(situations) > 5:
            click.echo(f"  ... and {len(situations) - 5} more")
        click.echo("\nUse --list to see all available guidance")


if __name__ == "__main__":
    main_cli()