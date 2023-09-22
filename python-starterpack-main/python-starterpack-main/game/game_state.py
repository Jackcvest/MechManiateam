from dataclasses import dataclass
from game.character.character import Character
from game.terrain.terrain import Terrain
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type


@dataclass
class GameState:
    turn: int
    characters: dict[str, Character]
    terrains: dict[str, Terrain]

    def deserialize(blob: object) -> "GameState":
        try:
            assert_blob_has_key_of_type(blob, "turn", int)
            assert_blob_has_key_of_type(blob, "characterStates", dict)
            assert_blob_has_key_of_type(blob, "terrainStates", dict)

            turn = blob["turn"]

            raw_characters: dict = blob["characterStates"]
            raw_terrain: dict = blob["terrainStates"]

            characters: dict[str, Character] = dict()
            terrains: dict[str, Terrain] = dict()

            for [id, character_blob] in raw_characters.items():
                character = Character.deserialize(character_blob)

                if character:
                    characters[id] = character

            for [id, terrain_blob] in raw_terrain.items():
                terrain = Terrain.deserialize(terrain_blob)

                if terrain:
                    terrains[id] = terrain
        except:
            print("Failed to validate Game State json")
            raise

        return GameState(turn, characters, terrains)
