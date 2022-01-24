import random

from board import return_all_field_coordinates, Board, FieldStatus
from fleet import ShipSegment, Ship, field_available, mark_misses_around, \
    Fleet, \
    fields_around_field, fields_around_ship


def test_ship_segment_create():
    segment = ShipSegment('b', 1)
    assert segment.position() == ('b', 1)
    assert not segment.sunk()


def test_ship_segment_sink():
    segment = ShipSegment('g', 7)
    assert not segment.sunk()
    segment.sink()
    assert segment.sunk()


def test_ship_segment_unsink():
    segment = ShipSegment('d', 10)
    segment.sink()
    segment.unsink()
    assert not segment.sunk()


def test_ship_create():
    ship = Ship(('f', 3), 4, False)
    segments = ship.segments()
    assert len(segments) == 4
    positions = [x.position() for x in segments]
    expected_segments = [('f', 3), ('g', 3), ('h', 3), ('i', 3)]
    for expected in expected_segments:
        assert expected in positions
    assert ship.size() == 4
    assert not ship.vertical()
    assert ship.origin() == ('f', 3)


def test_ship_create_vertical():
    ship = Ship(('g', 7), 3, True)
    segments = ship.segments()
    assert len(segments) == 3
    positions = [x.position() for x in segments]
    expected_segments = [('g', 7), ('g', 8), ('g', 9)]
    for expected in expected_segments:
        assert expected in positions
    assert ship.size() == 3
    assert ship.vertical()
    assert ship.origin() == ('g', 7)


def test_ship_get_segment_coordinates():
    ship = Ship(('f', 2), 3, True)
    expected_coordinates = [('f', 2), ('f', 3), ('f', 4)]
    positions = ship.get_segment_coordinates()
    for position in positions:
        assert position in expected_coordinates


def test_ship_check_if_belongs():
    ship = Ship(('g', 7), 3, True)
    expected_segments = [('g', 7), ('g', 8), ('g', 9)]
    for x, y in expected_segments:
        assert ship.check_if_belongs(x, y)


def test_ship_check_if_not_belongs():
    ship = Ship(('g', 7), 3, True)
    no_ship_fields = return_all_field_coordinates()
    expected_segments = [('g', 7), ('g', 8), ('g', 9)]
    for segment in expected_segments:
        no_ship_fields.remove(segment)
    for x, y in no_ship_fields:
        assert not ship.check_if_belongs(x, y)


def test_ship_sink():
    ship = Ship(('f', 3), 4, False)
    ship.sink('f', 3)
    segments = ship.segments()
    for segment in segments:
        if segment.position() == ('f', 3):
            assert segment.sunk()


def test_ship_sink_wrong_coordinates():
    ship = Ship(('b', 2), 2, True)
    ship.sink('a', 7)
    segments = ship.segments()
    for segment in segments:
        assert not segment.sunk()


def test_ship_sunk():
    ship = Ship(('b', 7), 4, False)
    assert not ship.sunk()


def test_ship_sunk_after_missed_shot():
    ship = Ship(('b', 7), 4, False)
    segments = ship.segments()
    for segment in segments:
        assert not segment.sunk()
    assert not ship.sunk()


def test_ship_sunk_after_hit():
    ship = Ship(('b', 7), 4, False)
    ship.sink('b', 7)
    segments = ship.segments()
    for segment in segments:
        if segment.position() != ('b', 7):
            assert not segment.sunk()
        else:
            assert segment.sunk()
    assert not ship.sunk()


def test_ship_sunk_after_all_hits():
    ship = Ship(('b', 7), 4, False)
    positions = ship.get_segment_coordinates()
    for x, y in positions:
        ship.sink(x, y)
    segments = ship.segments()
    for segment in segments:
        assert segment.sunk()
    assert ship.sunk()


def test_ship_ship_to_str_untouched():
    ship = Ship(('e', 2), 4, True)
    assert ship.ship_to_str() == "████"


def test_ship_ship_to_str_untouched_as_enemy():
    ship = Ship(('e', 2), 4, True)
    assert ship.ship_to_str(draw_as_enemy=True) == "████"


