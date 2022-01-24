import random
from copy import deepcopy

from board import return_all_field_coordinates, FieldStatus, field_on_board
from enemy import create_list_of_tangents
from fleet import fields_around_ship
from fleet_creator import FleetCreator
from game import Game, GameMessage
from settings import Setting, Settings


def test_game_create():
    game = Game()
    assert game._player_board is None
    assert game._enemy_board is None
    assert game._player_fleet is None
    assert game._enemy_fleet is None
    assert game._enemy is None
    assert game.players_turn()
    assert not game.won()
    assert not game._messages
    assert game._settings[Setting.MARK_MISSES_AROUND]
    assert not game._settings[Setting.HARD_ENEMY]


def test_game_apply_settings_none():
    game = Game()
    game.apply_settings()
    assert game._settings[Setting.MARK_MISSES_AROUND]
    assert not game._settings[Setting.HARD_ENEMY]


def test_game_apply_settings_custom():
    game = Game()
    settings = Settings()
    settings.set_hard_enemy(True)
    game.apply_settings(settings.get_settings())
    assert game._settings[Setting.MARK_MISSES_AROUND]
    assert game._settings[Setting.HARD_ENEMY]


def test_game_create_enemy_fleet():
    game = Game()
    assert game._enemy_fleet is None
    assert game._enemy_board is None
    game._create_enemy_fleet()
    assert game._enemy_fleet is not None
    assert game._enemy_board is not None


def test_game_start_game():
    creator = FleetCreator()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    assert game._player_board._data_board == board
    assert not game._enemy._hard_mode
    assert game._player_fleet == fleet
    assert game._enemy_fleet is not None
    assert game._enemy_board is not None
    assert game.players_turn()
    assert not game.won()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYERS_TURN in messages


def test_game_discover_field_miss():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    assert game._enemy_board._visible_board. \
        get_field_status(x, y) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_MISS in messages
    assert not game.players_turn()


def test_game_discover_field_hit():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    x, y = game._enemy_fleet.ships()[0].get_segment_coordinates()[0]
    assert game.discover_field(x, y)
    assert game._enemy_board._visible_board. \
        get_field_status(x, y) == FieldStatus.SHIP
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_SHIP_HIT in messages
    assert game.players_turn()


def test_game_discover_field_sink():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    settings = Settings()
    settings.set_mark_misses_around(False)
    game.apply_settings(settings.get_settings())
    game.start_game(board, fleet)
    game.get_display_messages()
    x, y = game._enemy_fleet.ships()[9].get_segment_coordinates()[0]
    assert game.discover_field(x, y)
    assert game._enemy_board._visible_board. \
        get_field_status(x, y) == FieldStatus.SUNK
    fields_around = fields_around_ship(game._enemy_fleet.ships()[9])
    for x, y in fields_around:
        assert game._enemy_board._visible_board. \
                   get_field_status(x, y) == FieldStatus.NOTHING
    messages = game.get_display_messages()
    assert len(messages) == 2
    assert GameMessage.ENEMY_SHIP_HIT in messages
    assert GameMessage.ENEMY_SHIP_SUNK in messages
    assert game.players_turn()


def test_game_discover_field_sink_mark_misses():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    x, y = game._enemy_fleet.ships()[9].get_segment_coordinates()[0]
    assert game.discover_field(x, y)
    assert game._enemy_board._visible_board. \
        get_field_status(x, y) == FieldStatus.SUNK
    fields_around = fields_around_ship(game._enemy_fleet.ships()[9])
    for x, y in fields_around:
        assert game._enemy_board._visible_board. \
                   get_field_status(x, y) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert len(messages) == 2
    assert GameMessage.ENEMY_SHIP_HIT in messages
    assert GameMessage.ENEMY_SHIP_SUNK in messages
    assert game.players_turn()


def test_game_discover_field_win():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    messages = game.get_display_messages()
    ship_poss = []
    for ship in game._enemy_fleet.ships():
        ship_poss += ship.get_segment_coordinates()
    for x, y in ship_poss:
        assert game.discover_field(x, y)
        messages = game.get_display_messages()
        assert GameMessage.ENEMY_SHIP_HIT in messages
    assert GameMessage.PLAYER_WIN in messages
    assert game.won()
    assert game.check_win()


