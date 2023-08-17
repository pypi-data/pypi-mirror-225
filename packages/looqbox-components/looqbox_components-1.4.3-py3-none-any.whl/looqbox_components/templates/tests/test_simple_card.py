import unittest

from looqbox_components import SimpleCard


class TestJsonEncoder(unittest.TestCase):
    """
    Test Simple Card
    """

    def setUp(self) -> None:
        self.card_0 = SimpleCard("title", 0.5, 0.5, "tooltip", True, "#40db62", color="#40db62")

    def test_size_property(self):
        self.card_0.set_size(3)
        rendered_card = self.card_0._build_card()
        # TODO: refactor Container class to receive properties within self
        self.assertIn("col-md-3", rendered_card.properties.get("obj_class") or [])


if __name__ == '__main__':
    unittest.main()