def test_ship_ship_to_str_hit():
    ship = Ship(('e', 2), 4, True)
    ship.sink('e', 3)
    ship.sink('e', 4)
    assert ship.ship_to_str() == "█▒▒█"


def test_ship_ship_to_str_hit_as_enemy():
    ship = Ship(('e', 2), 4, True)
    ship.sink('e', 3)
    assert ship.ship_to_str(draw_as_enemy=True) == "████"


def test_ship_ship_to_str_sunk():
    ship = Ship(('e', 2), 4, True)
    positions = ship.get_segment_coordinates()
    for x, y in positions:
        ship.sink(x, y)
    assert ship.sunk()
    assert ship.ship_to_str() == "▒▒▒▒"


def test_ship_ship_to_str_sunk_as_enemy():
    ship = Ship(('e', 2), 4, True)
    positions = ship.get_segment_coordinates()
    for x, y in positions:
        ship.sink(x, y)
    assert ship.sunk()
    assert ship.ship_to_str(draw_as_enemy=True) == "▒▒▒▒"


def test_field_available():
    board = Board()
    ship = Ship(('b', 7), 3, False)
    assert field_available(ship, board)


def test_field_available_ship_outside_board():
    board = Board()
    ship = Ship(('a', 9), 3, True)
    assert not field_available(ship, board)


def test_field_available_ship_colliding_with_other_ship():
    board = Board()
    placed_ship = Ship(('c', 6), 2, True)
    board.place_ship(placed_ship)
    ship = Ship(('b', 7), 3, False)
    assert not field_available(ship, board)


def test_field_available_ship_colliding_with_markers():
    board = Board()
    board.set_field_status('d', 7, FieldStatus.MISS)
    ship = Ship(('b', 7), 3, False)
    assert not field_available(ship, board)


def test_fields_around_field_typical():
    source = ('b', 5)
    expected = [('a', 4), ('a', 5), ('a', 6), ('b', 4), ('b', 6), ('c', 4),
                ('c', 5), ('c', 6)]
    fields_around = fields_around_field(source)
    assert len(fields_around) == 8
    for field in fields_around:
        assert field in expected


def test_fields_around_field_edge():
    source = ('a', 5)
    expected = [('`', 4), ('`', 5), ('`', 6), ('a', 4), ('a', 6), ('b', 4),
                ('b', 5), ('b', 6)]
    fields_around = fields_around_field(source)
    assert len(fields_around) == 8
    for field in fields_around:
        assert field in expected


def test_fields_around_field_corner():
    source = ('a', 1)
    expected = [('`', 0), ('`', 1), ('`', 2), ('a', 0), ('a', 2), ('b', 0),
                ('b', 1), ('b', 2)]
    fields_around = fields_around_field(source)
    assert len(fields_around) == len(expected)
    for field in fields_around:
        assert field in expected


def test_fields_around_ship_typical():
    ship = Ship(('c', 4), 2, True)
    fields_around = fields_around_ship(ship)
    expected = [('b', 3), ('c', 3), ('d', 3), ('b', 4), ('d', 4), ('b', 5),
                ('d', 5), ('b', 6), ('c', 6), ('d', 6)]
    assert len(fields_around) == len(expected)
    for field in fields_around:
        assert field in expected


def test_fields_around_ship_edge():
    ship = Ship(('a', 5), 2, True)
    fields_around = fields_around_ship(ship)
    expected = [('a', 4), ('a', 7), ('b', 4), ('b', 5), ('b', 6), ('b', 7)]
    assert len(fields_around) == len(expected)
    for field in fields_around:
        assert field in expected


def test_fields_around_ship_corner():
    ship = Ship(('a', 1), 2, True)
    fields_around = fields_around_ship(ship)
    expected = [('a', 3), ('b', 1), ('b', 2), ('b', 3)]
    assert len(fields_around) == len(expected)
    for field in fields_around:
        assert field in expected


def test_mark_misses_around_typical():
    board = Board()
    ship = Ship(('c', 4), 2, True)
    board.place_ship(ship)
    mark_misses_around(ship, board)
    fields_around = fields_around_ship(ship)
    other_fields = return_all_field_coordinates()
    for x, y in fields_around:
        other_fields.remove((x, y))
        assert board.get_field_status(x, y) == FieldStatus.MISS
    for x, y in other_fields:
        if (x, y) in ship.get_segment_coordinates():
            assert board.get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert board.get_field_status(x, y) == FieldStatus.NOTHING