def test_game_discover_field_not_players_turn():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    game.discover_field(x, y)
    game.get_display_messages()
    misses.remove((x, y))
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.NOT_PLAYERS_TURN in messages


def test_game_discover_field_not_on_board():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    assert game.discover_field('v', 0)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.INVALID_COORDS in messages


def test_game_discover_field_already_discovered():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    x, y = game._enemy_fleet.ships()[0].get_segment_coordinates()[0]
    game.discover_field(x, y)
    game.get_display_messages()
    game.discover_field(x, y)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_ALREADY_DISCOVERED in messages


def test_game_mark_field():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.mark_field('a', 1)
    assert game._enemy_board._visible_board. \
        get_field_status('a', 1) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert not messages


def test_game_mark_field_fail_not_on_board():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.mark_field('a', 0)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.INVALID_COORDS in messages


def test_game_mark_field_fail_not_empty():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.mark_field('a', 1)
    game.get_display_messages()
    game.mark_field('a', 1)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_MARK_FAIL in messages


def test_game_unmark_field():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.mark_field('a', 1)
    assert game._enemy_board._visible_board. \
        get_field_status('a', 1) == FieldStatus.MISS
    game.get_display_messages()
    game.unmark_field('a', 1)
    assert game._enemy_board._visible_board. \
        get_field_status('a', 1) == FieldStatus.NOTHING
    messages = game.get_display_messages()
    assert not messages


def test_game_unmark_field_fail_not_on_board():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.unmark_field('a', 0)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.INVALID_COORDS in messages


def test_game_unmark_field_fail_not_marked():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.unmark_field('a', 1)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_UNMARK_FAIL in messages


def test_game_game_help():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    game.get_display_messages()
    game.game_help()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.GAME_HELP in messages


def test_game_enemy_move_players_turn():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    assert not game.enemy_move()


def test_game_enemy_move_miss(monkeypatch):
    def rigged_shoot(self):
        return misses_for_enemy[0]

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    game.get_display_messages()
    misses_for_enemy = return_all_field_coordinates()
    ships = fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses_for_enemy.remove(coords)
    assert not game.enemy_move()
    x, y = misses_for_enemy[0]
    assert game._player_board._visible_board. \
        get_field_status(x, y) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_MISS in messages


def test_game_enemy_move_hit(monkeypatch):
    def rigged_shoot(self):
        self._last_target = guaranteed_hit
        return guaranteed_hit

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    game.get_display_messages()
    guaranteed_hit = fleet.ships()[0].get_segment_coordinates()[0]
    x, y = guaranteed_hit
    assert game.enemy_move()
    assert game._player_board._visible_board. \
        get_field_status(x, y) == FieldStatus.SHIP
    assert game._player_board._data_board. \
        get_field_status(x, y) == FieldStatus.SUNK
    tangents = create_list_of_tangents(guaranteed_hit)
    for a, b in tangents:
        if field_on_board((a, b)):
            assert game._player_board._visible_board. \
                get_field_status(a, b) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_SHIP_HIT in messages


def test_game_enemy_move_sink(monkeypatch):
    def rigged_shoot(self):
        self._last_target = guaranteed_sink
        return guaranteed_sink

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    game.get_display_messages()
    guaranteed_sink = fleet.ships()[9].get_segment_coordinates()[0]
    x, y = guaranteed_sink
    assert game.enemy_move()
    assert game._player_board._visible_board. \
        get_field_status(x, y) == FieldStatus.SUNK
    assert game._player_board._data_board. \
        get_field_status(x, y) == FieldStatus.SUNK
    around = fields_around_ship(fleet.ships()[9])
    for a, b in around:
        assert game._player_board._visible_board. \
                   get_field_status(a, b) == FieldStatus.MISS
    messages = game.get_display_messages()
    assert len(messages) == 2
    assert GameMessage.PLAYER_SHIP_HIT in messages
    assert GameMessage.PLAYER_SHIP_SUNK in messages


