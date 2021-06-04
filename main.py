from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import datetime

def getStateCases(df, state):
    casesDF = df[df["state"] == state][["date", "cases"]]
    return casesDF.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0

def lineChartAnimation(dataframe):
    dataCount = len(dataframe.index) + 50
    color = ['red']
    fig = plt.figure()
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('Cases')
    plt.xlabel('Dates')

    def animate(i):
        # plots the dataset from beginning to i
        p = plt.plot(dataframe["date"][:i], dataframe["cases"][:i])
        p[0].set_color(color[0]) #set the colour of each curve
            
        if (i == len(dataframe.index)): # stop animation once all points plotted
            animator.event_source.stop()

        if (int(str((i / dataCount))[2:]) % 8 == 0): # use only decimal places
            print('{:.1%}'.format(i/dataCount))

    
    # save_count has +50 frames to give ending time, if no end time then use +1 (.index)   
    animator = FuncAnimation(fig, animate, repeat=False, interval=20, save_count=50) # dataCount
    animator.save("newnew.gif", writer=PillowWriter(fps=30))

    # plt.get_backend() default TkAgg
    # plt.switch_backend("agg") to prevent function calling twice (animation repeats)
    
    # plt.show()

    
# https://github.com/nytimes/covid-19-data
# covid-19 data published by NYTimes on GitHub, which is updated daily
NYTIMES_DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

df = pd.read_csv(NYTIMES_DATA_URL)

# manipulate the data
df["date"] = pd.to_datetime(df["date"])

#print(df["date"][99] < datetime.datetime(2020, 9, 30))
#print(df["date"][99] < datetime.datetime(2020, 1, 30))



washingtonState = getStateCases(df, "Washington")



# kinda lags while generating graph, maybe instead of graphing every point just graph some?
# plt.subplots(figsize=(8,6))
# https://holypython.com/how-to-save-matplotlib-animations-the-ultimate-guide/


import tkinter as tk

