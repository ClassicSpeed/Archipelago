import logging
import re
from dataclasses import dataclass, field
from typing import List, TextIO

from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_characters, is_level_playable, \
    is_character_playable
from .Enums import Character, Area, pascal_to_space, LevelMission, level_area_connections, \
    bosses_area_connections, AreaConnection, LogicLevelDifficulty, chao_garden_area_connections, LEVEL_AREAS, \
    all_areas_with_multiple_connections, all_areas_with_one_connection, non_existent_areas
from .Locations import level_location_table, mission_location_table
from .Options import SonicAdventureDXOptions


@dataclass
class CharacterArea:
    character: Character
    area: Area = None


@dataclass
class StarterSetup:
    character: Character = None
    area: Area = None
    charactersWithArea: List[CharacterArea] = field(default_factory=list)
    level_mapping: dict[AreaConnection, AreaConnection] = field(default_factory=dict)

    def get_starting_area(self, character: Character) -> Area:
        for char_area in self.charactersWithArea:
            if char_area.character == character:
                return char_area.area
        return self.area


def generate_early_sadx(world: World, options: SonicAdventureDXOptions) -> StarterSetup:
    validate_settings(options)

    possible_characters = get_playable_characters(options)

    world.random.shuffle(possible_characters)

    if options.starting_character.value != 0:
        possible_characters.remove(Character(options.starting_character.value))
        possible_characters.insert(0, Character(options.starting_character.value))

    starter_setup = calculate_starter_locations(options, possible_characters, world)

    if options.entrance_randomizer.value > 0:
        area_list = list(level_area_connections)
        if options.entrance_randomizer.value >= 2:
            area_list += bosses_area_connections
        if options.entrance_randomizer.value >= 3:
            area_list += chao_garden_area_connections

        if options.entrance_randomizer.value == 4:
            randomized_remaining_areas_2 = {}
            all_areas_to_connect = [all_areas_with_multiple_connections.copy(), all_areas_with_one_connection.copy(),
                                    LEVEL_AREAS.copy()]
            starting_area = starter_setup.area
            for group in all_areas_to_connect:
                if starting_area in group:
                    group.remove(starting_area)
            unused_connections = list(AreaConnection.from_area(starting_area))

            extra_weird_connections = []
            # Prioritize areas with multiple connections.
            for area_group in all_areas_to_connect:
                # Repeat until al areas are connected.
                while area_group:
                    # Select a random entrance from all the available unused entrances and connect en unconnected area
                    next_area = world.random.choice(area_group)
                    area_group.remove(next_area)
                    new_next_area_connections = AreaConnection.from_area(next_area)

                    # Do not add extra Final Egg, Lost World, Sky Deck, and Speed Highway entrances
                    a_selected_connection = world.random.choice(unused_connections)
                    b_selected_connection = world.random.choice(new_next_area_connections)
                    if next_area in [Area.FinalEgg, Area.LostWorld, Area.SkyDeck, Area.SpeedHighway]:
                        extra_weird_connections += new_next_area_connections
                    else:
                        unused_connections += new_next_area_connections

                    randomized_remaining_areas_2[a_selected_connection] = b_selected_connection
                    randomized_remaining_areas_2[b_selected_connection] = a_selected_connection
                    print(f"-- {b_selected_connection} is connected to {a_selected_connection}")
                    unused_connections.remove(a_selected_connection)
                    if next_area not in [Area.FinalEgg, Area.LostWorld, Area.SkyDeck, Area.SpeedHighway]:
                        unused_connections.remove(b_selected_connection)

            print("++ Unused doors")
            # Check unused doors, connect them randomly
            unused_connections += extra_weird_connections
            world.random.shuffle(unused_connections)
            for connection_a, connection_b in zip(unused_connections[::2], unused_connections[1::2]):
                randomized_remaining_areas_2[connection_a] = connection_b
                randomized_remaining_areas_2[connection_b] = connection_a
                print(f"-- {connection_b} is connected to {connection_a}")

        if 0 < options.entrance_randomizer.value < 4:
            randomized_remaining_areas = dict(
                zip(
                    area_list,
                    world.random.sample(area_list, len(area_list))
                )
            )
        else:
            randomized_remaining_areas = randomized_remaining_areas_2
        starter_setup.level_mapping = randomized_remaining_areas

    return starter_setup