def test_game_enemy_move_win(monkeypatch):
    def rigged_shoot(self):
        self._last_target = target
        return target

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    game.get_display_messages()
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    messages = game.get_display_messages()
    guaranteed_sinks = []
    target = ('`', 0)
    for ship in fleet.ships():
        guaranteed_sinks += ship.get_segment_coordinates()
    for guaranteed in guaranteed_sinks:
        target = guaranteed
        assert game.enemy_move()
        messages = game.get_display_messages()
        assert GameMessage.PLAYER_SHIP_HIT in messages
    assert GameMessage.ENEMY_WIN in messages
    assert game.won()
    assert not game.check_win()
    for ship in fleet.ships():
        around = fields_around_ship(ship)
        for x, y in around:
            assert game._player_board._visible_board. \
                       get_field_status(x, y) == FieldStatus.MISS


def test_game_check_win():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    assert game.check_win() is None
    # the other situations are tested in test_game_discover_field_win() and
    # test_game_enemy_move_win()


def test_game_message_not_players_turn():
    game = Game()
    game._message_not_players_turn()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.NOT_PLAYERS_TURN in messages


def test_game_message_invalid_coordinates():
    game = Game()
    game._message_invalid_coordinates()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.INVALID_COORDS in messages


def test_game_message_enemy_ship_hit():
    game = Game()
    game._message_enemy_ship_hit()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_SHIP_HIT in messages


def test_game_message_enemy_ship_sunk():
    game = Game()
    game._message_enemy_ship_sunk()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_SHIP_SUNK in messages


def test_game_message_enemy_miss():
    game = Game()
    game._message_enemy_miss()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_MISS in messages


def test_game_message_enemy_win():
    game = Game()
    game._message_enemy_win()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.ENEMY_WIN in messages


def test_game_message_field_mark_fail():
    game = Game()
    game._message_field_mark_fail()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_MARK_FAIL in messages


def test_game_message_field_unmark_fail():
    game = Game()
    game._message_field_unmark_fail()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_UNMARK_FAIL in messages


def test_game_message_game_help():
    game = Game()
    game._message_game_help()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.GAME_HELP in messages


def test_game_message_player_ship_hit():
    game = Game()
    game._message_player_ship_hit()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_SHIP_HIT in messages


def test_game_message_player_ship_sunk():
    game = Game()
    game._message_player_ship_sunk()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_SHIP_SUNK in messages


def test_game_message_player_miss():
    game = Game()
    game._message_player_miss()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_MISS in messages


def test_game_message_player_win():
    game = Game()
    game._message_player_win()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYER_WIN in messages


def test_game_message_field_already_discovered():
    game = Game()
    game._message_field_already_discovered()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.FIELD_ALREADY_DISCOVERED in messages


def test_game_message_players_turn():
    game = Game()
    game._message_players_turn()
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYERS_TURN in messages


def test_game_game_get_display_messages():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    messages = game.get_display_messages()
    assert len(messages) == 1
    assert GameMessage.PLAYERS_TURN in messages
    assert not game._messages


def test_game_get_player_board_display(monkeypatch):
    def rigged_shoot(self):
        self._last_target = list_for_enemy[0]
        list_for_enemy.remove(self._last_target)
        return self._last_target

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    list_for_enemy = []
    misses_for_enemy = return_all_field_coordinates()
    ships = fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses_for_enemy.remove(coords)
    list_for_enemy.append(fleet.ships()[9].get_segment_coordinates()[0])
    list_for_enemy.append(fleet.ships()[0].get_segment_coordinates()[0])
    list_for_enemy.append(misses_for_enemy[0])
    shoot_list = deepcopy(list_for_enemy)
    for _ in shoot_list:
        game.enemy_move()
    display_board = game.get_player_board_display()
    all_other_fields = return_all_field_coordinates()
    for field in shoot_list:
        all_other_fields.remove(field)
    fields_with_ships = []
    for ship in fleet.ships():
        fields_with_ships += ship.get_segment_coordinates()
    for field in fields_with_ships:
        if field in all_other_fields:
            all_other_fields.remove(field)
    fields_with_ships.remove(shoot_list[0])
    fields_with_ships.remove(shoot_list[1])
    assert display_board.get_field_status(*shoot_list[0]) == FieldStatus.SUNK
    assert display_board.get_field_status(*shoot_list[1]) == FieldStatus.SUNK
    assert display_board.get_field_status(*shoot_list[2]) == FieldStatus.MISS
    for x, y in fields_around_ship(fleet.ships()[9]):
        assert display_board.get_field_status(x, y) == FieldStatus.MISS
        if (x, y) in all_other_fields:
            all_other_fields.remove((x, y))
    for x, y in create_list_of_tangents(shoot_list[1]):
        if field_on_board((x, y)):
            assert display_board.get_field_status(x, y) == FieldStatus.MISS
            if (x, y) in all_other_fields:
                all_other_fields.remove((x, y))
    for x, y in fields_with_ships:
        assert display_board.get_field_status(x, y) == FieldStatus.SHIP
    for x, y in all_other_fields:
        assert display_board.get_field_status(x, y) == FieldStatus.NOTHING


