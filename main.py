from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import datetime


# get the data: https://github.com/nytimes/covid-19-data
# COVID-19 data published by the NYTimes, updated daily
CUMULATIVE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
ROLLING_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"


# matplotlib styles
titleFont = {"family":"Georgia",
             "color":"black",
             "fontweight":"bold"}

def createDF(dataType):
    # argument ex: 'cumulative' 'rolling' hence .upper()
    # create df variable name 'cumulative_df' or 'rolling_df'
    if (dataType + "_df") in globals():
        print(f"{dataType} df already exists.")
    else:
        globals()[f"{dataType}_df"] = pd.read_csv(
                                        globals()[f"{dataType.upper()}_DATA"])
        # make all dates into datetime (for graphing)
        df_variable = globals()[f"{dataType}_df"] 
        df_variable["date"] = pd.to_datetime(df_variable["date"])      
        print(f"{dataType} df created.")

def getCumulativeCases(state):
    createDF("cumulative")
    cases_df = cumulative_df[cumulative_df["state"] == state][["date", "cases"]]
    return cases_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0

def getCumulativeDeaths(state):
    createDF("cumulative")
    deaths_df = cumulative_df[cumulative_df["state"] == state][["date", "deaths"]]
    return deaths_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0

def getDailyCases(state):
    createDF("rolling")
    cases_df = rolling_df[(rolling_df["state"] == state) & (rolling_df["cases"] >= 0) & (rolling_df["cases_avg"] >= 0)]\
                                    [["date", "cases", "cases_avg"]]
    return cases_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0

def getDailyDeaths(state):
    createDF("rolling")
    deaths_df = rolling_df[(rolling_df["state"] == state) & (rolling_df["deaths"] >= 0) & (rolling_df["deaths_avg"] >= 0)]\
                                    [["date", "deaths", "deaths_avg"]]
    return deaths_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0
                                                     
def lineChartAnimation(dataframe1, dataframe2, states, metric):
    # make dates aligned
    if (dataframe1["date"][0] < dataframe2["date"][0]):
        dataframe1 = dataframe1[dataframe1["date"] >= dataframe2["date"][0]]
    elif (dataframe1["date"][0] > dataframe2["date"][0]):
        dataframe2["date"] = dataframe2[dataframe2["date"] >= dataframe1["date"][0]]

        
    fig = plt.figure()
    fig.set_figwidth(9)
    fig.set_figheight(5)
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.subplots_adjust(bottom = 0.2, top = 0.9)
    plt.ylabel(metric)
    plt.xlabel('Dates')
    plt.title(metric + " Over Time", fontdict=titleFont)
    
    dataType = dataframe1.columns[1]
    dataCount = len(dataframe1.index) + 50
    
    def animate(i):
        # plots the dataset from beginning to i
        if (i % 1 == 0):
            plt.plot(dataframe1["date"][:i], dataframe1[dataType][:i], '#1f77b4')
            plt.plot(dataframe2["date"][:i], dataframe2[dataType][:i], '#17becf')
            plt.legend(states, loc="upper left")
            
        if (i == len(dataframe1.index)): # stop animation once all points plotted
            animator.event_source.stop()

        # make better progress
        #if (int(str((i / dataCount))[2:]) % 8 == 0): # use only decimal places
        #    print('{:.1%}'.format(i/dataCount))

    
    # save_count has +50 frames to give ending time, if no end time then use +1 (.index)   
    animator = FuncAnimation(fig, animate, repeat=False, interval=20, save_count=dataCount + 50)
    #animator.save("newnew.gif", writer=PillowWriter(fps=30))

    # plt.get_backend() default TkAgg
    # plt.switch_backend("agg") to prevent function calling twice (animation repeats)
    
    plt.show()

def lineChart(dataframe1, dataframe2, states, metric):
    # make dates aligned
    if (dataframe1["date"][0] < dataframe2["date"][0]):
        dataframe1 = dataframe1[dataframe1["date"] >= dataframe2["date"][0]]
    elif (dataframe1["date"][0] > dataframe2["date"][0]):
        dataframe2["date"] = dataframe2[dataframe2["date"] >= dataframe1["date"][0]]

    fig = plt.figure()
    fig.set_figwidth(9)
    fig.set_figheight(5)
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.subplots_adjust(bottom = 0.2, top = 0.9)
    plt.ylabel(metric)
    plt.xlabel('Dates')
    plt.title(metric + " Over Time", fontdict=titleFont)

    dataType = dataframe1.columns[1]
    
    
    plt.plot(dataframe1["date"], dataframe1[dataType], '#1f77b4')
    plt.plot(dataframe2["date"], dataframe2[dataType], '#17becf')
    plt.legend(states, loc="upper left")
    
    plt.savefig("test.png")
    plt.show()



    



washingtonState = getCumulativeDeaths("Washington")


# sd = test[["date", "cases_avg"]]
# kinda lags while generating graph, maybe instead of graphing every point just graph some?
# plt.subplots(figsize=(8,6))
# https://holypython.com/how-to-save-matplotlib-animations-the-ultimate-guide/
# scientific notation
# let users choose color


