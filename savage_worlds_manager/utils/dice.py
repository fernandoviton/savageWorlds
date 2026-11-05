"""
Dice system for Savage Worlds mechanics.
"""

from enum import Enum
from typing import List, Tuple
import random


class DieType(Enum):
    """Represents the different die types in Savage Worlds."""
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    
    def __str__(self):
        return f"d{self.value}"
    
    def __repr__(self):
        return f"DieType.{self.name}"


class DiceRoll:
    """Represents a dice roll with acing (exploding dice) mechanics."""
    
    def __init__(self, die_type: DieType, modifier: int = 0):
        self.die_type = die_type
        self.modifier = modifier
        self.rolls: List[int] = []
        self.total = 0
        self.aced = False  # Track if any dice aced
        
    def roll(self) -> int:
        """Roll the die with acing mechanics."""
        self.rolls = []
        self.aced = False
        
        current_roll = random.randint(1, self.die_type.value)
        self.rolls.append(current_roll)
        
        # Acing: if we roll the maximum, roll again and add
        while current_roll == self.die_type.value:
            self.aced = True
            current_roll = random.randint(1, self.die_type.value)
            self.rolls.append(current_roll)
            
        self.total = sum(self.rolls) + self.modifier
        return self.total
    
    def is_success(self, target_number: int = 4) -> bool:
        """Check if the roll meets or exceeds the target number."""
        return self.total >= target_number
    
    def is_raise(self, target_number: int = 4) -> bool:
        """Check if the roll achieves a raise (4+ over target)."""
        return self.total >= target_number + 4
    
    def get_raises(self, target_number: int = 4) -> int:
        """Get the number of raises achieved."""
        if not self.is_success(target_number):
            return 0
        return (self.total - target_number) // 4
    
    def __str__(self):
        if not self.rolls:
            modifier_str = f"{'+' + str(self.modifier) if self.modifier > 0 else str(self.modifier) if self.modifier < 0 else ''}"
            return f"{self.die_type}{modifier_str}"
        
        rolls_str = "+".join(str(roll) for roll in self.rolls)
        modifier_str = f"{'+' + str(self.modifier) if self.modifier > 0 else str(self.modifier) if self.modifier < 0 else ''}"
        ace_indicator = " (ACED!)" if self.aced else ""
        return f"{self.die_type}[{rolls_str}]{modifier_str} = {self.total}{ace_indicator}"


def roll_trait_test(trait_die: DieType, wild_die: DieType = DieType.D6, modifier: int = 0) -> Tuple[int, DiceRoll, DiceRoll]:
    """
    Roll a trait test with trait die and wild die, returning the higher result.
    
    Args:
        trait_die: The character's trait die
        wild_die: The wild die (usually d6)
        modifier: Modifier to add to both rolls
        
    Returns:
        Tuple of (best_total, trait_roll, wild_roll)
    """
    trait_roll = DiceRoll(trait_die, modifier)
    wild_roll = DiceRoll(wild_die, modifier)
    
    trait_total = trait_roll.roll()
    wild_total = wild_roll.roll()
    
    best_total = max(trait_total, wild_total)
    
    return best_total, trait_roll, wild_roll


