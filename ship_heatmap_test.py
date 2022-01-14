import seaborn as seaborn
import matplotlib.pyplot as plt

from fleet import Fleet

hitmap = {}
for x in "abcdefghij":
    for y in range(1, 11):
        hitmap[(x, y)] = 0
fleet = Fleet()
for i in range(1000000):
    fleet.create_random()
    ships = fleet.ships()
    for ship in ships:
        segments = ship.segments()
        for segment in segments:
            x, y = segment.position()
            hitmap[(x, y)] = hitmap[(x, y)] + 1
    if i % 1000 == 0:
        print(f"Analyzed {i} boards...")
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        print(f"({x}, {y}) = {hitmap[(x, y)]}")
        row.append(hitmap[(x, y)])
    two_d_dataset.append(row)
heatmapa = seaborn.heatmap(two_d_dataset)
plt.show()
