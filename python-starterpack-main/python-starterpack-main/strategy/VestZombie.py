# This is a simple zombie strategy:
# Move directly towards the closest human. If there are any humans in attacking range, attack a random one.
# If there are no humans in attacking range but there are obstacles, attack a random obstacle.

import random
from game.character.action.ability_action import AbilityAction
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.game_state import GameState
from game.character.action.attack_action_type import AttackActionType
from strategy.strategy import Strategy
from game.util.position import Position


class VestZombieStrategy(Strategy):


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
                if (not has_visited) and (not is_obstacle) and valid_coords:
                    position_queue.append(new_tuple)
                    visited_set.add(coord_str)
        return return_position

    def regular_move(
        self, 
        possible_moves: dict[str, list[MoveAction]],
        game_state: GameState
        ) -> list[MoveAction]:
        choices = []
        character_id_set = set({})
        for [character_id, moves] in possible_moves.items():
            if len(moves) == 0:  # No choices... Next!
                continue

            pos = game_state.characters[character_id].position  # position of the zombie
            closest_human_pos = pos  # default position is zombie's pos
            closest_human_distance = 1984  # large number, map isn't big enough to reach this distance
            closest_human_id = "a"
            # Iterate through every human to find the closest one
            for c in game_state.characters.values():
                if len(character_id_set) < 13:
                    if c.is_zombie or c.id in character_id_set:
                        continue  # Fellow zombies are frens :D, ignore them
                else:
                    if c.is_zombie:
                        continue

                distance = abs(c.position.x - pos.x) + abs(c.position.y - pos.y) # calculate manhattan distance between human and zombie
                if distance < closest_human_distance:  # If distance is closer than current closest, replace it!
                    closest_human_pos = c.position
                    closest_human_distance = distance
                    closest_human_id = c.id
            character_id_set.add(closest_human_id)
            new_pos = self.simple_bfs(closest_human_pos, pos, game_state, 5)
            new_action = MoveAction(character_id, new_pos)

            choices.append(new_action)  # add the choice to the list

        return choices

    def set_up_initial_diamond(
                self, 
                possible_moves: dict[str, list[MoveAction]],
                game_state: GameState
        ) -> MoveAction:
            p1 = Position(64, 42)
            p2 = Position(34, 42)
            p3 = Position(11, 41)
            p4 = Position(50, 41)
            p5 = Position(98, 42)
            diamond_list = [p1, p2, p3, p4, p5]
            choices = []

            for [character_id, moves] in possible_moves.items():
                if len(moves) == 0:  
                    continue
                pos = game_state.characters[character_id].position  # position of the zombie
                closest_goal = pos
                closest_goal_distance = 1000
                for i in diamond_list:
                    distance = abs(i.x - pos.x) + abs(i.y - pos.y)
                    if distance < closest_goal_distance:
                        closest_goal = i
                        closest_goal_distance = distance
                if closest_goal in diamond_list:
                    diamond_list.remove(closest_goal)
                move_distance = 1000
                move_choice = moves[0]
                for m in moves:
                    distance = abs(m.destination.x - closest_goal.x) + abs(m.destination.y - closest_goal.y)
                    if distance < move_distance:  
                        move_distance = distance
                        move_choice = m
                if f"{pos.x},{pos.y}" in [f"{move_choice.destination.x},{move_choice.destination.y}"]:
                    choices = self.regular_move(possible_moves, game_state)
                    return choices
                choices.append(move_choice)
            return choices
                
                            
    def decide_moves(
        self, 
        possible_moves: dict[str, list[MoveAction]],
        game_state: GameState,        
        ) -> MoveAction:
        if game_state.turn < 20:
            choices = self.set_up_initial_diamond(possible_moves, game_state)
        else: 
            choices = self.regular_move(possible_moves, game_state)
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

                humans = []  # holds humans that are in range

                # Gather list of humans in range
                for a in attacks:
                    if a.type is AttackActionType.CHARACTER:
                        humans.append(a)

                if humans:  # Attack a random human in range
                    choices.append(random.choice(humans))
                else:  # No humans? Shame. The targets in range must be terrain. May as well attack one.
                    choices.append(random.choice(attacks))

            return choices
