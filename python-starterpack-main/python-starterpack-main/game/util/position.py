from dataclasses import dataclass

from game.util.assert_blob_has_key_of_type import assert_blob_has_key_of_type


@dataclass
class Position:
    """
    Represents a position in a two-dimensional space
    """

    x: int
    y: int

    def deserialize(blob: object) -> "Position":
        try:
            assert_blob_has_key_of_type(blob, "x", int)
            assert_blob_has_key_of_type(blob, "y", int)
            position = Position(blob["x"], blob["y"])
        except:
            print("Failed to validate Position json")
            raise

        return position

    def serialize(self) -> dict[str, object]:
        return {
            "x": self.x,
            "y": self.y,
        }
