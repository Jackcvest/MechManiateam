from dataclasses import asdict, dataclass
import json
from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type
from game.util.position import Position


@dataclass
class MoveAction:
    """
    Defines where a character will move
    """

    executing_character_id: str
    destination: Position

    def deserialize(blob: object) -> "MoveAction":
        try:
            assert_blob_has_key_of_type(blob, "executingCharacterId", str)
            assert_blob_has_key_of_type(blob, "destination", dict)
            action = MoveAction(
                blob["executingCharacterId"],
                Position.deserialize(blob["destination"]),
            )
        except:
            print("Failed to validate MoveAction json")
            raise

        return action

    def serialize(self) -> dict[str, object]:
        return {
            "executingCharacterId": self.executing_character_id,
            "destination": self.destination.serialize(),
        }
