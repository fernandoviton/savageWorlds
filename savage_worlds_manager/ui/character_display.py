"""
Character sheet display formatting for CLI output.
"""

from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

from ..models.character import Character


class CharacterSheet:
    """Formats and displays character information."""
    
    def __init__(self):
        self.console = Console()
    
    def display_character(self, character: Character):
        """Display a complete character sheet."""
        
        # Character header
        header = self._create_header(character)
        
        # Attributes and derived stats
        attributes_panel = self._create_attributes_panel(character)
        derived_panel = self._create_derived_stats_panel(character)
        
        # Skills 
        skills_panel = self._create_skills_panel(character)
        
        # Edges and Hindrances
        edges_panel = self._create_edges_panel(character)
        hindrances_panel = self._create_hindrances_panel(character)
        
        # Equipment
        weapons_panel = self._create_weapons_panel(character)
        armor_panel = self._create_armor_panel(character)
        equipment_panel = self._create_equipment_panel(character)
        
        # Display everything
        self.console.print(header)
        self.console.print()
        
        # Two column layout for main stats
        self.console.print(Columns([attributes_panel, derived_panel], equal=True, expand=True))
        self.console.print()
        
        self.console.print(skills_panel)
        self.console.print()
        
        # Two column layout for edges/hindrances
        self.console.print(Columns([edges_panel, hindrances_panel], equal=True, expand=True))
        self.console.print()
        
        # Three column layout for equipment
        self.console.print(Columns([weapons_panel, armor_panel, equipment_panel], equal=True, expand=True))
    
    def _create_header(self, character: Character) -> Panel:
        """Create the character header panel."""
        title = f"[bold cyan]{character.name}[/bold cyan]"
        if character.player_name:
            title += f" (Player: {character.player_name})"
        
        subtitle = f"[italic]{character.race.value}[/italic]"
        if character.concept:
            subtitle += f" - {character.concept}"
            
        return Panel(
            f"{title}\n{subtitle}",
            title="Character",
            border_style="cyan"
        )
    
    def _create_attributes_panel(self, character: Character) -> Panel:
        """Create the attributes panel."""
        table = Table(show_header=True, header_style="bold magenta", box=None)
        table.add_column("Attribute", style="cyan")
        table.add_column("Die", justify="center")
        
        for attr_name, attribute in character.attributes.items():
            table.add_row(attr_name, str(attribute.die_type))
        
        return Panel(
            table,
            title="Attributes",
            border_style="magenta"
        )
    
    def _create_derived_stats_panel(self, character: Character) -> Panel:
        """Create the derived statistics panel."""
        table = Table(show_header=True, header_style="bold green", box=None)
        table.add_column("Stat", style="green")
        table.add_column("Value", justify="center")
        
        # Get combat stats
        combat_stats = character.get_combat_stats()
        
        table.add_row("Pace", str(character.pace))
        table.add_row("Parry", str(combat_stats.total_parry))
        table.add_row("Toughness", str(combat_stats.total_toughness))
        
        # Show armor breakdown if any
        if combat_stats.total_armor > 0:
            base_toughness = combat_stats.total_toughness - combat_stats.total_armor
            table.add_row("  Base", str(base_toughness))
            table.add_row("  +Armor", f"+{combat_stats.total_armor}")
        
        table.add_row("Charisma", f"{character.charisma:+d}" if character.charisma != 0 else "0")
        table.add_row("Bennies", str(character.bennies))
        table.add_row("Wounds", f"{character.current_wounds}/3")
        table.add_row("Fatigue", f"{character.current_fatigue}/2")
        
        # Show encumbrance if applicable
        if combat_stats.encumbrance_penalty > 0:
            table.add_row("Encumbrance", f"-{combat_stats.encumbrance_penalty}")
        
        return Panel(
            table,
            title="Derived Stats",
            border_style="green"
        )
    
    def _create_skills_panel(self, character: Character) -> Panel:
        """Create the skills panel."""
        if not character.skills:
            return Panel(
                "[dim]No skills learned[/dim]",
                title="Skills",
                border_style="yellow"
            )
        
        table = Table(show_header=True, header_style="bold yellow", box=None)
        table.add_column("Skill", style="yellow")
        table.add_column("Die", justify="center")
        table.add_column("Attribute", style="dim")
        table.add_column("Specialization", style="dim")
        
        for skill_name, skill in sorted(character.skills.items()):
            specialization = skill.specialization if skill.specialization else ""
            table.add_row(
                skill_name, 
                str(skill.die_type),
                skill.linked_attribute,
                specialization
            )
        
        return Panel(
            table,
            title="Skills",
            border_style="yellow"
        )
    
    def _create_edges_panel(self, character: Character) -> Panel:
        """Create the edges panel."""
        if not character.edges:
            content = "[dim]No edges[/dim]"
        else:
            content = ""
            for edge in character.edges:
                content += f"[bold green]{edge.name}[/bold green]\n"
                content += f"[dim]{edge.description}[/dim]\n\n"
            content = content.rstrip()
        
        return Panel(
            content,
            title="Edges",
            border_style="green"
        )
    
    def _create_hindrances_panel(self, character: Character) -> Panel:
        """Create the hindrances panel."""
        if not character.hindrances:
            content = "[dim]No hindrances[/dim]"
        else:
            content = ""
            for hindrance in character.hindrances:
                severity_color = "red" if hindrance.severity == "Major" else "orange3"
                content += f"[bold {severity_color}]{hindrance.name}[/bold {severity_color}] ({hindrance.severity})\n"
                content += f"[dim]{hindrance.description}[/dim]\n\n"
            content = content.rstrip()
        
        return Panel(
            content,
            title="Hindrances", 
            border_style="red"
        )
    
    def _create_weapons_panel(self, character: Character) -> Panel:
        """Create the weapons panel."""
        if not character.weapons:
            content = "[dim]No weapons[/dim]"
        else:
            content = ""
            for weapon in character.weapons:
                content += f"[bold cyan]{weapon.name}[/bold cyan]\n"
                content += f"Damage: {weapon.damage}"
                
                if weapon.weapon_type.value == "Ranged":
                    content += f"\nRange: {weapon.range_short}/{weapon.range_medium}/{weapon.range_long}"
                elif weapon.weapon_type.value == "Melee" and weapon.parry_modifier != 0:
                    content += f", Parry {weapon.parry_modifier:+d}"
                
                if weapon.special_rules:
                    content += f"\n[italic]{', '.join(weapon.special_rules)}[/italic]"
                
                content += "\n\n"
            content = content.rstrip()
        
        return Panel(
            content,
            title="Weapons",
            border_style="red"
        )
    
    def _create_armor_panel(self, character: Character) -> Panel:
        """Create the armor panel."""
        if not character.armor:
            content = "[dim]No armor[/dim]"
        else:
            content = ""
            total_armor = 0
            total_parry_bonus = 0
            
            for armor in character.armor:
                content += f"[bold blue]{armor.name}[/bold blue]\n"
                content += f"Armor: +{armor.armor_bonus}"
                
                if armor.parry_bonus > 0:
                    content += f", Parry +{armor.parry_bonus}"
                    total_parry_bonus += armor.parry_bonus
                
                total_armor += armor.armor_bonus
                
                if armor.special_rules:
                    content += f"\n[italic]{', '.join(armor.special_rules)}[/italic]"
                
                content += "\n\n"
            
            # Add totals
            content += f"[bold]Total Armor: +{total_armor}[/bold]"
            if total_parry_bonus > 0:
                content += f"\n[bold]Total Parry Bonus: +{total_parry_bonus}[/bold]"
        
        return Panel(
            content,
            title="Armor & Shields",
            border_style="blue"
        )
    
    def _create_equipment_panel(self, character: Character) -> Panel:
        """Create the equipment panel."""
        if not character.equipment and not character.gear:
            content = "[dim]No equipment[/dim]"
        else:
            content = ""
            
            # New equipment system
            for equipment in character.equipment:
                qty_str = f" x{equipment.quantity}" if equipment.quantity > 1 else ""
                content += f"[yellow]{equipment.name}{qty_str}[/yellow]\n"
                if equipment.description:
                    content += f"[dim]{equipment.description}[/dim]\n"
                if equipment.notes:
                    content += f"[italic]{equipment.notes}[/italic]\n"
                content += "\n"
            
            # Legacy gear system (for backward compatibility)
            for gear in character.gear:
                content += f"[yellow]{gear.name}[/yellow]\n"
                if gear.description:
                    content += f"[dim]{gear.description}[/dim]\n"
                content += "\n"
                
            content = content.rstrip()
        
        return Panel(
            content,
            title="Equipment",
            border_style="yellow"
        )
    
    def display_creation_summary(self, character: Character, attribute_points_available: int, skill_points_available: int):
        """Display character creation progress."""
        
        # Points summary
        attr_used = character.attribute_points_spent
        attr_remaining = attribute_points_available - attr_used
        
        skill_used = character.skill_points_spent  
        skill_remaining = skill_points_available - skill_used
        
        points_table = Table(show_header=True, header_style="bold blue", box=None)
        points_table.add_column("Resource", style="blue")
        points_table.add_column("Used", justify="center")
        points_table.add_column("Available", justify="center") 
        points_table.add_column("Remaining", justify="center")
        
        attr_style = "red" if attr_remaining < 0 else "green" if attr_remaining == 0 else "yellow"
        skill_style = "red" if skill_remaining < 0 else "green" if skill_remaining == 0 else "yellow"
        
        points_table.add_row(
            "Attribute Points",
            str(attr_used),
            str(attribute_points_available),
            f"[{attr_style}]{attr_remaining}[/{attr_style}]"
        )
        points_table.add_row(
            "Skill Points", 
            str(skill_used),
            str(skill_points_available),
            f"[{skill_style}]{skill_remaining}[/{skill_style}]"
        )
        
        points_panel = Panel(
            points_table,
            title="Character Creation Progress",
            border_style="blue"
        )
        
        self.console.print(points_panel)
        self.console.print()
        
        # Show basic character info
        self.display_character(character)