def test_game_get_enemy_board_display():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    settings = Settings()
    settings.set_mark_misses_around(False)
    game.apply_settings(settings.get_settings())
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    shoot_list = [game._enemy_fleet.ships()[0].get_segment_coordinates()[0],
                  game._enemy_fleet.ships()[9].get_segment_coordinates()[0],
                  misses[0]]
    for x, y in shoot_list:
        game.discover_field(x, y)
    all_other_fields = return_all_field_coordinates()
    for field in shoot_list:
        all_other_fields.remove(field)
    display_board = game.get_enemy_board_display()
    assert display_board.get_field_status(*shoot_list[0]) == FieldStatus.SHIP
    assert display_board.get_field_status(*shoot_list[1]) == FieldStatus.SUNK
    assert display_board.get_field_status(*shoot_list[2]) == FieldStatus.MISS
    for field in all_other_fields:
        assert display_board.get_field_status(*field) == FieldStatus.NOTHING


def test_game_get_player_fleet_display(monkeypatch):
    def rigged_shoot(self):
        self._last_target = list_for_enemy[0]
        list_for_enemy.remove(self._last_target)
        return self._last_target

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    x, y = random.choice(misses)
    assert not game.discover_field(x, y)
    list_for_enemy = []
    misses_for_enemy = return_all_field_coordinates()
    ships = fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses_for_enemy.remove(coords)
    list_for_enemy.append(fleet.ships()[9].get_segment_coordinates()[0])
    list_for_enemy.append(fleet.ships()[0].get_segment_coordinates()[0])
    list_for_enemy.append(misses_for_enemy[0])
    shoot_list = deepcopy(list_for_enemy)
    for _ in shoot_list:
        game.enemy_move()
    fleet_display = game.get_player_fleet_display()
    for ship_num, ship in enumerate(fleet_display.ships()):
        for segment_num, segment in enumerate(ship.segments()):
            if (ship_num == 0 and segment_num == 0) or ship_num == 9:
                assert segment.sunk()
            else:
                assert not segment.sunk()


def test_game_get_enemy_fleet_display():
    creator = FleetCreator()
    creator.start()
    board, fleet = creator.get_setup()
    game = Game()
    settings = Settings()
    settings.set_mark_misses_around(False)
    game.apply_settings(settings.get_settings())
    game.start_game(board, fleet)
    misses = return_all_field_coordinates()
    ships = game._enemy_fleet.ships()
    for ship in ships:
        for coords in ship.get_segment_coordinates():
            misses.remove(coords)
    shoot_list = [game._enemy_fleet.ships()[0].get_segment_coordinates()[0],
                  game._enemy_fleet.ships()[9].get_segment_coordinates()[0],
                  misses[0]]
    for x, y in shoot_list:
        game.discover_field(x, y)
    fleet_display = game.get_enemy_fleet_display()
    for ship_num, ship in enumerate(fleet_display.ships()):
        for segment_num, segment in enumerate(ship.segments()):
            if ship_num == 9:
                assert segment.sunk()
            else:
                assert not segment.sunk()
