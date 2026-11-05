"""
Equipment data models for Savage Worlds (weapons, armor, and gear).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class WeaponType(Enum):
    """Types of weapons in Savage Worlds."""
    MELEE = "Melee"
    RANGED = "Ranged"
    THROWN = "Thrown"


class ArmorType(Enum):
    """Types of armor coverage."""
    BODY = "Body"  # Torso armor
    HEAD = "Head"  # Helmet
    LIMBS = "Limbs"  # Arm/leg protection
    SHIELD = "Shield"  # Shield (adds to Parry)


@dataclass
class Weapon:
    """A weapon with Savage Worlds stats."""
    name: str
    weapon_type: WeaponType
    damage: str  # e.g., "Str+d6", "2d6", "1d4+1"
    description: str = ""
    
    # Melee weapon stats
    reach: int = 0  # Additional reach in inches
    parry_modifier: int = 0  # Modifier to Parry when using this weapon
    
    # Ranged weapon stats
    range_short: int = 0  # Short range in inches
    range_medium: int = 0  # Medium range in inches  
    range_long: int = 0  # Long range in inches
    rate_of_fire: int = 1  # Shots per action
    shots: Optional[int] = None  # Ammo capacity (None = unlimited like bow)
    
    # General stats
    weight: float = 0.0  # Weight in pounds
    cost: int = 0  # Cost in dollars/credits
    min_strength: Optional[str] = None  # Minimum Strength die (e.g., "d6")
    
    # Special notes
    special_rules: List[str] = field(default_factory=list)  # AP 2, Heavy Weapon, etc.
    
    def __str__(self):
        if self.weapon_type == WeaponType.MELEE:
            return f"{self.name} ({self.damage}, Parry {self.parry_modifier:+d})"
        elif self.weapon_type == WeaponType.RANGED:
            return f"{self.name} ({self.damage}, {self.range_short}/{self.range_medium}/{self.range_long})"
        else:
            return f"{self.name} ({self.damage})"


@dataclass
class Armor:
    """Armor with Savage Worlds protection stats."""
    name: str
    armor_type: ArmorType
    armor_bonus: int  # Armor bonus vs damage
    description: str = ""
    
    # Coverage areas
    covers_torso: bool = True
    covers_arms: bool = False
    covers_legs: bool = False
    covers_head: bool = False
    
    # Special properties
    parry_bonus: int = 0  # For shields
    toughness_bonus: int = 0  # Additional toughness bonus
    
    # Physical properties
    weight: float = 0.0
    cost: int = 0
    min_strength: Optional[str] = None
    
    # Special rules
    special_rules: List[str] = field(default_factory=list)  # Heavy Armor, etc.
    
    def __str__(self):
        if self.armor_type == ArmorType.SHIELD:
            return f"{self.name} (+{self.armor_bonus} Armor, +{self.parry_bonus} Parry)"
        else:
            return f"{self.name} (+{self.armor_bonus} Armor)"


@dataclass
class Equipment:
    """General equipment/gear item."""
    name: str
    description: str = ""
    weight: float = 0.0
    cost: int = 0
    quantity: int = 1
    notes: str = ""
    
    def __str__(self):
        qty_str = f" x{self.quantity}" if self.quantity > 1 else ""
        return f"{self.name}{qty_str} - {self.description}"


@dataclass
class CombatStats:
    """Calculated combat statistics for a character."""
    total_armor: int = 0  # Total armor bonus
    total_toughness: int = 0  # Toughness including armor
    total_parry: int = 0  # Parry including weapon/shield bonuses
    encumbrance_penalty: int = 0  # Penalty from carrying too much
    
    # Weapon ready status
    primary_weapon: Optional[Weapon] = None
    secondary_weapon: Optional[Weapon] = None
    
    def __str__(self):
        return f"Armor: {self.total_armor}, Toughness: {self.total_toughness}, Parry: {self.total_parry}"