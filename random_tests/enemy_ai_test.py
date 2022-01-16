import csv
from copy import deepcopy
from datetime import datetime

from board import return_all_field_coordinates
from fleet_creator import FleetCreator
from game import Game
from settings import Setting

tests_amount = 10000

old_ai_rounds = []
new_ai_rounds = []
old_ai_moves = []
new_ai_moves = []
old_ai_results = []
new_ai_results = []

creator = FleetCreator()
creator.start()
fields_queue = return_all_field_coordinates()
for i in range(tests_amount):
    game1 = Game()
    game1.apply_settings(
        {Setting.HARD_ENEMY: False, Setting.MARK_MISSES_AROUND: False}
    )
    game2 = Game()
    game2.apply_settings(
        {Setting.HARD_ENEMY: True, Setting.MARK_MISSES_AROUND: False})
    creator.random_fleet()
    board, fleet = creator.get_setup()
    board2, fleet2 = deepcopy(board), deepcopy(fleet)
    game1.start_game(board, fleet)
    field_index = 0
    moves_game1 = 0
    rounds_game1 = 0
    while not game1.won():
        if game1.players_turn():
            x, y = fields_queue[field_index]
            if not game1.discover_field(x, y):
                rounds_game1 += 1
            field_index += 1
        else:
            game1.enemy_move()
            moves_game1 += 1
    game2.start_game(board2, fleet2)
    field_index = 0
    moves_game2 = 0
    rounds_game2 = 0
    while not game2.won():
        if game2.players_turn():
            x, y = fields_queue[field_index]
            if not game2.discover_field(x, y):
                rounds_game2 += 1
            field_index += 1
        else:
            game2.enemy_move()
            moves_game2 += 1
    old_ai_rounds.append(rounds_game1)
    new_ai_rounds.append(rounds_game2)
    old_ai_moves.append(moves_game1)
    new_ai_moves.append(moves_game2)
    old_ai_results.append(1 if not game1.check_win() else 0)
    new_ai_results.append(1 if not game2.check_win() else 0)
    if i % 100 == 0:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print(f"[{time}] Processed {i} boards...")
with open("enemy_ai_test_results.csv", 'w', newline='') as file_handle:
    headers = [
        "old_ai_rounds", "old_ai_moves", "old_ai_results",
        "new_ai_rounds", "new_ai_moves", "new_ai_results",
        "tests_amount:", f"{tests_amount}"
    ]
    writer = csv.DictWriter(file_handle, headers)
    writer.writeheader()
    for oar, oam, oare, nar, nam, nare in zip(old_ai_rounds, old_ai_moves,
                                              old_ai_results, new_ai_rounds,
                                              new_ai_moves, new_ai_results):
        writer.writerow({
            "old_ai_rounds": oar,
            "old_ai_moves": oam,
            "old_ai_results": oare,
            "new_ai_rounds": nar,
            "new_ai_moves": nam,
            "new_ai_results": nare
        })