def test_mark_misses_around_edge():
    board = Board()
    ship = Ship(('a', 5), 2, True)
    board.place_ship(ship)
    mark_misses_around(ship, board)
    fields_around = fields_around_ship(ship)
    other_fields = return_all_field_coordinates()
    for x, y in fields_around:
        other_fields.remove((x, y))
        assert board.get_field_status(x, y) == FieldStatus.MISS
    for x, y in other_fields:
        if (x, y) in ship.get_segment_coordinates():
            assert board.get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert board.get_field_status(x, y) == FieldStatus.NOTHING


def test_mark_misses_around_corner():
    board = Board()
    ship = Ship(('a', 1), 2, True)
    board.place_ship(ship)
    mark_misses_around(ship, board)
    fields_around = fields_around_ship(ship)
    other_fields = return_all_field_coordinates()
    for x, y in fields_around:
        other_fields.remove((x, y))
        assert board.get_field_status(x, y) == FieldStatus.MISS
    for x, y in other_fields:
        if (x, y) in ship.get_segment_coordinates():
            assert board.get_field_status(x, y) == FieldStatus.SHIP
        else:
            assert board.get_field_status(x, y) == FieldStatus.NOTHING


def test_fleet_create():
    fleet = Fleet()
    assert not fleet.ships()


def test_fleet_create_with_ships():
    ships = [Ship(('a', 2), 4, True), Ship(('g', 7), 2, False)]
    fleet = Fleet(ships)
    assert fleet.ships() == ships


def test_fleet_create_random():
    # this test takes a lot of time but it proves that it doesn't fail when
    # generating a completely random board
    fleet = Fleet()
    for i in range(100):
        fleet.create_random()
        temp_board = Board()
        temp_board.place_fleet(fleet)
        ships = fleet.ships()
        for ship in ships:
            fields_around = fields_around_ship(ship)
            for x, y in fields_around:
                assert temp_board.get_field_status(x, y) == FieldStatus.NOTHING


def test_fleet_hit():
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    x, y = ships[0].get_segment_coordinates()[0]
    sunk = fleet.hit(x, y)
    assert not sunk
    assert not ships[0].sunk()
    assert ships[0].segments()[0].sunk()


def test_fleet_hit_sink():
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    x, y = ships[9].get_segment_coordinates()[0]
    sunk = fleet.hit(x, y)
    assert sunk
    assert ships[9].sunk()
    assert ships[9].segments()[0].sunk()


def test_fleet_hit_miss():
    fleet = Fleet()
    fleet.create_random()
    all_ship_pos = []
    ships = fleet.ships()
    for ship in ships:
        all_ship_pos += ship.get_segment_coordinates()
    all_fields = return_all_field_coordinates()
    for field in all_ship_pos:
        all_fields.remove(field)
    x, y = random.choice(all_fields)
    sunk = fleet.hit(x, y)
    assert not sunk
    for ship in fleet.ships():
        for segment in ship.segments():
            assert not segment.sunk()


def test_fleet_find_ship():
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    all_fields = return_all_field_coordinates()
    for ship in ships:
        segment_positions = ship.get_segment_coordinates()
        for x, y in segment_positions:
            assert fleet.find_ship(x, y) == ship
            all_fields.remove((x, y))
    for x, y in all_fields:
        assert fleet.find_ship(x, y) is None


def test_fleet_select_ship():
    fleet = Fleet()
    fleet.create_random()
    ships = fleet.ships()
    all_fields = return_all_field_coordinates()
    for ship in ships:
        segment_positions = ship.get_segment_coordinates()
        for x, y in segment_positions:
            assert fleet.select_ship(x, y)
            assert fleet.selected_ship() == ship
            all_fields.remove((x, y))
    for x, y in all_fields:
        assert not fleet.select_ship(x, y)
        assert fleet.selected_ship() is None


