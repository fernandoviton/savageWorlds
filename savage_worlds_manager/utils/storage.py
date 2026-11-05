"""
Character persistence system for saving/loading characters to/from JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict

from ..models.character import Character, Race, Attribute, Skill, Edge, Hindrance, Gear
from ..models.equipment import Weapon, Armor, Equipment, WeaponType, ArmorType
from ..utils.dice import DieType


class CharacterStorage:
    """Handles saving and loading characters to/from JSON files."""
    
    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            # Default to a characters folder in user's home directory
            self.storage_dir = Path.home() / "savage_worlds_characters"
        else:
            self.storage_dir = Path(storage_dir)
        
        # Create directory if it doesn't exist
        self.storage_dir.mkdir(exist_ok=True)
    
    def _character_to_dict(self, character: Character) -> Dict:
        """Convert a Character object to a JSON-serializable dictionary."""
        # Convert dataclass to dict, but handle special cases
        char_dict = asdict(character)
        
        # Convert enums to their values
        char_dict['race'] = character.race.value
        
        # Convert attributes
        for attr_name, attr in char_dict['attributes'].items():
            char_dict['attributes'][attr_name]['die_type'] = attr['die_type'].value
        
        # Convert skills
        for skill_name, skill in char_dict['skills'].items():
            char_dict['skills'][skill_name]['die_type'] = skill['die_type'].value
        
        # Convert weapons
        for i, weapon in enumerate(char_dict['weapons']):
            char_dict['weapons'][i]['weapon_type'] = weapon['weapon_type'].value
        
        # Convert armor
        for i, armor in enumerate(char_dict['armor']):
            char_dict['armor'][i]['armor_type'] = armor['armor_type'].value
        
        return char_dict
    
    def _dict_to_character(self, char_dict: Dict) -> Character:
        """Convert a dictionary back to a Character object."""
        # Handle race enum
        race = Race(char_dict['race'])
        
        # Create character with basic info
        character = Character(
            name=char_dict['name'],
            player_name=char_dict.get('player_name', ''),
            race=race,
            concept=char_dict.get('concept', '')
        )
        
        # Restore attributes
        for attr_name, attr_data in char_dict['attributes'].items():
            die_type = DieType(attr_data['die_type'])
            character.attributes[attr_name] = Attribute(attr_data['name'], die_type)
        
        # Restore skills
        character.skills = {}
        for skill_name, skill_data in char_dict['skills'].items():
            die_type = DieType(skill_data['die_type'])
            character.skills[skill_name] = Skill(
                name=skill_data['name'],
                linked_attribute=skill_data['linked_attribute'],
                die_type=die_type,
                specialization=skill_data.get('specialization')
            )
        
        # Restore edges
        character.edges = []
        for edge_data in char_dict['edges']:
            character.edges.append(Edge(
                name=edge_data['name'],
                description=edge_data['description'],
                requirements=edge_data.get('requirements', [])
            ))
        
        # Restore hindrances
        character.hindrances = []
        for hindrance_data in char_dict['hindrances']:
            character.hindrances.append(Hindrance(
                name=hindrance_data['name'],
                description=hindrance_data['description'],
                severity=hindrance_data['severity']
            ))
        
        # Restore gear
        character.gear = []
        for gear_data in char_dict.get('gear', []):
            character.gear.append(Gear(
                name=gear_data['name'],
                description=gear_data.get('description', ''),
                weight=gear_data.get('weight', 0.0),
                cost=gear_data.get('cost', 0)
            ))
        
        # Restore weapons
        character.weapons = []
        for weapon_data in char_dict.get('weapons', []):
            weapon_type = WeaponType(weapon_data['weapon_type'])
            character.weapons.append(Weapon(
                name=weapon_data['name'],
                weapon_type=weapon_type,
                damage=weapon_data['damage'],
                description=weapon_data.get('description', ''),
                reach=weapon_data.get('reach', 0),
                parry_modifier=weapon_data.get('parry_modifier', 0),
                range_short=weapon_data.get('range_short', 0),
                range_medium=weapon_data.get('range_medium', 0),
                range_long=weapon_data.get('range_long', 0),
                rate_of_fire=weapon_data.get('rate_of_fire', 1),
                shots=weapon_data.get('shots'),
                weight=weapon_data.get('weight', 0.0),
                cost=weapon_data.get('cost', 0),
                min_strength=weapon_data.get('min_strength'),
                special_rules=weapon_data.get('special_rules', [])
            ))
        
        # Restore armor
        character.armor = []
        for armor_data in char_dict.get('armor', []):
            armor_type = ArmorType(armor_data['armor_type'])
            character.armor.append(Armor(
                name=armor_data['name'],
                armor_type=armor_type,
                armor_bonus=armor_data['armor_bonus'],
                description=armor_data.get('description', ''),
                covers_torso=armor_data.get('covers_torso', True),
                covers_arms=armor_data.get('covers_arms', False),
                covers_legs=armor_data.get('covers_legs', False),
                covers_head=armor_data.get('covers_head', False),
                parry_bonus=armor_data.get('parry_bonus', 0),
                toughness_bonus=armor_data.get('toughness_bonus', 0),
                weight=armor_data.get('weight', 0.0),
                cost=armor_data.get('cost', 0),
                min_strength=armor_data.get('min_strength'),
                special_rules=armor_data.get('special_rules', [])
            ))
        
        # Restore equipment
        character.equipment = []
        for equipment_data in char_dict.get('equipment', []):
            character.equipment.append(Equipment(
                name=equipment_data['name'],
                description=equipment_data.get('description', ''),
                weight=equipment_data.get('weight', 0.0),
                cost=equipment_data.get('cost', 0),
                quantity=equipment_data.get('quantity', 1),
                notes=equipment_data.get('notes', '')
            ))
        
        # Restore other properties
        character.pace = char_dict.get('pace', 6)
        character.parry = char_dict.get('parry', 2)
        character.toughness = char_dict.get('toughness', 2)
        character.charisma = char_dict.get('charisma', 0)
        character.bennies = char_dict.get('bennies', 3)
        character.current_wounds = char_dict.get('current_wounds', 0)
        character.current_fatigue = char_dict.get('current_fatigue', 0)
        character.attribute_points_spent = char_dict.get('attribute_points_spent', 0)
        character.skill_points_spent = char_dict.get('skill_points_spent', 0)
        
        return character
    
    def save_character(self, character: Character) -> str:
        """
        Save a character to a JSON file.
        
        Args:
            character: The character to save
            
        Returns:
            The filename where the character was saved
        """
        # Create filename from character name (sanitized)
        safe_name = "".join(c for c in character.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        filename = f"{safe_name}.json"
        filepath = self.storage_dir / filename
        
        # Convert character to dict and save
        char_dict = self._character_to_dict(character)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(char_dict, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def load_character(self, filename: str) -> Character:
        """
        Load a character from a JSON file.
        
        Args:
            filename: Name of the file to load (with or without .json extension)
            
        Returns:
            The loaded Character object
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.storage_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Character file not found: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                char_dict = json.load(f)
            
            return self._dict_to_character(char_dict)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid character file format: {e}")
        except Exception as e:
            raise ValueError(f"Error loading character: {e}")
    
    def list_characters(self) -> List[str]:
        """
        List all saved character files.
        
        Returns:
            List of character filenames (without .json extension)
        """
        character_files = []
        
        for filepath in self.storage_dir.glob("*.json"):
            # Remove .json extension for display
            character_files.append(filepath.stem)
        
        return sorted(character_files)
    
    def delete_character(self, filename: str) -> bool:
        """
        Delete a character file.
        
        Args:
            filename: Name of the file to delete (with or without .json extension)
            
        Returns:
            True if file was deleted, False if it didn't exist
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.storage_dir / filename
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def character_exists(self, filename: str) -> bool:
        """
        Check if a character file exists.
        
        Args:
            filename: Name of the file to check (with or without .json extension)
            
        Returns:
            True if the file exists
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.storage_dir / filename
        return filepath.exists()
    
    def get_character_info(self, filename: str) -> Dict:
        """
        Get basic character information without fully loading the character.
        
        Args:
            filename: Name of the file to check (with or without .json extension)
            
        Returns:
            Dictionary with basic character info (name, race, concept)
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.storage_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Character file not found: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                char_dict = json.load(f)
            
            return {
                'name': char_dict.get('name', 'Unknown'),
                'race': char_dict.get('race', 'Unknown'),
                'concept': char_dict.get('concept', ''),
                'player_name': char_dict.get('player_name', '')
            }
            
        except json.JSONDecodeError:
            return {'name': 'Invalid File', 'race': '', 'concept': '', 'player_name': ''}