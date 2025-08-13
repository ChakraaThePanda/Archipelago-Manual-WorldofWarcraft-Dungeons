# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions, Visibility
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class GameMode(Choice):
    """The "Free to Play" mode will only allow dungeons playable at level 20 and under. (71 possible Dungeons) 
    "All" will offer every dungeons accessible below level 60. (40 additional Dungeons)"""
    display_name = "GameMode"
    option_free_to_play = 0
    option_all = 1
    default = 1

class ApexisCrystals(Range):
    """Select the amount of Apexis Crystals you need to complete your Goal"""
    display_name = "Apexis Crystals amount"
    range_start = 1
    range_end = 100
    default = 10

class LocationsPerDungeon(Range):
    """Select the amount of items each dungeon will send in the pool"""
    display_name = "Items per Dungeon"
    range_start = 1
    range_end = 10
    default = 4

class TotalDungeons(Range):
    """Select the amount of dungeons to complete"""
    display_name = "Dungeons to complete"
    range_start = 1
    range_end = 50
    default = 10

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["gamemode"] = GameMode
    options["apexis_crystals"] = ApexisCrystals
    options["items_per_dungeon"] = LocationsPerDungeon
    options["amount_of_dungeons"] = TotalDungeons
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    options.type_hints["include_classic_cataclysm"].__doc__ = """When set to true, will include the dungeons for Classic/Cataclysm in the pool. (33 Dungeons)"""
    options.type_hints["include_classic_cataclysm"].display_name = """Include Classic/Cataclysm"""
    options.type_hints["include_the_burning_crusade"].__doc__ = """When set to true, will include the dungeons for The Burning Crusade in the pool. (16 Dungeons)"""
    options.type_hints["include_the_burning_crusade"].display_name = """Include The Burning Crusade"""
    options.type_hints["include_wrath_of_the_lich_king"].__doc__ = """When set to true, will include the dungeons for Wrath of the Lich King in the pool. (16 Dungeons)"""
    options.type_hints["include_wrath_of_the_lich_king"].display_name = """Include Wrath of the Lich King"""
    options.type_hints["include_mists_of_pandaria"].__doc__ = """When set to true, will include the dungeons for Mists of Pandaria in the pool. (6 Dungeons)"""
    options.type_hints["include_mists_of_pandaria"].display_name = """Include Mists of Pandaria"""
    options.type_hints["include_warlords_of_draenor"].__doc__ = """When set to true, will include the dungeons for Warlords of Draenor in the pool. (8 Dungeons)"""
    options.type_hints["include_warlords_of_draenor"].display_name = """Include Warlords of Draenor"""
    options.type_hints["include_legion"].__doc__ = """When set to true, will include the dungeons for Legion in the pool. (8 Dungeons)"""
    options.type_hints["include_legion"].display_name = """Include Legion"""
    options.type_hints["include_battle_for_azeroth"].__doc__ = """When set to true, will include the dungeons for Battle for Azeroth in the pool. (8 Dungeons)"""
    options.type_hints["include_battle_for_azeroth"].display_name = """Include Battle for Azeroth"""
    options.type_hints["include_shadowlands"].__doc__ = """When set to true, will include the dungeons for Shadowlands in the pool. (8 Dungeons)"""
    options.type_hints["include_shadowlands"].display_name = """Include Shadowlands"""
    options.type_hints["include_dragonflight"].__doc__ = """When set to true, will include the dungeons for Dragonflight in the pool. (8 Dungeons)"""
    options.type_hints["include_dragonflight"].display_name = """Include Dragonflight"""
    return options

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
