import random

from board import return_all_field_coordinates
from enemy import create_list_of_adherent, create_list_of_tangents, \
    upper_field, lower_field, left_field, right_field, Enemy


def test_create_list_of_adherent_typical():
    source = ('b', 5)
    adherent = create_list_of_adherent(source)
    assert len(adherent) == 4
    assert ('a', 5) in adherent
    assert ('c', 5) in adherent
    assert ('b', 4) in adherent
    assert ('b', 6) in adherent


def test_create_list_of_adherent_edge():
    source = ('j', 5)
    adherent = create_list_of_adherent(source)
    assert len(adherent) == 4
    assert ('i', 5) in adherent
    assert ('k', 5) in adherent
    assert ('j', 4) in adherent
    assert ('j', 6) in adherent
    # (k, 5) is a valid position, since it will be ignored by the enemy anyways


def test_create_list_of_adherent_corner():
    source = ('a', 1)
    adherent = create_list_of_adherent(source)
    assert len(adherent) == 4
    assert ('`', 1) in adherent
    assert ('b', 1) in adherent
    assert ('a', 0) in adherent
    assert ('a', 2) in adherent
    # again, (`, 1) and (a, 0) are valid because they will be ignored


def test_create_list_of_tangents_typical():
    source = ('b', 5)
    tangent = create_list_of_tangents(source)
    assert len(tangent) == 4
    assert ('a', 4) in tangent
    assert ('c', 4) in tangent
    assert ('a', 6) in tangent
    assert ('c', 6) in tangent


def test_create_list_of_tangents_edge():
    source = ('j', 5)
    tangent = create_list_of_tangents(source)
    assert len(tangent) == 4
    assert ('i', 4) in tangent
    assert ('i', 4) in tangent
    assert ('k', 6) in tangent
    assert ('k', 6) in tangent
    # again, (k, 4) and (k, 6) will be ignored by the enemy


def test_create_list_of_tangents_corner():
    source = ('a', 1)
    tangent = create_list_of_tangents(source)
    assert len(tangent) == 4
    assert ('`', 0) in tangent
    assert ('b', 0) in tangent
    assert ('`', 2) in tangent
    assert ('b', 2) in tangent
    # (`, 0), (b, 0) and (`, 2) will be ignored by the enemy


def test_upper_field():
    coords = ('b', 5)
    assert upper_field(coords) == ('b', 4)


def test_upper_field_edge():
    coords = ('b', 1)
    assert upper_field(coords) == ('b', 0)
    # (b, 0) will be ignored, or in the harder enemy's methods, will break the
    # loop counting fields up from the analyzed one


def test_lower_field():
    coords = ('b', 5)
    assert lower_field(coords) == ('b', 6)


def test_lower_field_edge():
    coords = ('b', 10)
    assert lower_field(coords) == ('b', 11)
    # again, this value will be ignored or it will break a loop


def test_left_field():
    coords = ('b', 5)
    assert left_field(coords) == ('a', 5)


def test_left_field_edge():
    coords = ('a', 5)
    assert left_field(coords) == ('`', 5)
    # this value will be ignored or it will break a loop


def test_right_field():
    coords = ('b', 5)
    assert right_field(coords) == ('c', 5)


def test_right_field_edge():
    coords = ('j', 5)
    assert right_field(coords) == ('k', 5)
    # as stated above, in test_left_field_edge()


def test_enemy_create():
    Enemy()


def test_enemy_create_hard():
    Enemy(hard_mode=True)


def test_enemy_shoot():
    all_fields = return_all_field_coordinates()
    enemy = Enemy()
    assert enemy.shoot() in all_fields


def test_enemy_hard_shoot():
    all_fields = return_all_field_coordinates()
    enemy = Enemy(hard_mode=True)
    assert enemy.shoot() in all_fields


