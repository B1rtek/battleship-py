from board import Field, FieldStatus, game_to_array_coords


def test_field_create():
    field = Field()
    assert field.status() == FieldStatus.NOTHING


def test_field_set_status():
    field = Field()
    assert field.status() == FieldStatus.NOTHING
    field.set_status(FieldStatus.MISS)
    assert field.status() == FieldStatus.MISS


def test_field_str_nothing():
    field = Field()
    assert str(field) == ' '


def test_field_str_miss():
    field = Field()
    field.set_status(FieldStatus.MISS)
    assert str(field) == '.'


def test_field_str_ship():
    field = Field()
    field.set_status(FieldStatus.SHIP)
    assert str(field) == '█'


def test_field_str_sunk():
    field = Field()
    field.set_status(FieldStatus.SUNK)
    assert str(field) == '▒'


def test_field_str_selected():
    field = Field()
    field.set_status(FieldStatus.SELECTED)
    assert str(field) == '#'


def test_game_to_array_coords_typical():
    assert game_to_array_coords('a', 1) == (0, 0)


def test_game_to_array_coords_edge_case():
    assert game_to_array_coords('j', 10) == (9, 9)


def test_game_to_array_coords_not_on_board():