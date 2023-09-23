# This is a simple human strategy:
# 6 Marksman, 6 Medics, and 4 Traceurs
# Move as far away from the closest zombie as possible
# If there are any zombies in attack range, attack the closest
# If a Medic's ability is available, heal a human in range with the least health

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.ability_action_type import AbilityActionType
from game.character.action.attack_action import AttackAction
from game.character.action.attack_action_type import AttackActionType
from game.character.action.move_action import MoveAction
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position
from strategy.strategy import Strategy


class TestSetupStrategy(Strategy):
    def find_obstacles( # returns a set with all coordinates in coord_str format with obstacles
        self,
        game_state: GameState
    ) -> set[str]:
        obstacle_set = set({})
        for [terrain_id, terrain_obj] in game_state.terrains.items():
            pos = terrain_obj.position
            obstacle_set.add(f"{pos.x},{pos.y}")
        return obstacle_set

    def simple_bfs( # returns the next value that the start position should move to reach the goal given a move speed of step
        self,
        goal: Position,
        start: Position,
        game_state: GameState,
        move_speed: int
    ) -> Position:

        if (goal.x == start.x) and (goal.y == start.y): # if we are already on the goal, return the goal itself
            return goal
        obstacle_set = self.find_obstacles(game_state)
        position_queue = [tuple([goal if i == 0 else None for i in range(move_speed + 1)])] # format of tuple (curr, 1 before curr, 2 before curr, 3 before curr, etc depending on move_speed)

        visited_set = {f"{goal.x},{goal.y}"}

        return_position = None
        while position_queue and return_position == None:
            node_tuple = position_queue.pop(0)
            curr = node_tuple[0]
            p_left = Position(curr.x - 1, curr.y)
            p_right = Position(curr.x + 1, curr.y)
            p_up = Position(curr.x, curr.y + 1)
            p_down = Position(curr.x, curr.y - 1)
            p_list = [p_left, p_right, p_up, p_down]
            for p in p_list:
                new_tuple = tuple([p if i == 0 else node_tuple[i - 1] for i in range(move_speed + 1)])
                if p.x == start.x and p.y == start.y:
                    offset = 0
                    return_position = new_tuple[move_speed - offset]
                    while return_position == None:
                        offset += 1
                        return_position = node_tuple[move_speed - offset]
                    break
                coord_str = f"{p.x},{p.y}"
                has_visited = coord_str in visited_set
                is_obstacle = coord_str in obstacle_set
                valid_coords = p.x >= 0 and p.x < 100 and p.y >= 0 and p.y < 100 
                if (not has_visited) and (not is_obstacle) and (valid_coords):
                    position_queue.append(new_tuple)
                    visited_set.add(coord_str)
        return return_position

    def decide_character_classes(
            self,
            possible_classes: list[CharacterClassType],
            num_to_pick: int,
            max_per_same_class: int,
            ) -> dict[CharacterClassType, int]:
        # The maximum number of special classes we can choose is 16
        # Selecting 6 Marksmen, 6 Medics, and 4 Traceurs
        # The other 4 humans will be regular class
        choices = {
            CharacterClassType.MARKSMAN: 2,
            CharacterClassType.MEDIC: 5,
            CharacterClassType.BUILDER: 5,
            CharacterClassType.DEMOLITIONIST: 1,
            CharacterClassType.TRACEUR: 3
        }
        return choices

    def set_up_initial_barricade(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
    ) -> list[MoveAction]:

        t1 = Position(28, 48)
        t2 = Position(71, 45)
        t3 = Position(0, 99)
        traceur_list = [t1, t2, t3]

        p1 = Position(41, 44)
        p2 = Position(50, 44)
        p3 = Position(59, 44)
        p4 = Position(70, 44)
        p5 = Position(71, 44)

        dummy_list = [p1, p2, p3, p4, p5]
        barricade_list = []
        obstacle_set = self.find_obstacles(game_state)
        builder_to_barricade = {} # maps the barricade object to a given builder
        for barricade in dummy_list:
            str_pos = f"{barricade.x},{barricade.y - 1}"
            if not(str_pos in obstacle_set):
                print(f"{str_pos} is empty")
                barricade_list.append(barricade)
                closest_builder_id = -1
                min_distance = 1234
                for [character_id, moves] in possible_moves.items():
                    if len(moves) == 0 or (not game_state.characters[character_id].class_type == CharacterClassType.BUILDER):
                        continue
                    pos = game_state.characters[character_id].position
                    distance = abs(barricade.x - pos.x) + abs(barricade.y - pos.y)
                    if distance < min_distance and not(character_id in builder_to_barricade):
                        closest_builder_id = character_id
                        min_distance = distance
                builder_to_barricade[closest_builder_id] = barricade
        print(f"length of dict: {len(builder_to_barricade)}")
        print(builder_to_barricade)         
        choices = []
        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:
                continue
            pos = game_state.characters[character_id].position

            is_traceur = game_state.characters[character_id].class_type == CharacterClassType.TRACEUR
            if is_traceur:
                min_distance = 1234
                closest_goal = traceur_list[0]
                for p in traceur_list:
                    distance = abs(p.x - pos.x) + abs(p.y - pos.y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_goal = p
                traceur_list.remove(closest_goal)
                new_pos = self.simple_bfs(closest_goal, pos, game_state, 4)
                new_action = MoveAction(character_id, new_pos)
                choices.append(new_action)
            elif character_id in builder_to_barricade:
                print(f"{character_id} is moving to barricade")
                new_pos = self.simple_bfs(builder_to_barricade[character_id], pos, game_state, 3)
                new_action = MoveAction(character_id, new_pos)
                choices.append(new_action)
            else: # run to bottom right if not traceur
                bot_right = Position(64, 75)
                new_pos = self.simple_bfs(bot_right, pos, game_state, 3)
                new_action = MoveAction(character_id, new_pos)
                choices.append(new_action)

                
        return choices

    

    




    
    def simple_run(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> MoveAction:
        
        choices = []

        t1 = Position(0, 0)
        t2 = Position(99, 27)
        t3 = Position(0, 99)
        traceur_list = [t1, t2, t3]

        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the human
            is_traceur = game_state.characters[character_id].class_type == CharacterClassType.TRACEUR
            closest_zombie_pos = pos  # default position is zombie's pos
            closest_zombie_distance =  1234  # large number, map isn't big enough to reach this distance
            

            # Iterate through every zombie to find the closest one
            for c in game_state.characters.values():
                if not c.is_zombie:
                    continue  # Fellow humans are frens :D, ignore them

                distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y)  # calculate manhattan distance between human and zombie
                if distance < closest_zombie_distance:  # If distance is closer than current closest, replace it!
                    closest_zombie_pos = c.position
                    closest_zombie_distance = distance

            if is_traceur and closest_zombie_distance > 15:
                min_distance = 1234
                closest_goal = traceur_list[0]
                for p in traceur_list:
                    distance = abs(p.x - pos.x) + abs(p.y - pos.y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_goal = p
                traceur_list.remove(closest_goal)
                new_pos = self.simple_bfs(closest_goal, pos, game_state, 4)
                new_action = MoveAction(character_id, new_pos)
                choices.append(new_action)

            

            # Move as far away from the zombie as possible
            move_distance = -1  # Distance between the move action's destination and the closest zombie
            move_choice = moves[0]  # The move action the human will be taking

            for m in moves:
                distance = abs(m.destination.x - closest_zombie_pos.x) + abs(m.destination.y - closest_zombie_pos.y)  # calculate manhattan distance

                if distance > move_distance:  # If distance is further, that's our new choice!
                    move_distance = distance
                    move_choice = m

            choices.append(move_choice)  # add the choice to the list

        return choices

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> list[MoveAction]:
        choices = []
        print(f"{game_state.turn}------------------------------------")
        is_in_setup = (game_state.turn < 20)
        if is_in_setup:
            choices = self.set_up_initial_barricade(possible_moves, game_state)
        else:
            choices = self.simple_run(possible_moves, game_state)

        return choices

    def decide_attacks(
            self, 
            possible_attacks: dict[str, list[AttackAction]], 
            game_state: GameState
            ) -> list[AttackAction]:
        choices = []
        
        for [character_id, attacks] in possible_attacks.items():
            if len(attacks) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the human
            closest_zombie = None  # Closest zombie in range
            closest_zombie_distance = 404  # Distance between closest zombie and human

            # Iterate through zombies in range and find the closest one
            for a in attacks:
                if a.type is AttackActionType.CHARACTER:
                    attackee_pos = game_state.characters[a.attacking_id].position  # Get position of zombie in question
                    
                    distance = abs(attackee_pos.x - pos.x) + abs(attackee_pos.y - pos.y)  # Get distance between the two

                    if distance < closest_zombie_distance:  # Closer than current? New target!
                        closest_zombie = a
                        closest_zombie_distance = distance

            if closest_zombie:  # Attack the closest zombie, if there is one
                choices.append(closest_zombie)
            

        return choices

    def set_up_initial_barricade_abilities(
            self, 
            possible_abilities: dict[str, list[AbilityAction]], 
            game_state: GameState
    ) -> list[AbilityAction]:
        choices = []
        p1 = Position(41, 43)
        p2 = Position(50, 43)
        p3 = Position(59, 43)
        p4 = Position(70, 43)
        p5 = Position(71, 43)

        dummy_list = [p1, p2, p3, p4, p5]

        barricade_list = [p1, p2, p3, p4, p5]
        barr_str_list = []
        obstacle_set = self.find_obstacles(game_state)
        for barricade in barricade_list:
            str_pos = f"{barricade.x},{barricade.y}"
            if not (str_pos in obstacle_set):
                barr_str_list.append(str_pos)

        for [character_id, abilities] in possible_abilities.items():
            if len(abilities) == 0:  # No choices? Next!
                continue

            # determine medic action
            if game_state.characters[character_id].class_type == CharacterClassType.MEDIC:
                for a in abilities:
                    if game_state.characters[str(a.character_id_target)].class_type == CharacterClassType.MEDIC:
                        choices.append(a)
                        break
                choices.append(abilities[0])

            # determine builder action
            if game_state.characters[character_id].class_type == CharacterClassType.BUILDER:
                for a in abilities:
                    pos = a.positional_target
                    if f"{pos.x},{pos.y}" in barr_str_list:
                        choices.append(a)
                        break

        return choices
    
    def medic_heal (
        self, 
        possible_abilities: dict[str, list[AbilityAction]], 
        game_state: GameState
        ) -> list[AbilityAction]:
        choices = []
        for [character_id, abilities] in possible_abilities.items():
            if len(abilities) == 0:  # No choices? Next!
                continue

            # determine medic action
            if game_state.characters[character_id].class_type == CharacterClassType.MEDIC:
                for a in abilities:
                    if game_state.characters[str(a.character_id_target)].class_type == CharacterClassType.MEDIC:
                        choices.append(a)
                        break
                choices.append(abilities[0])
        return choices

    def decide_abilities(
            self, 
            possible_abilities: dict[str, list[AbilityAction]], 
            game_state: GameState
            ) -> list[AbilityAction]:
        choices = []
        is_in_setup = (game_state.turn < 20)
        if is_in_setup:
            choices = self.set_up_initial_barricade_abilities(possible_abilities, game_state)
        else:
            choices = self.medic_heal(possible_abilities, game_state)

        return choices
