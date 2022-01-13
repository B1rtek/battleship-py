import seaborn as seaborn
import matplotlib.pyplot as plt

from datetime import datetime

from fleet import Fleet

hitmap4 = {}
hitmap3_1 = {}
hitmap3_2 = {}
hitmap2_1 = {}
hitmap2_2 = {}
hitmap2_3 = {}
hitmap1_1 = {}
hitmap1_2 = {}
hitmap1_3 = {}
hitmap1_4 = {}

for x in "abcdefghij":
    for y in range(1, 11):
        hitmap4[(x, y)] = 0
        hitmap3_1[(x, y)] = 0
        hitmap3_2[(x, y)] = 0
        hitmap2_1[(x, y)] = 0
        hitmap2_2[(x, y)] = 0
        hitmap2_3[(x, y)] = 0
        hitmap1_1[(x, y)] = 0
        hitmap1_2[(x, y)] = 0
        hitmap1_3[(x, y)] = 0
        hitmap1_4[(x, y)] = 0
fleet = Fleet()
for i in range(500000):
    fleet.create_random()
    ships = fleet.ships()
    segments = ships[0].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap4[(x, y)] += 1
    segments = ships[1].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap3_1[(x, y)] += 1
    segments = ships[2].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap3_2[(x, y)] += 1
    segments = ships[3].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap2_1[(x, y)] += 1
    segments = ships[4].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap2_2[(x, y)] += 1
    segments = ships[5].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap2_3[(x, y)] += 1
    segments = ships[6].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap1_1[(x, y)] += 1
    segments = ships[7].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap1_2[(x, y)] += 1
    segments = ships[8].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap1_3[(x, y)] += 1
    segments = ships[9].segments()
    for segment in segments:
        x, y = segment.position()
        hitmap1_4[(x, y)] += 1
    if i % 1000 == 0:
        now = datetime.now()
        strtime = now.strftime("%H:%M:%S")
        print(f"[{strtime}] Analyzed {i} boards...")
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap4[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap4.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap3_1[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap3_1.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap3_2[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap3_2.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap2_1[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap2_1.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap2_2[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap2_2.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap2_3[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap2_3.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap1_1[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap1_1.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap1_2[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap1_2.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap1_3[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap1_3.png")
plt.clf()
two_d_dataset = []
for x in "abcdefghij":
    row = []
    for y in range(1, 11):
        row.append(hitmap1_4[(x, y)])
    two_d_dataset.append(row)
seaborn.heatmap(two_d_dataset)
plt.savefig("heatmap1_4.png")
plt.clf()