# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation
from .Options import GameMode, GoldCoins, LocationsPerDungeon, TotalDungeons

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging, random, re

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    """ Selects dungeons based on player options and disables unchosen dungeons & locations """

    num_dungeons = get_option_value(multiworld, player, "amount_of_dungeons")  # Get the number of dungeons to include
    gamemode = get_option_value(multiworld, player, "gamemode")  # Get the selected game mode

    items_data = world.item_name_to_item.values()  # Retrieve all item data

    all_dungeons = [item for item in items_data if "Dungeons" in item.get("category", [])]  # Get all dungeons
    valid_dungeons = all_dungeons.copy()  # Start with all dungeons as valid

    if gamemode == 0:  # If game mode is 0, filter only "Free to Play" dungeons
        valid_dungeons = [item for item in all_dungeons if "Free to Play" in item.get("category", [])]

    all_dungeons = {dungeon["name"] for dungeon in all_dungeons}  
    valid_dungeons = list({dungeon["name"] for dungeon in valid_dungeons})

    world.random.shuffle(valid_dungeons)  # Randomize the order of valid dungeons
    selected_dungeons = list(valid_dungeons)[:num_dungeons]  # Select the required number of dungeons

    world.selected_dungeons = getattr(world, "selected_dungeons", {})
    world.selected_dungeons[player] = selected_dungeons

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    """ Removes locations belonging to unselected dungeons and those exceeding 'items_per_dungeon', while preserving Victory locations """
    
    if getattr(multiworld, 'generation_is_fake', False):
        return
    
    selected_dungeons = world.selected_dungeons.get(player, set())
    items_per_dungeon = get_option_value(multiworld, player, "items_per_dungeon")

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                dungeon_name = re.sub(r" - Item \d+$", "", location.name)

                if getattr(location, "victory", False) or "Victory" in dungeon_name:
                    continue  

                if dungeon_name:
                    if dungeon_name not in selected_dungeons:
                        region.locations.remove(location)
                        continue

                match = re.search(r"(\d+)$", location.name)
                if match:
                    item_number = int(match.group(1))
                    if item_number > items_per_dungeon:
                        region.locations.remove(location)

    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    """ Limits Gold Coins and removes items from unselected dungeons """

    selected_dungeons = set(world.selected_dungeons.get(player, set()))
    number_of_coins = get_option_value(multiworld, player, "gold_coins")

    # Remove excess Gold Coins
    gold_coins = [item for item in item_pool if item.name == "Gold Coin"]

    if len(gold_coins) > number_of_coins:
        excess_coins = len(gold_coins) - number_of_coins

        for _ in range(excess_coins):
            gold_coin = gold_coins.pop()
            multiworld.push_precollected(gold_coin)
            item_pool.remove(gold_coin)

    # Filter dungeon items
    filtered_items = []
    kept_dungeon_items = []

    for item in list(item_pool):  # Copy the list to avoid modification issues
        
        item_table_element = next(i_t for i_t in item_table if i_t['name'] == item.name)
        item_categories = item_table_element.get("category", [])

        if "Dungeons" not in item_categories:
            filtered_items.append(item)
            continue

        if item.name in selected_dungeons:
            filtered_items.append(item)
            kept_dungeon_items.append(item)

    # Randomly precollect one dungeon item
    if kept_dungeon_items:
        starter_item = random.choice(kept_dungeon_items)
        multiworld.push_precollected(starter_item)
        filtered_items.remove(starter_item)

    return world.add_filler_items(filtered_items, [])

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
        return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
        return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
