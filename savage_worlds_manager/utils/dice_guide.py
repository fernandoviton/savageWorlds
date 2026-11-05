"""
Savage Worlds dice rolling guidance system.
Provides recommendations for what dice to roll in various situations without actually rolling.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RollType(Enum):
    """Types of dice rolls in Savage Worlds."""
    TRAIT_TEST = "Trait Test"
    DAMAGE = "Damage"
    HEALING = "Healing"
    FEAR = "Fear Check"
    SOAK = "Soak Roll"
    VIGOR = "Vigor Roll"
    INITIATIVE = "Initiative"
    RAISE_DAMAGE = "Raise Damage"
    WILD_ATTACK = "Wild Attack"
    CALLED_SHOT = "Called Shot"
    GANG_UP = "Gang Up"
    MULTI_ACTION = "Multi-Action"


@dataclass
class DiceGuidance:
    """Guidance for what dice to roll in a specific situation."""
    situation: str
    dice_to_roll: str
    modifiers: List[str]
    target_number: Optional[int]
    special_rules: List[str]
    examples: List[str]


class SavageWorldsDiceGuide:
    """Comprehensive dice rolling guidance for Savage Worlds."""
    
    def __init__(self):
        self.guidance_db = self._build_guidance_database()
    
    def _build_guidance_database(self) -> Dict[str, DiceGuidance]:
        """Build the comprehensive guidance database."""
        return {
            # Trait Tests
            "trait_test": DiceGuidance(
                situation="Basic Trait Test",
                dice_to_roll="Trait Die + Wild Die (if Wild Card)",
                modifiers=[
                    "+2 for good conditions/equipment",
                    "-2 for poor conditions/distractions",
                    "-4 for terrible conditions",
                    "+1 per ally helping (max +4)"
                ],
                target_number=4,
                special_rules=[
                    "Take highest of Trait Die and Wild Die",
                    "Raise = every 4 points above TN",
                    "Snake Eyes (1 on both dice) = Critical Failure"
                ],
                examples=[
                    "Fighting d8 + Wild Die vs Parry",
                    "Shooting d10 + Wild Die vs 4 (or Range)",
                    "Athletics d6 + Wild Die vs 4 for climbing"
                ]
            ),
            
            "fighting": DiceGuidance(
                situation="Fighting (Melee Attack)",
                dice_to_roll="Fighting Skill + Wild Die",
                modifiers=[
                    "Target's Parry = base difficulty",
                    "+2 if target is prone/bound/grappled",
                    "+1 per ally adjacent to target (Gang Up)",
                    "-2 if attacker is prone",
                    "-2 for off-hand weapon",
                    "-4 for called shot (specific body part)"
                ],
                target_number=None,  # Variable based on Parry
                special_rules=[
                    "Target Number = Opponent's Parry",
                    "Raise = +1d6 damage",
                    "Can use Wild Attack (+2 Fighting, -2 Parry until next turn)"
                ],
                examples=[
                    "Fighting d8 + Wild Die vs Parry 5",
                    "Fighting d10 + Wild Die +1 (Gang Up) vs Parry 6"
                ]
            ),
            
            "shooting": DiceGuidance(
                situation="Shooting (Ranged Attack)",
                dice_to_roll="Shooting Skill + Wild Die",
                modifiers=[
                    "Short Range: +0",
                    "Medium Range: -2",
                    "Long Range: -4",
                    "+2 if target is large (Size +2 or bigger)",
                    "-2 if target has cover",
                    "-4 if target has heavy cover",
                    "Called Shot: -2 (limb), -4 (head/vitals), bypasses some armor",
                    "Multi-action penalty if taking multiple actions this turn"
                ],
                target_number=4,
                special_rules=[
                    "Raise = +1d6 damage",
                    "Can aim (+2 Shooting, requires one round without movement)",
                    "Rate of Fire: Roll multiple Shooting dice simultaneously (no multi-action penalty)",
                    "Each Shooting die is a separate attack roll; apply range/cover mods to each",
                    "Multi-action: 2 actions = -2 to each, 3 actions = -4 to each",
                    "For Full Auto attacks, see 'full_auto' guidance"
                ],
                examples=[
                    "Shooting d8 + Wild Die vs 4 (short range)",
                    "Shooting d10 + Wild Die -2 (medium range)",
                    "Shooting d6 + Wild Die -4 (long range) -2 (cover)",
                    "Shooting d8 + Wild Die -4 (called shot: head)",
                    "Rate of Fire 3: Roll 3 separate Shooting dice vs same target"
                ]
            ),
            
            # Damage Rolls
            "weapon_damage": DiceGuidance(
                situation="Weapon Damage",
                dice_to_roll="Weapon Damage + Strength (if melee)",
                modifiers=[
                    "+1d6 for each Raise on attack roll",
                    "+2 damage for Wild Attack",
                    "AP (Armor Piercing) reduces target's Armor",
                    "Heavy Weapon: +4 vs vehicles/structures"
                ],
                target_number=None,
                special_rules=[
                    "Acing: Dice explode on maximum result",
                    "Each point of damage over Toughness = 1 Wound",
                    "4+ points over Toughness = 1 additional Wound"
                ],
                examples=[
                    "Sword: Str+d8 (if Str d6 = d6+d8)",
                    "Pistol: 2d6 +1d6 (for raise)",
                    "Great Sword: Str+d10 with two-handed +1 parry"
                ]
            ),
            
            # Healing
            "healing": DiceGuidance(
                situation="Natural Healing",
                dice_to_roll="Vigor",
                modifiers=[
                    "+2 with medical attention",
                    "+1 with proper rest/care",
                    "-1 per current Wound level",
                    "-2 if environment is harsh"
                ],
                target_number=4,
                special_rules=[
                    "One roll per day",
                    "Success = heal 1 Wound",
                    "Raise = heal 1 additional Wound",
                    "Failure = no healing",
                    "Critical Failure = lose 1 Wound level"
                ],
                examples=[
                    "Vigor d8 vs 4 (basic healing)",
                    "Vigor d6 -2 (2 current wounds) vs 4",
                    "Vigor d10 +2 (medical attention) vs 4"
                ]
            ),
            
            "medical_healing": DiceGuidance(
                situation="Healing Skill (First Aid)",
                dice_to_roll="Healing Skill",
                modifiers=[
                    "+2 with medical kit/supplies",
                    "+1 in sterile environment",
                    "-1 per current Wound on patient",
                    "-2 if more than 1 hour since injury",
                    "-4 if more than 24 hours since injury"
                ],
                target_number=4,
                special_rules=[
                    "Only one attempt per person per injury",
                    "Success = heal 1 Wound",
                    "Raise = heal 1 additional Wound",
                    "Must be used within 24 hours of injury"
                ],
                examples=[
                    "Healing d6 +2 (med kit) vs 4",
                    "Healing d8 -1 (patient has 1 wound) vs 4"
                ]
            ),
            
            # Fear and Mental Effects
            "fear": DiceGuidance(
                situation="Fear Check",
                dice_to_roll="Spirit + Wild Die",
                modifiers=[
                    "Varies by fear source:",
                    "+0 for startling situations",
                    "-2 for frightening situations",
                    "-4 for horrifying situations",
                    "-6 for terrifying situations"
                ],
                target_number=4,
                special_rules=[
                    "Success = no effect",
                    "Failure = Shaken",
                    "Critical Failure = mark experience, gain Phobia Hindrance",
                    "Some creatures cause additional effects on failure"
                ],
                examples=[
                    "Spirit d6 vs 4 (startling)",
                    "Spirit d8 -2 vs 4 (frightening)",
                    "Spirit d6 -4 vs 4 (horrifying creature)"
                ]
            ),
            
            # Soak Rolls
            "soak": DiceGuidance(
                situation="Soak Roll (Damage Resistance)",
                dice_to_roll="Vigor + Wild Die",
                modifiers=[
                    "-1 per Wound level currently taken",
                    "Spend 1 Benny to attempt",
                    "Each success/raise negates 1 Wound"
                ],
                target_number=4,
                special_rules=[
                    "Must spend Benny to attempt",
                    "Roll after taking damage",
                    "Success = negate 1 Wound",
                    "Raise = negate 2 Wounds",
                    "Can attempt multiple times with multiple Bennies"
                ],
                examples=[
                    "Vigor d8 vs 4 (no current wounds)",
                    "Vigor d6 -2 vs 4 (2 current wounds)"
                ]
            ),
            
            # Initiative
            "initiative": DiceGuidance(
                situation="Initiative",
                dice_to_roll="Standard playing card OR Agility + Wild Die",
                modifiers=[
                    "Quick Edge: Draw extra card, keep best",
                    "Hesitant Hindrance: Draw extra card, keep worst",
                    "Level Headed: Draw extra card for ties",
                    "Combat Reflexes: +2 Spirit vs being Shaken"
                ],
                target_number=None,
                special_rules=[
                    "Cards: Spades > Hearts > Diamonds > Clubs",
                    "Face cards beat numbers",
                    "Jokers = best initiative + draw again",
                    "Alternative: Roll Agility, ties go to highest die type"
                ],
                examples=[
                    "Draw 1 card (or 2 with Quick Edge)",
                    "Agility d8 vs other characters' Agility"
                ]
            ),
            
            # Special Combat Actions
            "wild_attack": DiceGuidance(
                situation="Wild Attack",
                dice_to_roll="Fighting/Shooting + Wild Die",
                modifiers=[
                    "+2 to Fighting or Shooting roll",
                    "+2 to damage if hit",
                    "-2 to Parry until next turn"
                ],
                target_number=None,
                special_rules=[
                    "Declare before rolling",
                    "All-or-nothing high-risk attack",
                    "Parry penalty lasts until next turn"
                ],
                examples=[
                    "Fighting d8 +2 (Wild Attack) vs Parry",
                    "Damage: Str+d8 +2 (Wild Attack bonus)"
                ]
            ),
            
            # Full Auto
            "full_auto": DiceGuidance(
                situation="Full Auto Attack",
                dice_to_roll="Rate of Fire number of Shooting dice + Wild Die",
                modifiers=[
                    "-2 penalty to all Shooting rolls for this action",
                    "Standard range modifiers apply",
                    "Cover and other modifiers apply normally"
                ],
                target_number=4,
                special_rules=[
                    "Roll Rate of Fire number of Shooting dice + Wild Die",
                    "Wild Die may replace the result of one Shooting die for hit determination; it does not generate an extra hit",
                    "All dice take -2 penalty for Full Auto",
                    "Each successful die is a separate hit",
                    "Raises on individual dice add +1d6 damage each",
                    "Consumes RoF rounds of ammunition per action (e.g., RoF 3 = 3 rounds per Full Auto)",
                    "Can split dice among multiple targets within 2\" radius",
                    "If combined with multi-action, apply RoF and ammo use to each action separately",
                    "Some weapons have additional modes: Suppressive Fire, Three-Round Burst"
                ],
                examples=[
                    "RoF 3 weapon: Roll 3 Shooting dice + Wild Die, all at -2",
                    "Results: d8=2, d8=5, d8=3, Wild d6=6. Wild Die replaces one d8=2",
                    "Final: 5, 6, 3 vs TN 4 = 2 hits (uses 3 rounds)",
                    "Can assign 2 dice to one target, 1 die to another nearby target",
                    "Multi-action example: 2 Full Auto actions = 6 total rounds used"
                ]
            ),
            
            "called_shot": DiceGuidance(
                situation="Called Shot (Target Specific Location)",
                dice_to_roll="Fighting/Shooting + Wild Die",
                modifiers=[
                    "Limb (arm/leg): -2 to attack roll",
                    "Head/vitals: -4 to attack roll",
                    "Small target: GM discretion for extra penalties"
                ],
                target_number=None,
                special_rules=[
                    "Must declare target location before rolling",
                    "Head shots: +4 damage, possible instant incapacitation",
                    "Head shots: Often bypass helmet armor",
                    "Limb shots: May cause specific injuries or disarm",
                    "Called shots can target gaps in armor"
                ],
                examples=[
                    "Shooting d8 -4 (called shot: head) vs 4",
                    "Fighting d6 -2 (called shot: weapon hand) vs Parry",
                    "Shooting d10 -2 (called shot: leg) vs 4"
                ]
            ),
            
            # Multi-Actions
            "multi_action": DiceGuidance(
                situation="Multi-Action (Multiple actions in one turn)",
                dice_to_roll="All actions at penalty",
                modifiers=[
                    "-2 to all actions this turn",
                    "Each additional action: additional -2",
                    "3 actions total: -6 to all",
                    "Ambidextrous Edge: No off-hand penalty"
                ],
                target_number=None,
                special_rules=[
                    "Can perform multiple actions",
                    "All actions take the full penalty",
                    "Movement doesn't count as an action"
                ],
                examples=[
                    "2 attacks: Fighting d8 -2, Fighting d8 -2",
                    "3 actions: All rolls at -6"
                ]
            ),
            
            # Gang Up Bonus
            "gang_up": DiceGuidance(
                situation="Gang Up Bonus (Multiple Attackers)",
                dice_to_roll="Fighting/Shooting + Wild Die",
                modifiers=[
                    "+1 per ally adjacent to same target (max +4)",
                    "Only applies to Fighting attacks in melee",
                    "All attackers must be adjacent to target",
                    "Bonus applies to all attackers"
                ],
                target_number=None,
                special_rules=[
                    "Each ally adjacent to target gives +1 to all melee attacks",
                    "Maximum bonus is +4 (from 4+ allies)",
                    "Does not apply to ranged attacks",
                    "Must be declared before rolling"
                ],
                examples=[
                    "Fighting d8 +1 (1 ally) vs Parry",
                    "Fighting d6 +3 (3 allies) vs Parry",
                    "Fighting d10 +4 (4+ allies) vs Parry"
                ]
            )
        }
    
    def get_guidance(self, situation: str) -> Optional[DiceGuidance]:
        """Get guidance for a specific situation."""
        return self.guidance_db.get(situation.lower().replace(" ", "_"))
    
    def list_all_situations(self) -> List[str]:
        """Get a list of all available guidance situations."""
        return [guidance.situation for guidance in self.guidance_db.values()]
    
    def search_guidance(self, query: str) -> List[Tuple[str, DiceGuidance]]:
        """Search for guidance matching a query."""
        query_lower = query.lower()
        results = []
        
        for key, guidance in self.guidance_db.items():
            if (query_lower in guidance.situation.lower() or 
                query_lower in key or
                any(query_lower in example.lower() for example in guidance.examples)):
                results.append((key, guidance))
        
        return results
    
    def format_guidance(self, guidance: DiceGuidance) -> str:
        """Format guidance for display."""
        output = []
        output.append(f"📋 {guidance.situation}")
        output.append("=" * (len(guidance.situation) + 3))
        output.append("")
        
        output.append(f"🎲 Dice to Roll: {guidance.dice_to_roll}")
        
        if guidance.target_number:
            output.append(f"🎯 Target Number: {guidance.target_number}")
        else:
            output.append("🎯 Target Number: Variable (see modifiers)")
        
        output.append("")
        
        if guidance.modifiers:
            output.append("📊 Common Modifiers:")
            for modifier in guidance.modifiers:
                output.append(f"  • {modifier}")
            output.append("")
        
        if guidance.special_rules:
            output.append("⚡ Special Rules:")
            for rule in guidance.special_rules:
                output.append(f"  • {rule}")
            output.append("")
        
        if guidance.examples:
            output.append("💡 Examples:")
            for example in guidance.examples:
                output.append(f"  • {example}")
        
        return "\n".join(output)


def get_dice_guide() -> SavageWorldsDiceGuide:
    """Get the global dice guide instance."""
    return SavageWorldsDiceGuide()