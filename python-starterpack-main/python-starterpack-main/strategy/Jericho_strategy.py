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
            moves: list[MoveAction],
            character_id: str,
            game_state: GameState
    ) -> MoveAction:
        p1 = Position(41, 42)
        p2 = Position(50, 42)
        p3 = Position(59, 42)
        p4 = Position(70, 43)
        p5 = Position(71, 42)
        barricade_list = [p1, p2, p3, p4, p5]
            
        pos = game_state.characters[character_id].position
        if game_state.characters[character_id].class_type == "BUILDER":
            min_distance = 1234
            p_to_move_to = barriacde_list[0]
            for p in barricade_list:
                distance = abs(p.x - pos.x) + abs(p.x - pos.x)
                if distance < min_distance:
                    min_distance = distance
                    p_to_move_to = p
            move_distance = -1
            move_choice = moves[0]
            for m in moves:
                distance = abs(m.destination.x - closest_zombie_pos.x) + abs(m.destination.y - closest_zombie_pos.y)

                if distance > move_distance:  # If distance is further, that's our new choice!
                    move_distance = distance
                    move_choice = m

                
            # find barricade closest to them
            # move to closest barricade
        else:

    def simple_bfs( # returns the next value that the start position should move to reach the goal given a move speed of step
        self,
        goal: Position,
        start: Position,
        game_state: GameState
        step: int
    ) -> Position:
        position_queue = [(goal, None, None, None)] # format of tuple (curr, 1 before curr, 2 before curr, 3 before curr)
        visited_set = {goal}
        while position_queue:
            node_tuple = position_queue.pop()
            curr = position_queue
            for x in range(-1, 2):
                for y in range(-1, 2):
                    p = Position(curr.x + x, curr.y + y)
                    position_queue.append(())


    def find_obstacles( # method used to iterate over terrain array, find all obstacles, then return a set of Position objects where an obstacle exists
        self,
        game_state: GameState
    ) -> set[Position]:
        obstacle_set = {}
        for [terrain_id, terrain_obj] in GameState.terrains:
            if terrain_obj.health != 0:
                obstacle_set.add(terrain_obj.position)
        return obstacle_set




    
    def simple_run(
            self, 
            moves: list[MoveAction],
            character_id: str,
            game_state: GameState
            ) -> list[MoveAction]:
        
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

        return move_choice

    def decide_moves(
            self, 
            possible_moves: dict[str, list[MoveAction]], 
            game_state: GameState
            ) -> list[MoveAction]:
        choices = []

        is_in_setup = (game_state.turn < 6)
        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:
                continue
            
            choice = moves[0]
            if is_in_setup:
                choice = self.set_up_initial_barricade(possible_moves, game_state)
            else:
                choice = self.simple_run(possible_moves, game_state)
            choices.append(choice)
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

    def decide_abilities(
            self, 
            possible_abilities: dict[str, list[AbilityAction]], 
            game_state: GameState
            ) -> list[AbilityAction]:
        choices = []

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
        
        return choices
