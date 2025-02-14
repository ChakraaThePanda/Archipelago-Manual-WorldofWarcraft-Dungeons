# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, Visibility

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

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
def before_options_defined(options: dict) -> dict:
    options["gamemode"] = GameMode
    options["apexis_crystals"] = ApexisCrystals
    options["items_per_dungeon"] = LocationsPerDungeon
    options["amount_of_dungeons"] = TotalDungeons
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["include_classic_cataclysm"].__doc__ = """When set to true, will include the dungeons for Classic/Cataclysm in the pool. (33 Dungeons)"""
    options["include_classic_cataclysm"].display_name = """Include Classic/Cataclysm"""
    options["include_the_burning_crusade"].__doc__ = """When set to true, will include the dungeons for The Burning Crusade in the pool. (16 Dungeons)"""
    options["include_the_burning_crusade"].display_name = """Include The Burning Crusade"""
    options["include_wrath_of_the_lich_king"].__doc__ = """When set to true, will include the dungeons for Wrath of the Lich King in the pool. (16 Dungeons)"""
    options["include_wrath_of_the_lich_king"].display_name = """Include Wrath of the Lich King"""
    options["include_mists_of_pandaria"].__doc__ = """When set to true, will include the dungeons for Mists of Pandaria in the pool. (6 Dungeons)"""
    options["include_mists_of_pandaria"].display_name = """Include Mists of Pandaria"""
    options["include_warlords_of_draenor"].__doc__ = """When set to true, will include the dungeons for Warlords of Draenor in the pool. (8 Dungeons)"""
    options["include_warlords_of_draenor"].display_name = """Include Warlords of Draenor"""
    options["include_legion"].__doc__ = """When set to true, will include the dungeons for Legion in the pool. (8 Dungeons)"""
    options["include_legion"].display_name = """Include Legion"""
    options["include_battle_for_azeroth"].__doc__ = """When set to true, will include the dungeons for Battle for Azeroth in the pool. (8 Dungeons)"""
    options["include_battle_for_azeroth"].display_name = """Include Battle for Azeroth"""
    options["include_shadowlands"].__doc__ = """When set to true, will include the dungeons for Shadowlands in the pool. (8 Dungeons)"""
    options["include_shadowlands"].display_name = """Include Shadowlands"""
    options["include_dragonflight"].__doc__ = """When set to true, will include the dungeons for Dragonflight in the pool. (8 Dungeons)"""
    options["include_dragonflight"].display_name = """Include Dragonflight"""
    for option in options.keys():
        if 'dungeonamounts_' in option:
            options[option].visibility = Visibility.none    
    return options