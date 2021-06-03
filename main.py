import pandas as pd
import datetime

# https://github.com/nytimes/covid-19-data
# covid-19 data published by NYTimes on GitHub, which is updated daily
NYTIMES_DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

df = pd.read_csv(NYTIMES_DATA_URL)

NEW = df.drop(["fips", "deaths", "deaths"], axis=1)
NEW = NEW.drop("state", axis=1)
NEW = NEW.rename(columns = {"cases": "Pennsylvania"})
NEW["Extra"] = NEW["Pennsylvania"] * 10
NEW["Extra"] = NEW["Extra"].apply(lambda x: int(x))

NEW["Extra1"] = NEW["Pennsylvania"] * 2
NEW["Extra1"] = NEW["Extra1"].apply(lambda x: int(x))

NEW["Extra2"] = NEW["Pennsylvania"] * 5
NEW["Extra2"] = NEW["Extra2"].apply(lambda x: int(x))

NEW.index = NEW["date"]
NEW = NEW.drop("date", axis=1)

def text(x):
    year, month, day = map(int, x.split("-"))
    return datetime.datetime(year, month, day)


year, month, day = map(int, df.date[0].split("-"))
df["datetime"] = df["date"].apply(text)

print(df["datetime"][99] < datetime.datetime(year, month, 30))



washingtonState = df[df.state == "Washington"][["date", "state", "cases"]]
washingtonState = washingtonState.reset_index()
washingtonState = washingtonState.iloc[50:200]

print(washingtonState)

print("beginning")
print(df[(df["state"] == "Washington") & (df["datetime"] < datetime.datetime(year, month, 30))])

#print(df[df["state"] == "Washington"].iloc[0:900].to_string())


from matplotlib import pyplot as plt

fig = plt.figure()

def animate(i):
    plt.plot(washingtonState[:i].index, washingtonState["cases"][:i])
    #plt.plot(washingtonState["date"][:i], washingtonState["cases"][:i])

import matplotlib.animation as ani
from matplotlib.animation import PillowWriter

animator = ani.FuncAnimation(fig, animate, interval = 1, save_count=200)

animator.save("newnew.gif", writer=PillowWriter(fps=60))
#animator.save("new.mp4", writer=ani.FFMpegWriter(fps=60))
plt.show()


def asd(): 
    color = ['red', 'green', 'blue', 'orange']
    fig = plt.figure()
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('No of Deaths')
    plt.xlabel('Dates')
    plt.legend(NEW.columns)
    
    def buildmebarchart(i):
        print(i)
        plt.plot(NEW[:i].index, NEW[:i].values) #note it only returns the dataset, up to the point i
        
            
    import matplotlib.animation as ani
    animator = ani.FuncAnimation(fig, buildmebarchart, interval = 1000)
    plt.show()