def test_fleet_new_ship_test_fit_success(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('a', 1)
    new_ship = Ship(('e', 9), 4, False)
    assert fleet._new_ship_test_fit(new_ship) == 0


def test_fleet_new_ship_test_fit_fail_collision(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('a', 1)
    new_ship = Ship(('f', 10), 4, False)
    assert fleet._new_ship_test_fit(new_ship) == -1


def test_fleet_new_ship_test_fit_fail_out_of_board(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('a', 1)
    new_ship = Ship(('i', 7), 4, False)
    assert fleet._new_ship_test_fit(new_ship) == -1


def test_fleet_set_ship_position_success(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('b', 3)
    assert fleet.set_ship_position('d', 10)
    assert fleet.ships()[1].origin() == ('d', 10)
    assert fleet.selected_ship().origin() == ('d', 10)


def test_fleet_set_ship_position_fail_collision(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('b', 3)
    assert not fleet.set_ship_position('f', 4)
    assert fleet.ships()[1].origin() == ('a', 3)
    assert fleet.selected_ship().origin() == ('a', 3)


def test_fleet_set_ship_position_fail_out_of_board(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('b', 3)
    assert not fleet.set_ship_position('i', 5)
    assert fleet.ships()[1].origin() == ('a', 3)
    assert fleet.selected_ship().origin() == ('a', 3)


def test_fleet_change_ship_rotation_success(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('f', 5)
    assert fleet.change_ship_rotation()
    assert fleet.ships()[5].vertical()
    assert fleet.selected_ship().vertical()


def test_fleet_change_ship_rotation_fail_collision(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('a', 1)
    assert not fleet.change_ship_rotation()
    assert not fleet.ships()[0].vertical()
    assert not fleet.selected_ship().vertical()


def test_fleet_change_ship_rotation_fail_out_of_board(monkeypatch):
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

    fleet = Fleet()
    fleet.create_random()
    fleet.select_ship('e', 10)
    assert not fleet.change_ship_rotation()
    assert not fleet.ships()[0].vertical()
    assert not fleet.selected_ship().vertical()


def test_fleet_is_alive():
    fleet = Fleet()
    fleet.create_random()
    all_fields = return_all_field_coordinates()
    for ship in fleet.ships():
        for x, y in ship.get_segment_coordinates():
            all_fields.remove((x, y))
    for x, y in all_fields:
        assert not fleet.hit(x, y)
        assert fleet.is_alive()
    for index, ship in enumerate(fleet.ships()):
        for ship_num, pos in enumerate(ship.get_segment_coordinates()):
            x, y = pos
            fleet.hit(x, y)
            if index == 9:
                assert not fleet.is_alive()
            else:
                assert fleet.is_alive()
    assert not fleet.is_alive()


def test_fleet_fleet_to_str_untouched():
    fleet = Fleet()
    fleet.create_random()
    assert fleet.fleet_to_str() == "████ ███ ███ █\n" \
                                   "██ ██ ██ █ █ █"


def test_fleet_fleet_to_str_untouched_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    assert fleet.fleet_to_str(draw_as_enemy=True) == "████ ███ ███ █\n" \
                                                     "██ ██ ██ █ █ █"


def test_fleet_fleet_to_str_hit():
    fleet = Fleet()
    fleet.create_random()
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[1])
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[2])
    fleet.hit(*fleet.ships()[9].get_segment_coordinates()[0])
    fleet.hit(*fleet.ships()[6].get_segment_coordinates()[0])
    assert fleet.fleet_to_str() == "█▒▒█ ███ ███ ▒\n" \
                                   "██ ██ ██ ▒ █ █"


def test_fleet_fleet_to_str_hit_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[1])
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[2])
    fleet.hit(*fleet.ships()[9].get_segment_coordinates()[0])
    fleet.hit(*fleet.ships()[6].get_segment_coordinates()[0])
    assert fleet.fleet_to_str(draw_as_enemy=True) == "████ ███ ███ ▒\n" \
                                                     "██ ██ ██ ▒ █ █"


def test_fleet_fleet_to_str_sunk():
    fleet = Fleet()
    fleet.create_random()
    for ship in fleet.ships():
        for x, y in ship.get_segment_coordinates():
            fleet.hit(x, y)
    assert fleet.fleet_to_str() == "▒▒▒▒ ▒▒▒ ▒▒▒ ▒\n" \
                                   "▒▒ ▒▒ ▒▒ ▒ ▒ ▒"


def test_fleet_fleet_to_str_sunk_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    for ship in fleet.ships():
        for x, y in ship.get_segment_coordinates():
            fleet.hit(x, y)
    assert fleet.fleet_to_str(draw_as_enemy=True) == "▒▒▒▒ ▒▒▒ ▒▒▒ ▒\n" \
                                                     "▒▒ ▒▒ ▒▒ ▒ ▒ ▒"


def test_fleet_get_display_fleet_untouched():
    fleet = Fleet()
    fleet.create_random()
    display_fleet = fleet.get_display_fleet()
    for ship, display_ship in zip(fleet.ships(), display_fleet.ships()):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment, display_segment in zip(ship.segments(),
                                            display_ship.segments()):
            assert segment.sunk() == display_segment.sunk()
            assert segment.position() == display_segment.position()


def test_fleet_get_display_fleet_untouched_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    display_fleet = fleet.get_display_fleet(display_as_enemy=True)
    for ship, display_ship in zip(fleet.ships(), display_fleet.ships()):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment, display_segment in zip(ship.segments(),
                                            display_ship.segments()):
            assert segment.sunk() == display_segment.sunk()
            assert segment.position() == display_segment.position()


def test_fleet_get_display_fleet_hit():
    fleet = Fleet()
    fleet.create_random()
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[1])
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[2])
    fleet.hit(*fleet.ships()[9].get_segment_coordinates()[0])
    fleet.hit(*fleet.ships()[6].get_segment_coordinates()[0])
    display_fleet = fleet.get_display_fleet()
    for ship, display_ship in zip(fleet.ships(), display_fleet.ships()):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment, display_segment in zip(ship.segments(),
                                            display_ship.segments()):
            assert segment.sunk() == display_segment.sunk()
            assert segment.position() == display_segment.position()


def test_fleet_get_display_fleet_hit_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[1])
    fleet.hit(*fleet.ships()[0].get_segment_coordinates()[2])
    fleet.hit(*fleet.ships()[9].get_segment_coordinates()[0])
    fleet.hit(*fleet.ships()[6].get_segment_coordinates()[0])
    display_fleet = fleet.get_display_fleet(display_as_enemy=True)
    for ship_num, (ship, display_ship) in enumerate(
            zip(fleet.ships(), display_fleet.ships())):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment_num, (segment, display_segment) in enumerate(
                zip(ship.segments(), display_ship.segments())):
            if ship_num == 0 and 1 <= segment_num <= 2:
                assert not segment.sunk() == display_segment.sunk()
                assert segment.sunk()
            assert segment.position() == display_segment.position()


def test_fleet_get_display_fleet_sunk():
    fleet = Fleet()
    fleet.create_random()
    for ship in fleet.ships():
        for x, y in ship.get_segment_coordinates():
            fleet.hit(x, y)
    display_fleet = fleet.get_display_fleet()
    for ship, display_ship in zip(fleet.ships(), display_fleet.ships()):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment, display_segment in zip(ship.segments(),
                                            display_ship.segments()):
            assert segment.sunk() == display_segment.sunk()
            assert segment.position() == display_segment.position()
            assert segment.sunk()


def test_fleet_get_display_fleet_sunk_as_enemy():
    fleet = Fleet()
    fleet.create_random()
    for ship in fleet.ships():
        for x, y in ship.get_segment_coordinates():
            fleet.hit(x, y)
    display_fleet = fleet.get_display_fleet(display_as_enemy=True)
    for ship, display_ship in zip(fleet.ships(), display_fleet.ships()):
        assert ship.origin() == display_ship.origin()
        assert ship.vertical() == display_ship.vertical()
        assert ship.size() == display_ship.size()
        assert ship.sunk() == display_ship.sunk()
        for segment, display_segment in zip(ship.segments(),
                                            display_ship.segments()):
            assert segment.sunk() == display_segment.sunk()
            assert segment.position() == display_segment.position()
            assert segment.sunk()
