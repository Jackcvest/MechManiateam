from dataclasses import dataclass
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type
from game.util.position import Position


@dataclass
class Terrain:
    """
    Represents a piece of terrain
    """

    id: str
    position: Position
    health: int
    can_attack_through: bool

    def deserialize(blob: object) -> "Terrain":
        try:
            assert_blob_has_key_of_type(blob, "id", str)
            assert_blob_has_key_of_type(blob, "position", dict)
            assert_blob_has_key_of_type(blob, "health", int)
            assert_blob_has_key_of_type(blob, "canAttackThrough", bool)
            terrain = Terrain(
                blob["id"],
                Position.deserialize(blob["position"]),
                blob["health"],
                blob["canAttackThrough"],
            )
        except:
            print("Failed to validate Terrain json")
            raise

        return terrain
