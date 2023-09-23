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
                if (not has_visited) and (not is_obstacle):
                    position_queue.append(new_tuple)
                    visited_set.add(coord_str)
        #print(f"{start.x},{start.y} is moving to {return_position.x},{return_position.y} for goal {goal.x},{goal.y}")
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
            CharacterClassType.MARKSMAN: 3,
            CharacterClassType.MEDIC: 5,
            CharacterClassType.BUILDER: 5,
            CharacterClassType.DEMOLITIONIST: 3 
        }
        return choices

    def set_up_initial_barricade(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
    ) -> list[MoveAction]:
        p1 = Position(41, 43)
        p2 = Position(50, 43)
        p3 = Position(59, 43)

        barricade_list = [p1, p2, p3]

        obstacle_set = self.find_obstacles(game_state)
        for barricade in barricade_list:
            str_pos = f"{barricade.x},{barricade.y}"
            if str_pos in obstacle_set:
                barricade_list.remove(barricade)

        choices = []
        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:
                continue
            pos = game_state.characters[character_id].position

            is_builder = game_state.characters[character_id].class_type == CharacterClassType.BUILDER
            if is_builder:
                if len(barricade_list) == 0: # if nothing to be built, move to bottom right
                    is_builder = False
                else:
                    min_distance = 1234
                    closest_barricade = barricade_list[0]
                    for p in barricade_list: # finds the closest barricade position and sets it to new position
                        distance = abs(p.x - pos.x) + abs(p.x - pos.x)
                        if distance < min_distance:
                            min_distance = distance
                            p_to_move_to = p
                    barricade_list.remove(p_to_move_to)
                    new_pos = self.simple_bfs(p_to_move_to, pos, game_state, 3)
                    new_action = MoveAction(character_id, new_pos)
                    choices.append(new_action)
            if not is_builder: # run to bottom right
                bot_right = Position(64, 75)
                new_pos = self.simple_bfs(bot_right, pos, game_state, 3)
                new_action = MoveAction(character_id, new_pos)
                choices.append(new_action)

                
            # find barricade closest to them
            # move to closest barricade
        return choices

    

    




    
    def simple_run(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> MoveAction:
        
        choices = []

        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the human
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

        is_in_setup = (game_state.turn < 30)
        
        #print(f"Turn {game_state.turn}: -------------------------------------")
        if is_in_setup:
            choices = self.set_up_initial_barricade(possible_moves, game_state)
            #print(len(choices))
        else:
            choices = self.simple_run(possible_moves, game_state)

        return choices

    def decide_attacks(
            self, 
            possible_attacks: dict[str, list[AttackAction]], 
            game_state: GameState
            ) -> list[AttackAction]:
        choices = []
        """
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
            """

        return choices

    def decide_abilities(
            self, 
            possible_abilities: dict[str, list[AbilityAction]], 
            game_state: GameState
            ) -> list[AbilityAction]:
        choices = []
        """
        for [character_id, abilities] in possible_abilities.items():
            if len(abilities) == 0:  # No choices? Next!
                continue

            # Since we only have medics, the choices must only be healing a nearby human
            human_target = abilities[0]  # the human that'll be healed
            least_health = 999  # The health of the human being targeted

            for a in abilities:
                health = game_state.characters[a.character_id_target].health  # Health of human in question

                if health < least_health:  # If they have less health, they are the new patient!
                    human_target = a
                    least_health = health

            if human_target:  # Give the human a cookie
                choices.append(human_target)
        """
        return choices
