"""
Character creation system for Savage Worlds.
Handles point allocation, validation, and character generation rules.
"""

from typing import Dict, List, Optional, Tuple
from ..models.character import Character, Race, Attribute, Skill, Edge, Hindrance
from ..utils.dice import DieType
from ..data.game_data import COMMON_EDGES, COMMON_HINDRANCES, SKILL_LIST


class CharacterCreationError(Exception):
    """Exception raised during character creation validation."""
    pass


class CharacterCreator:
    """Handles character creation with Savage Worlds rules."""
    
    # Starting points for new characters
    STARTING_ATTRIBUTE_POINTS = 5
    STARTING_SKILL_POINTS = 15
    MAX_HINDRANCES = 4  # 1 Major + 2 Minor, or 4 Minor
    
    def __init__(self):
        self.character: Optional[Character] = None
    
    def create_new_character(self, name: str, player_name: str = "", race: Race = Race.HUMAN, concept: str = "") -> Character:
        """Create a new character with default values."""
        self.character = Character(
            name=name,
            player_name=player_name,
            race=race,
            concept=concept
        )
        return self.character
    
    def get_attribute_cost(self, current_die: DieType, target_die: DieType) -> int:
        """Calculate the cost to raise an attribute from current to target level."""
        if target_die.value <= current_die.value:
            return 0
            
        cost = 0
        current_value = current_die.value
        
        while current_value < target_die.value:
            if current_value == 4:  # d4 to d6
                cost += 1
                current_value = 6
            elif current_value == 6:  # d6 to d8  
                cost += 1
                current_value = 8
            elif current_value == 8:  # d8 to d10
                cost += 1
                current_value = 10
            elif current_value == 10:  # d10 to d12
                cost += 1
                current_value = 12
            elif current_value == 12:  # d12 to d12+1, d12+2, etc.
                cost += 1
                current_value += 1
            else:
                break
                
        return cost
    
    def get_skill_cost(self, current_die: DieType, target_die: DieType, attribute_die: DieType) -> int:
        """
        Calculate the cost to raise a skill from current to target level.
        Skills cannot exceed their linked attribute.
        """
        if target_die.value > attribute_die.value:
            raise CharacterCreationError(f"Skill cannot exceed linked attribute ({attribute_die})")
            
        if target_die.value <= current_die.value:
            return 0
            
        cost = 0
        current_value = current_die.value
        
        while current_value < target_die.value:
            if current_value == 4:  # d4 to d6
                cost += 1
                current_value = 6
            elif current_value == 6:  # d6 to d8
                cost += 1
                current_value = 8
            elif current_value == 8:  # d8 to d10
                cost += 2  # Skills cost 2 points from d8 to d10
                current_value = 10
            elif current_value == 10:  # d10 to d12
                cost += 2  # Skills cost 2 points from d10 to d12
                current_value = 12
            else:
                break
                
        return cost
    
    def set_attribute(self, attribute_name: str, die_type: DieType) -> bool:
        """Set an attribute die type and update point costs."""
        if not self.character:
            raise CharacterCreationError("No character created")
            
        if attribute_name not in self.character.attributes:
            raise CharacterCreationError(f"Unknown attribute: {attribute_name}")
            
        current_die = self.character.attributes[attribute_name].die_type
        cost = self.get_attribute_cost(current_die, die_type)
        
        # Check if we have enough points
        new_total = self.character.attribute_points_spent + cost
        if new_total > self.STARTING_ATTRIBUTE_POINTS:
            raise CharacterCreationError(f"Not enough attribute points. Would need {new_total}, have {self.STARTING_ATTRIBUTE_POINTS}")
        
        # Update attribute and points
        self.character.attributes[attribute_name].die_type = die_type
        self.character.attribute_points_spent = new_total
        
        return True
    
    def set_skill(self, skill_name: str, die_type: DieType, specialization: Optional[str] = None) -> bool:
        """Set a skill die type and update point costs."""
        if not self.character:
            raise CharacterCreationError("No character created")
            
        if skill_name not in SKILL_LIST:
            raise CharacterCreationError(f"Unknown skill: {skill_name}")
            
        linked_attribute = SKILL_LIST[skill_name]
        attribute_die = self.character.get_attribute_die(linked_attribute)
        
        # Get current skill level
        current_die = self.character.get_skill_die(skill_name) if skill_name in self.character.skills else DieType.D4
        
        cost = self.get_skill_cost(current_die, die_type, attribute_die)
        
        # Check if we have enough points
        new_total = self.character.skill_points_spent + cost
        if new_total > self.STARTING_SKILL_POINTS:
            raise CharacterCreationError(f"Not enough skill points. Would need {new_total}, have {self.STARTING_SKILL_POINTS}")
        
        # Add or update skill
        self.character.add_skill(skill_name, linked_attribute, die_type, specialization)
        self.character.skill_points_spent = new_total
        
        return True
    
    def add_edge(self, edge_name: str) -> bool:
        """Add an edge to the character."""
        if not self.character:
            raise CharacterCreationError("No character created")
            
        # Find the edge in available edges
        edge = None
        for available_edge in COMMON_EDGES:
            if available_edge.name == edge_name:
                edge = available_edge
                break
                
        if not edge:
            raise CharacterCreationError(f"Unknown edge: {edge_name}")
            
        # TODO: Check requirements
        # For now, just add the edge
        self.character.edges.append(edge)
        return True
    
    def add_hindrance(self, hindrance_name: str) -> bool:
        """Add a hindrance to the character."""
        if not self.character:
            raise CharacterCreationError("No character created")
            
        # Find the hindrance
        hindrance = None
        for available_hindrance in COMMON_HINDRANCES:
            if available_hindrance.name == hindrance_name:
                hindrance = available_hindrance
                break
                
        if not hindrance:
            raise CharacterCreationError(f"Unknown hindrance: {hindrance_name}")
            
        # Check hindrance limits
        major_count = sum(1 for h in self.character.hindrances if h.severity == "Major")
        minor_count = sum(1 for h in self.character.hindrances if h.severity == "Minor") 
        
        if hindrance.severity == "Major":
            if major_count >= 1:
                raise CharacterCreationError("Cannot have more than 1 Major hindrance")
            if minor_count + major_count * 2 >= self.MAX_HINDRANCES:
                raise CharacterCreationError("Too many hindrances (max 4 points: Major=2, Minor=1)")
        else:  # Minor
            if minor_count + major_count * 2 >= self.MAX_HINDRANCES:
                raise CharacterCreationError("Too many hindrances (max 4 points: Major=2, Minor=1)")
        
        self.character.hindrances.append(hindrance)
        return True
    
    def get_hindrance_bonus_points(self) -> Tuple[int, int]:
        """
        Calculate bonus points from hindrances.
        Returns (attribute_points, skill_points).
        """
        if not self.character:
            return 0, 0
            
        total_hindrance_points = 0
        for hindrance in self.character.hindrances:
            if hindrance.severity == "Major":
                total_hindrance_points += 2
            else:
                total_hindrance_points += 1
                
        # Each hindrance point can be used for:
        # - 1 attribute point
        # - 2 skill points  
        # - 1 edge (not implemented yet)
        
        # For now, assume all go to skill points
        return 0, total_hindrance_points * 2
    
    def validate_character(self) -> List[str]:
        """Validate the character and return any errors."""
        if not self.character:
            return ["No character created"]
            
        errors = []
        
        # Check attribute points
        if self.character.attribute_points_spent > self.STARTING_ATTRIBUTE_POINTS:
            errors.append(f"Too many attribute points spent: {self.character.attribute_points_spent}/{self.STARTING_ATTRIBUTE_POINTS}")
        
        # Check skill points (including hindrance bonuses)
        _, bonus_skill_points = self.get_hindrance_bonus_points()
        max_skill_points = self.STARTING_SKILL_POINTS + bonus_skill_points
        
        if self.character.skill_points_spent > max_skill_points:
            errors.append(f"Too many skill points spent: {self.character.skill_points_spent}/{max_skill_points}")
        
        # Check skills don't exceed attributes
        for skill_name, skill in self.character.skills.items():
            attr_die = self.character.get_attribute_die(skill.linked_attribute)
            if skill.die_type.value > attr_die.value:
                errors.append(f"Skill {skill_name} ({skill.die_type}) exceeds attribute {skill.linked_attribute} ({attr_die})")
        
        return errors
    
    def finalize_character(self) -> Character:
        """Finalize the character by calculating derived stats."""
        if not self.character:
            raise CharacterCreationError("No character created")
            
        errors = self.validate_character()
        if errors:
            raise CharacterCreationError("Character validation failed:\n" + "\n".join(errors))
            
        self.character.calculate_derived_stats()
        return self.character