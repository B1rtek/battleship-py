import seaborn as seaborn
import matplotlib.pyplot as plt

from datetime import datetime

from fleet import Fleet

heatmaps = []
for x in range(10):
    heatmaps.append({})
filenames = [
    "heatmap4", "heatmap3_1", "heatmap3_2", "heatmap2_1", "heatmap2_2",
    "heatmap2_3", "heatmap1_1", "heatmap1_2", "heatmap1_3", "heatmap1_4"
]

for x in "abcdefghij":
    for y in range(1, 11):
        for heatmap in heatmaps:
            heatmap[(x, y)] = 0
fleet = Fleet()
for i in range(1000000):
    fleet.create_random()
    ships = fleet.ships()
    for ship, heatmap in zip(ships, heatmaps):
        segments = ship.segments()
        for segment in segments:
            x, y = segment.position()
            heatmap[(x, y)] += 1
    if i % 1000 == 0:
        now = datetime.now()
        strtime = now.strftime("%H:%M:%S")
        print(f"[{strtime}] Analyzed {i} boards...")
for heatmap, filename in zip(heatmaps, filenames):
    two_d_dataset = []
    for x in "abcdefghij":
        row = []
        for y in range(1, 11):
            row.append(heatmap[(x, y)]/10000)
        two_d_dataset.append(row)
    seaborn.heatmap(two_d_dataset, annot=True, fmt=".1f")
    plt.title(f"{filename} distribution on the map (values/10^4)")
    plt.savefig(f"{filename}.png")
    plt.clf()
