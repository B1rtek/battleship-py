import random

from board import FieldStatus, return_all_field_coordinates
from fleet import Ship
from fleet_creator import FleetCreator, FCMessage


def test_fleet_creator_create():
    creator = FleetCreator()


def test_fleet_creator_start():
    creator = FleetCreator()
    creator.start()
    board = creator.get_board_display()
    ships = creator._fleet.ships()
    assert len(ships) == 10
    for ship in ships:
        for x, y in ship.get_segment_coordinates():
            assert board.get_field_status(x, y) == FieldStatus.SHIP


def test_fleet_creator_select_ship():
    creator = FleetCreator()
    creator.start()
    ships = creator._fleet.ships()
    all_fields = return_all_field_coordinates()
    for ship in ships:
        segment_positions = ship.get_segment_coordinates()
        for x, y in segment_positions:
            creator.select_ship(x, y)
            assert creator.get_selected_ship() == ship
            messages = creator.get_display_messages()
            assert len(messages) == 1
            assert FCMessage.SHIP_SELECTED in messages
            all_fields.remove((x, y))
    for x, y in all_fields:
        creator.select_ship(x, y)
        assert creator.get_selected_ship() is None


def test_fleet_creator_set_ship_position_success(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('a', 1)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.set_ship_position('g', 3)
    messages = creator.get_display_messages()
    assert not messages
    assert creator._fleet.ships()[0].origin() == ('g', 3)


def test_fleet_creator_set_ship_position_fail_collision(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('b', 3)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.set_ship_position('f', 4)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_MOVE_FAIL in messages
    assert creator._fleet.ships()[1].origin() == ('a', 3)


def test_fleet_creator_set_ship_position_fail_out_of_board(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('b', 3)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.set_ship_position('j', 8)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_MOVE_FAIL in messages
    assert creator._fleet.ships()[1].origin() == ('a', 3)


def test_fleet_creator_change_ship_rotation_success(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('g', 5)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.change_ship_rotation()
    messages = creator.get_display_messages()
    assert not messages
    assert creator._fleet.ships()[5].vertical()


def test_fleet_creator_change_ship_rotation_fail_collision(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('a', 1), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('d', 1)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.change_ship_rotation()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_ROTATION_FAIL in messages
    assert not creator._fleet.ships()[0].vertical()


def test_fleet_creator_change_ship_rotation_fail_out_of_board(monkeypatch):
    def rigged_fleet(self):
        self._ships.clear()
        ships = []
        ships.append(Ship(('d', 10), 4, False))
        ships.append(Ship(('a', 3), 3, False))
        ships.append(Ship(('a', 5), 3, False))
        ships.append(Ship(('a', 7), 2, False))
        ships.append(Ship(('a', 9), 2, False))
        ships.append(Ship(('f', 5), 2, False))
        ships.append(Ship(('f', 1), 1, False))
        ships.append(Ship(('h', 1), 1, False))
        ships.append(Ship(('j', 1), 1, False))
        ships.append(Ship(('j', 10), 1, False))
        self._ships = ships

    monkeypatch.setattr("fleet.Fleet.create_random", rigged_fleet)

    creator = FleetCreator()
    creator.start()
    creator.select_ship('d', 10)
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages
    creator.change_ship_rotation()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_ROTATION_FAIL in messages
    assert not creator._fleet.ships()[0].vertical()


def test_fleet_creator_random_fleet():
    creator = FleetCreator()
    creator.start()
    creator.random_fleet()
    board = creator.get_board_display()
    ships = creator._fleet.ships()
    assert len(ships) == 10
    for ship in ships:
        for x, y in ship.get_segment_coordinates():
            assert board.get_field_status(x, y) == FieldStatus.SHIP


def test_fleet_creator_setup_help():
    creator = FleetCreator()
    creator.setup_help()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SETUP_HELP in messages


def test_fleet_creator_contains_not_selected_ship():
    creator = FleetCreator()
    creator.start()
    ships = creator.get_setup()[1].ships()
    to_select = random.choice(ships)
    ship_poss = []
    for ship in ships:
        ship_poss += ship.get_segment_coordinates()
    for coords in to_select.get_segment_coordinates():
        ship_poss.remove(coords)
    all_fields = return_all_field_coordinates()
    for x, y in to_select.get_segment_coordinates():
        all_fields.remove((x, y))
        creator.select_ship(x, y)
    for x, y in all_fields:
        if (x, y) in ship_poss:
            assert creator.contains_not_selected_ship(x, y)
        else:
            assert not creator.contains_not_selected_ship(x, y)
    for x, y in to_select.get_segment_coordinates():
        assert not creator.contains_not_selected_ship(x, y)


def test_fleet_creator_message_ship_selected():
    creator = FleetCreator()
    creator._message_ship_selected()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_SELECTED in messages


def test_fleet_creator_message_move_fail():
    creator = FleetCreator()
    creator._message_ship_move_fail()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_MOVE_FAIL in messages


def test_fleet_creator_message_rotation_fail():
    creator = FleetCreator()
    creator._message_ship_rotation_fail()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SHIP_ROTATION_FAIL in messages


def test_fleet_creator_message_setup_help():
    creator = FleetCreator()
    creator._message_setup_help()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SETUP_HELP in messages


def test_fleet_creator_get_display_messages():
    creator = FleetCreator()
    creator._message_setup_help()
    messages = creator.get_display_messages()
    assert len(messages) == 1
    assert FCMessage.SETUP_HELP in messages
    assert not creator._messages
