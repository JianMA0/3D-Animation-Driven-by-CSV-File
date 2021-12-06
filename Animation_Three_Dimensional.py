
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pandas._config import display
from PIL import Image, ImageDraw

ACTION_NUMBER = 0;

# read file
csv_file = '/Users/breeze/Desktop/pose-output.csv'
df = pd.read_csv(csv_file, delimiter=',', header=0)
data = df.iloc[:, :37]

#data preparation
maximum = -1000
minimum = 1000
#data: maximum:  1.396005392074585   minimum:  -3.661261558532715
for i in range(data.shape[0]):
    row = data.iloc[i]
    for j in range(1, len(row)):
        temp = row[j].strip('[]')
        x = temp.split(',')
        xline = np.array(x, dtype=float)
        n = row[0]
        maximum = max(maximum, np.min(xline))
        minimum = min(minimum, np.min(xline))
        # print(row[0], " max: ", np.min(xline), " min: ", np.min(xline))
        data.iloc[i][j] = xline
# print("maximum: ", maximum, "  minimum: ", minimum)


# start for current action
row = data.iloc[ACTION_NUMBER];
# animation function.  This is called sequentially
def animate(i, lineRight, lineLeft, lineUpper, linelower):
    # order: wrist, elbow, shoulder, hip, knee, ankle
    rightx = [row[16][i], row[10][i], row[4][i], row[22][i], row[28][i], row[34][i]]
    righty = [row[17][i], row[11][i], row[5][i], row[23][i], row[29][i], row[35][i]]
    rightz = [row[18][i], row[12][i], row[6][i], row[24][i], row[30][i], row[36][i]]

    # order: wrist, elbow, shoulder, hip, knee, ankle
    leftx = [row[13][i], row[7][i], row[1][i], row[19][i], row[25][i], row[31][i]]
    lefty = [row[14][i], row[8][i], row[2][i], row[20][i], row[26][i], row[32][i]]
    leftz = [row[15][i], row[9][i], row[3][i], row[21][i], row[27][i], row[33][i]]

    # left shoulder to right shoelder
    upperConnectionx = [row[1][i], row[4][i]]
    upperConnectiony = [row[2][i], row[5][i]]
    upperConnectionz = [row[3][i], row[6][i]]

    # left hip to right hip
    lowerConnectionx = [row[19][i], row[22][i]]
    lowerConnectiony = [row[20][i], row[23][i]]
    lowerConnectionz = [row[21][i], row[24][i]]

    lineRight.set_data(rightx, righty)
    lineRight.set_3d_properties(rightz)

    lineLeft.set_data(leftx, lefty)
    lineLeft.set_3d_properties(leftz)

    lineUpper.set_data(upperConnectionx, upperConnectiony)
    lineUpper.set_3d_properties(upperConnectionz)

    linelower.set_data(lowerConnectionx, lowerConnectiony)
    linelower.set_3d_properties(lowerConnectionz)

    return lineRight, lineLeft, lineUpper, linelower,


fig = plt.figure()
ax = fig.add_subplot(projection="3d")

lineLeft, = ax.plot([], [], [], color='#519259', marker='o', linestyle='solid', linewidth=2, markersize=3)
lineRight, = ax.plot([], [], [], color='#519259', marker='o', linestyle='solid', linewidth=2, markersize=3)
lineUpper, = ax.plot([], [], [], color='#F0BB62', marker='o', linestyle='dashed', linewidth=2, markersize=3)
linelower, = ax.plot([], [], [], color='#F0BB62', marker='o', linestyle='dashed', linewidth=2, markersize=3)

# Setting the axes properties
ax.set(xlim3d=(-0.5, 1), xlabel='X')
ax.set(ylim3d=(-0.5, 1), ylabel='Y')
ax.set(zlim3d=(-0.5, 1), zlabel='Z')
ax.set_title(row[0])

ani = animation.FuncAnimation(fig, animate,
                                   frames=len(row[1]),
                                   fargs=(lineRight, lineLeft, lineUpper, linelower),
                                   interval=10, blit=False)

ani.save("movie.gif", writer=animation.PillowWriter(fps=24))
plt.show()
