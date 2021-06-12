import pandas as pd
import datetime

# https://github.com/nytimes/covid-19-data
# covid-19 data published by NYTimes on GitHub, which is updated daily
NYTIMES_DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

NYTIMES_ROLLING_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"

df = pd.read_csv(NYTIMES_ROLLING_DATA)


NEWJERSEY = df[df.state == "Pennsylvania"][["date", "state", "cases"]]
NEWJERSEY = NEWJERSEY.reset_index()
print(NEWJERSEY)



from matplotlib import pyplot as plt

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(5)

def animate(i):
    if (i % 10 == 0):
        plt.plot(NEWJERSEY[:i].index, NEWJERSEY["cases"][:i], label="test")

import matplotlib.animation as ani
from matplotlib.animation import PillowWriter
animator = ani.FuncAnimation(fig, animate, interval = 30, save_count = 300)
animator.save("asd.gif", writer=PillowWriter(fps=30))

plt.show()