def validate_settings(options):
    if not get_playable_characters(options):
        logging.warning(" -- SADX warning: Zero playable characters in settings. enabling Sonic as a failsafe.")
        options.playable_sonic.value = True

    if options.gating_mode.value == 0 and not options.goal_requires_emblems:
        logging.warning(
            " -- SADX warning: Gating mode is set to Emblems and they are not enabled. Enabling emblems as a failsafe.")
        options.goal_requires_emblems.value = True
    if options.entrance_randomizer.value >= 3 and options.chao_egg_checks:
        logging.warning(
            " -- SADX warning: Extended random level entrances is not compatible with egg checks. Disabling them as a failsafe.")
        options.chao_egg_checks.value = False

    if options.starting_character.value > 0:
        if Character(options.starting_character.value) not in get_playable_characters(options):
            logging.warning(
                " -- SADX warning: Starting character is not playable. Randomizing starting character.")
            options.starting_character.value = 0

    if (not options.goal_requires_levels and not options.goal_requires_missions and not options.goal_requires_emblems
            and not options.goal_requires_chaos_emeralds and not options.goal_requires_bosses and not options.goal_requires_chao_races):
        logging.warning(" -- SADX warning: No goal requirement set. Enabling action stages requirement as a failsafe.")
        options.goal_requires_levels.value = True

    if options.goal_requires_levels.value or options.chao_races_checks:
        levels_available = False
        for level in level_location_table:
            if is_level_playable(level, options) and level.levelMission == LevelMission.C:
                levels_available = True
        if not levels_available:
            options.sonic_action_stage_missions.value = 1
            options.tails_action_stage_missions.value = 1
            options.knuckles_action_stage_missions.value = 1
            options.amy_action_stage_missions.value = 1
            options.big_action_stage_missions.value = 1
            options.gamma_action_stage_missions.value = 1
            if options.goal_requires_levels.value and not options.chao_races_checks:
                logging.warning(
                    " -- SADX warning: No action stages enabled with levels as goal. Enabling all characters levels as a failsafe")
            elif not options.goal_requires_levels.value and options.chao_races_checks:
                logging.warning(
                    " -- SADX warning: No action stages enabled with chao races as checks. Enabling all characters levels as a failsafe")
            else:
                logging.warning(
                    " -- SADX warning: No action stages enabled with chao races and levels as goal. Enabling all characters levels as a failsafe")

    if options.goal_requires_missions.value:
        if not options.mission_mode_checks.value:
            logging.warning(
                " -- SADX warning: Missions as goal requirement are enabled but mission mode checks are disabled. Enabling mission mode checks.")
            options.mission_mode_checks.value = True
    if options.goal_requires_bosses.value:
        if not options.boss_checks.value:
            logging.warning(
                " -- SADX warning: Bosses as goal requirement are enabled but mission mode checks are disabled. Enabling bosses checks.")
            options.boss_checks.value = True
    if options.goal_requires_chao_races.value:
        if not options.chao_races_checks.value:
            logging.warning(
                " -- SADX warning: Chao Races as goal requirements are enabled but chao races checks are disabled. Enabling chao races checks.")
            options.chao_races_checks.value = True

        mission_quantity = 0
        for mission in mission_location_table:
            if str(mission.missionNumber) in options.mission_blacklist.value:
                continue
            if str(mission.character.name) in options.mission_blacklist.value:
                continue
            if is_character_playable(mission.character, options):
                mission_quantity += 1
        if mission_quantity == 0:
            raise OptionError(
                " -- SADX Error: You need to add more missions in the settings to use mission as goal. Either add more characters or remove missions from the blacklist.")

    if options.logic_level.value == LogicLevelDifficulty.Easy and (
            options.sonic_action_stage_missions.value == 4 or options.tails_action_stage_missions.value == 4
            or options.knuckles_action_stage_missions.value == 4 or options.amy_action_stage_missions.value == 4
            or options.big_action_stage_missions.value == 4 or options.gamma_action_stage_missions.value == 4):
        raise OptionError(
            " -- SADX error: S-Rank missions are not available for easy logic, please select a harder logic level.")


def get_possible_starting_areas() -> List[Area]:
    return [Area.Station, Area.Casino, Area.Sewers, Area.SSMain, Area.TPTunnel, Area.Hotel, Area.HotelPool,
            Area.TPLobby, Area.MRMain, Area.AngelIsland, Area.IceCave, Area.PastAltar, Area.PastMain, Area.Jungle,
            Area.FinalEggTower, Area.CaptainRoom, Area.ECPool, Area.Arsenal, Area.ECInside,
            Area.HedgehogHammer, Area.PrisonHall, Area.WaterTank, Area.WarpHall, Area.ECBridge, Area.ECDeck]


def write_sadx_spoiler(world: World, spoiler_handle: TextIO, starter_setup: StarterSetup,
                       options: SonicAdventureDXOptions):
    spoiler_handle.write("\n")
    header_text = f"Sonic Adventure starting setup for {world.multiworld.player_name[world.player]}:\n"
    spoiler_handle.write(header_text)

    starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', starter_setup.area.name)

    text = "- Will start as {0} in the {1} area.\n"
    text = text.format(starter_setup.character.name, starting_area_name)

    for characterArea in starter_setup.charactersWithArea:
        if characterArea.character == starter_setup.character:
            continue
        starting_area_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', characterArea.area.name)
        text += "- {0} will spawn in the {1} area.\n".format(characterArea.character.name, starting_area_name)

    if options.entrance_randomizer:
        text += f"\nLevel entrances:\n"
        for original, randomized in starter_setup.level_mapping.items():
            text += f"- {pascal_to_space(original.name)} -> {pascal_to_space(randomized.name)}\n"
    spoiler_handle.writelines(text)


def calculate_starter_locations(options: SonicAdventureDXOptions,
                                possible_characters: List[Character],
                                world: World) -> StarterSetup:
    starter_setup = StarterSetup()

    possible_starter_areas = get_possible_starting_areas()
    if options.starting_location.value == 0 and Area.SSMain in possible_starter_areas:
        starter_setup.area = Area.SSMain
    else:
        starter_setup.area = world.random.choice(possible_starter_areas)
    starter_setup.character = possible_characters[0]

    if not starter_setup.area:
        raise OptionError(
            "SADX Error: Couldn't define a valid starting location (Probably a problem of low settings, guaranteed level and/or fixed starting location).")
    if options.starting_location.value == 2:
        used_areas = {starter_setup.area}
        starter_setup.charactersWithArea.append(CharacterArea(starter_setup.character, starter_setup.area))
        for character in possible_characters:
            if character == starter_setup.character:
                continue
            unused_areas = [area for area in get_possible_starting_areas(options) if area not in used_areas]
            area = world.random.choice(unused_areas if unused_areas else get_possible_starting_areas(options))
            used_areas.add(area)
            starter_setup.charactersWithArea.append(CharacterArea(character, area))
    return starter_setup
