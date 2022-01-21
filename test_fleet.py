from fleet import ShipSegment, Ship


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