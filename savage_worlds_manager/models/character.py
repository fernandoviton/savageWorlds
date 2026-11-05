"""
Core character data models for Savage Worlds.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

from ..utils.dice import DieType
from .equipment import Weapon, Armor, Equipment, CombatStats


class Race(Enum):
    """Character races in Savage Worlds."""
    HUMAN = "Human"
    DWARF = "Dwarf" 
    ELF = "Elf"
    HALF_ELF = "Half-Elf"
    HALFLING = "Halfling"
    # Add more races as needed


@dataclass
class Attribute:
    """A character attribute (Agility, Smarts, Spirit, Strength, Vigor)."""
    name: str
    die_type: DieType
    
    def __post_init__(self):
        # Attributes start at d4 minimum
        if self.die_type.value < 4:
            self.die_type = DieType.D4
    
    def __str__(self):
        return f"{self.name}: {self.die_type}"


@dataclass 
class Skill:
    """A character skill linked to an attribute."""
    name: str
    linked_attribute: str  # Name of the linked attribute
    die_type: DieType
    specialization: Optional[str] = None
    
    def __str__(self):
        spec_str = f" ({self.specialization})" if self.specialization else ""
        return f"{self.name}{spec_str}: {self.die_type}"


@dataclass
class Edge:
    """A character edge (advantage/feat)."""
    name: str
    description: str
    requirements: List[str] = field(default_factory=list)
    
    def __str__(self):
        return f"{self.name}: {self.description}"


@dataclass
class Hindrance:
    """A character hindrance (disadvantage)."""
    name: str
    description: str
    severity: str  # "Minor" or "Major"
    
    def __str__(self):
        return f"{self.name} ({self.severity}): {self.description}"


@dataclass
class Gear:
    """Equipment and gear."""
    name: str
    description: str = ""
    weight: float = 0.0
    cost: int = 0
    
    def __str__(self):
        return f"{self.name} - {self.description}"


@dataclass
class Character:
    """A Savage Worlds character."""
    name: str
    player_name: str = ""
    race: Race = Race.HUMAN
    concept: str = ""  # Character concept/description
    
    # Core attributes
    attributes: Dict[str, Attribute] = field(default_factory=lambda: {
        "Agility": Attribute("Agility", DieType.D4),
        "Smarts": Attribute("Smarts", DieType.D4), 
        "Spirit": Attribute("Spirit", DieType.D4),
        "Strength": Attribute("Strength", DieType.D4),
        "Vigor": Attribute("Vigor", DieType.D4)
    })
    
    skills: Dict[str, Skill] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    hindrances: List[Hindrance] = field(default_factory=list)
    
    # Equipment
    weapons: List[Weapon] = field(default_factory=list)
    armor: List[Armor] = field(default_factory=list)
    equipment: List[Equipment] = field(default_factory=list)
    
    # Legacy gear field (keeping for backward compatibility)
    gear: List[Gear] = field(default_factory=list)
    
    # Derived stats
    pace: int = 6
    parry: int = 2  # Base parry, will be calculated from Fighting skill
    toughness: int = 2  # Base toughness, will be calculated from Vigor
    charisma: int = 0  # Modifier from edges/hindrances
    
    # Resources
    bennies: int = 3  # Starting bennies
    current_wounds: int = 0
    current_fatigue: int = 0
    
    # Character creation points
    attribute_points_spent: int = 0
    skill_points_spent: int = 0
    
    def get_attribute_die(self, attribute_name: str) -> DieType:
        """Get the die type for an attribute."""
        if attribute_name in self.attributes:
            return self.attributes[attribute_name].die_type
        return DieType.D4
    
    def get_skill_die(self, skill_name: str) -> DieType:
        """Get the die type for a skill."""
        if skill_name in self.skills:
            return self.skills[skill_name].die_type
        return DieType.D4  # Unskilled is d4-2
    
    def add_skill(self, skill_name: str, linked_attribute: str, die_type: DieType = DieType.D4, specialization: Optional[str] = None):
        """Add a skill to the character."""
        self.skills[skill_name] = Skill(skill_name, linked_attribute, die_type, specialization)
    
    def calculate_derived_stats(self):
        """Calculate derived statistics like Parry and Toughness."""
        # Parry = 2 + half Fighting skill die
        fighting_die = self.get_skill_die("Fighting")
        base_parry = 2 + (fighting_die.value // 2)
        
        # Add weapon and shield bonuses to Parry
        weapon_parry_bonus = 0
        shield_parry_bonus = 0
        
        for weapon in self.weapons:
            weapon_parry_bonus += weapon.parry_modifier
            
        for armor_piece in self.armor:
            shield_parry_bonus += armor_piece.parry_bonus
            
        self.parry = base_parry + weapon_parry_bonus + shield_parry_bonus
        
        # Toughness = 2 + half Vigor die + armor
        vigor_die = self.get_attribute_die("Vigor")
        base_toughness = 2 + (vigor_die.value // 2)
        
        # Add armor bonus
        armor_bonus = 0
        for armor_piece in self.armor:
            armor_bonus += armor_piece.armor_bonus
            
        self.toughness = base_toughness + armor_bonus
    
    def add_weapon(self, weapon: Weapon):
        """Add a weapon to the character."""
        self.weapons.append(weapon)
        
    def add_armor(self, armor: Armor):
        """Add armor to the character."""
        self.armor.append(armor)
        
    def add_equipment(self, equipment: Equipment):
        """Add equipment to the character."""
        self.equipment.append(equipment)
        
    def remove_weapon(self, weapon_name: str) -> bool:
        """Remove a weapon by name. Returns True if found and removed."""
        for i, weapon in enumerate(self.weapons):
            if weapon.name == weapon_name:
                del self.weapons[i]
                return True
        return False
        
    def remove_armor(self, armor_name: str) -> bool:
        """Remove armor by name. Returns True if found and removed."""
        for i, armor in enumerate(self.armor):
            if armor.name == armor_name:
                del self.armor[i]
                return True
        return False
        
    def remove_equipment(self, equipment_name: str) -> bool:
        """Remove equipment by name. Returns True if found and removed."""
        for i, equipment in enumerate(self.equipment):
            if equipment.name == equipment_name:
                del self.equipment[i]
                return True
        return False
    
    def get_combat_stats(self) -> CombatStats:
        """Get calculated combat statistics."""
        # Total armor from all worn armor
        total_armor = sum(armor.armor_bonus for armor in self.armor)
        
        # Total toughness (base + vigor + armor)
        vigor_die = self.get_attribute_die("Vigor")
        base_toughness = 2 + (vigor_die.value // 2)
        total_toughness = base_toughness + total_armor
        
        # Total parry (base + fighting + weapon/shield bonuses)
        fighting_die = self.get_skill_die("Fighting")
        base_parry = 2 + (fighting_die.value // 2)
        
        weapon_parry_bonus = sum(weapon.parry_modifier for weapon in self.weapons)
        shield_parry_bonus = sum(armor.parry_bonus for armor in self.armor)
        total_parry = base_parry + weapon_parry_bonus + shield_parry_bonus
        
        # Encumbrance (simplified - could be enhanced)
        total_weight = (sum(weapon.weight or 0 for weapon in self.weapons) + 
                       sum(armor.weight or 0 for armor in self.armor) +
                       sum((equipment.weight or 0) * equipment.quantity for equipment in self.equipment))
        
        # Basic encumbrance rule: Strength die value * 5 = max carry without penalty
        strength_die = self.get_attribute_die("Strength")
        max_weight = strength_die.value * 5
        encumbrance_penalty = max(0, int((total_weight - max_weight) // 10))
        
        # Primary/secondary weapons (first two weapons)
        primary_weapon = self.weapons[0] if len(self.weapons) > 0 else None
        secondary_weapon = self.weapons[1] if len(self.weapons) > 1 else None
        
        return CombatStats(
            total_armor=total_armor,
            total_toughness=total_toughness,
            total_parry=total_parry,
            encumbrance_penalty=encumbrance_penalty,
            primary_weapon=primary_weapon,
            secondary_weapon=secondary_weapon
        )
    
    def __str__(self):
        return f"{self.name} ({self.race.value}) - {self.concept}"