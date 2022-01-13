from datetime import datetime

import seaborn
import matplotlib.pyplot as plt

from enemy import Enemy
from fleet_creator import FleetCreator
from game import Game

test_runs = 10000
rounds = []
wins_old = 0
wins_new = 0

fleet_creator = FleetCreator()
game = Game()
for i in range(test_runs):
    fleet_creator.random_fleet()
    board, fleet = fleet_creator.get_setup()
    player = Enemy(hard_mode=True)
    game.start_game(board, fleet)
    round_count = 0
    while not game.won():
        if game.players_turn():
            x, y = player.shoot()
            game.discover_field(x, y)
            messages = game.get_display_messages()
            if messages.find("You've hit an enemy ship!") != -1:
                player.react_to_hit()
            if messages.find("You've destroyed an enemy ship!") != -1:
                player.react_to_sink()
            to_mark_as_empty = player.mark_as_empty()
            if to_mark_as_empty:
                for m_x, m_y in to_mark_as_empty:
                    game.mark_field(m_x, m_y)
        else:
            round_count += 1
            while not game.players_turn():
                game.enemy_move()
                if game.won():
                    break
    if game.check_win():
        wins_new += 1
    else:
        wins_old += 1
    rounds.append(round_count)
    if i % 10 == 0:
        now = datetime.now()
        strtime = now.strftime("%H:%M:%S")
        print(f"[{strtime}] {i}/{test_runs}")
seaborn.histplot(data=rounds, binwidth=1)
plt.savefig("new_vs_old_ai_rounds.png")
plt.pie([wins_old, wins_new], labels=["old_wins", "new_wins"])
plt.savefig("new_vs_old_ai_wins.png")