def make_skill_check(skill_die: DieType, target_number: int, modifier: int = 0) -> Tuple[bool, int, DiceRoll, DiceRoll]:
    """
    Make a skill check against a target number.
    
    Args:
        skill_die: The skill die type
        target_number: The target number to beat
        modifier: Modifier to add to the roll
        
    Returns:
        Tuple of (success, raises, skill_roll, wild_roll)
    """
    best_total, skill_roll, wild_roll = roll_trait_test(skill_die, DieType.D6, modifier)
    
    success = best_total >= target_number
    raises = max(0, (best_total - target_number) // 4) if success else 0
    
    return success, raises, skill_roll, wild_roll


def roll_damage(damage_die: DieType, modifier: int = 0, num_dice: int = 1) -> Tuple[int, List[DiceRoll]]:
    """
    Roll damage dice (no wild die).
    
    Args:
        damage_die: Type of damage die
        modifier: Modifier to add to total
        num_dice: Number of dice to roll
        
    Returns:
        Tuple of (total_damage, list_of_rolls)
    """
    rolls = []
    total_damage = 0
    
    for _ in range(num_dice):
        roll = DiceRoll(damage_die, 0)  # No modifier on individual dice
        roll.roll()
        rolls.append(roll)
        total_damage += roll.total
    
    total_damage += modifier
    return total_damage, rolls


def roll_opposed_test(attacker_die: DieType, defender_die: DieType, 
                     attacker_mod: int = 0, defender_mod: int = 0) -> Tuple[str, DiceRoll, DiceRoll, DiceRoll, DiceRoll]:
    """
    Roll an opposed test between two characters.
    
    Args:
        attacker_die: Attacker's trait die
        defender_die: Defender's trait die  
        attacker_mod: Attacker's modifier
        defender_mod: Defender's modifier
        
    Returns:
        Tuple of (result, attacker_trait, attacker_wild, defender_trait, defender_wild)
        Result is "attacker_wins", "defender_wins", or "tie"
    """
    # Attacker rolls
    attacker_total, attacker_trait, attacker_wild = roll_trait_test(attacker_die, DieType.D6, attacker_mod)
    
    # Defender rolls
    defender_total, defender_trait, defender_wild = roll_trait_test(defender_die, DieType.D6, defender_mod)
    
    # Determine winner
    if attacker_total > defender_total:
        result = "attacker_wins"
    elif defender_total > attacker_total:
        result = "defender_wins"
    else:
        result = "tie"
    
    return result, attacker_trait, attacker_wild, defender_trait, defender_wild


def roll_soak_damage(vigor_die: DieType, modifier: int = 0) -> Tuple[bool, DiceRoll, DiceRoll]:
    """
    Roll to soak damage using Vigor.
    
    Args:
        vigor_die: Character's Vigor die
        modifier: Modifier (usually from edges like Hard to Kill)
        
    Returns:
        Tuple of (success, vigor_roll, wild_roll)
        Success is True if any wound was soaked
    """
    total, vigor_roll, wild_roll = roll_trait_test(vigor_die, DieType.D6, modifier)
    
    # Need 4+ to soak a wound, each raise soaks an additional wound
    success = total >= 4
    
    return success, vigor_roll, wild_roll


def roll_initiative() -> int:
    """
    Roll initiative (standard playing card draw simulation).
    Returns a value from 1-13 where:
    - 1-10 = number cards
    - 11 = Jack, 12 = Queen, 13 = King, 14 = Ace
    - Jokers would be 15-16 but aren't implemented here
    """
    return random.randint(1, 14)


# Predefined target numbers for common tasks
class TargetNumber:
    TRIVIAL = 2
    EASY = 4
    MODERATE = 6
    HARD = 8
    VERY_HARD = 10
    HEROIC = 12
    LEGENDARY = 14
    
    @classmethod
    def get_description(cls, tn: int) -> str:
        """Get a description for a target number."""
        descriptions = {
            2: "Trivial",
            4: "Easy", 
            6: "Moderate",
            8: "Hard",
            10: "Very Hard", 
            12: "Heroic",
            14: "Legendary"
        }
        return descriptions.get(tn, f"TN {tn}")


def make_skill_check(skill_die: DieType, target_number: int = 4, modifier: int = 0) -> Tuple[bool, int, DiceRoll, DiceRoll]:
    """
    Make a skill check against a target number.
    
    Args:
        skill_die: The skill's die type
        target_number: Target number to beat
        modifier: Modifier to the roll
        
    Returns:
        Tuple of (success, raises, skill_roll, wild_roll)
    """
    total, skill_roll, wild_roll = roll_trait_test(skill_die, DieType.D6, modifier)
    
    success = total >= target_number
    raises = (total - target_number) // 4 if success else 0
    
    return success, raises, skill_roll, wild_roll