def test_enemy_shoot_all():
    all_fields = return_all_field_coordinates()
    enemy = Enemy()
    for i in range(len(all_fields)):
        shot = enemy.shoot()
        assert shot in all_fields
        all_fields.remove(shot)
    assert not all_fields


def test_enemy_hard_shoot_all():
    all_fields = return_all_field_coordinates()
    enemy = Enemy(hard_mode=True)
    for i in range(len(all_fields)):
        shot = enemy.shoot()
        assert shot in all_fields
        all_fields.remove(shot)
    assert not all_fields


def test_enemy_rank_fields_and_choose_first_shot():
    all_fields = return_all_field_coordinates()
    enemy = Enemy()
    assert enemy._rank_fields_and_choose() in all_fields


def test_enemy_rank_fields_and_choose_after_two_shots(monkeypatch):
    def rigged_shoot(self):
        if len(self._undiscovered) == 100:
            chosen = ('d', 3)
            self._undiscovered.remove(chosen)
            return chosen
        elif len(self._undiscovered) == 99:
            chosen = ('e', 4)
            self._undiscovered.remove(chosen)
            return chosen

    monkeypatch.setattr("enemy.Enemy.shoot", rigged_shoot)

    enemy = Enemy()
    enemy.shoot()
    enemy.shoot()
    for i in range(100):
        assert enemy._rank_fields_and_choose() not in [('d', 4), ('e', 3)]
        # these fields will never be chosen because the potential longest ship
        # in their columns and rows is shorter than the one that can fit in all
        # other fields, only the fields with the highest rank will be taken
        # into the account while choosing the next target


def test_enemy_react_to_hit_typical(monkeypatch):
    target = ('b', 5)

    def rigged_shoot(self):
        self._undiscovered.remove(target)
        self._last_target = target
        return target

    monkeypatch.setattr('enemy.Enemy.shoot', rigged_shoot)

    enemy = Enemy()
    enemy.shoot()
    enemy.react_to_hit()
    assert len(enemy._to_shoot) == 4
    adherent = create_list_of_adherent(target)
    for field in adherent:
        assert field in enemy._to_shoot
    assert len(enemy._to_mark_as_empty) == 4
    tangents = create_list_of_tangents(target)
    for field in tangents:
        assert field in enemy._to_mark_as_empty


def test_enemy_react_to_hit_edge(monkeypatch):
    target = ('a', 5)

    def rigged_shoot(self):
        self._undiscovered.remove(target)
        self._last_target = target
        return target

    monkeypatch.setattr('enemy.Enemy.shoot', rigged_shoot)

    enemy = Enemy()
    enemy.shoot()
    enemy.react_to_hit()

    assert len(enemy._to_shoot) == 3
    adherent = create_list_of_adherent(target)
    for field in adherent:
        if field == ('`', 5):
            continue
        assert field in enemy._to_shoot
    assert len(enemy._to_mark_as_empty) == 2
    tangents = create_list_of_tangents(target)
    for field in tangents:
        if field == ('`', 4) or field == ('`', 6):
            assert field not in enemy._to_mark_as_empty
        else:
            assert field in enemy._to_mark_as_empty


def test_enemy_react_to_hit_corner(monkeypatch):
    target = ('a', 1)

    def rigged_shoot(self):
        self._undiscovered.remove(target)
        self._last_target = target
        return target

    monkeypatch.setattr('enemy.Enemy.shoot', rigged_shoot)

    enemy = Enemy()
    enemy.shoot()
    enemy.react_to_hit()

    assert len(enemy._to_shoot) == 2
    adherent = create_list_of_adherent(target)
    for field in adherent:
        if field == ('`', 1) or field == ('a', 0):
            continue
        assert field in enemy._to_shoot
    assert len(enemy._to_mark_as_empty) == 1
    tangents = create_list_of_tangents(target)
    for field in tangents:
        if field != ('b', 2):
            assert field not in enemy._to_mark_as_empty
        else:
            assert field in enemy._to_mark_as_empty
