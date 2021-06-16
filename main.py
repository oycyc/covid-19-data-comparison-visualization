from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import datetime
import os


# get the data: https://github.com/nytimes/covid-19-data
# COVID-19 data published by the NYTimes, updated daily
CUMULATIVE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
ROLLING_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"


# matplotlib styles
titleFont = {"family":"Georgia",
             "color":"black",
             "fontweight":"bold"}

colors = ["#003f5c", "#ffa600"]

def createOuterFolder():
    if not os.path.isdir("graphs"):
        os.makedirs("graphs")

def createFolder(chartType):
    createOuterFolder()
    folderName = "graphs/" + chartType
    
    if not os.path.isdir(folderName):
        os.makedirs(folderName)
        
    return folderName
    
                
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
    cases_df = rolling_df[(rolling_df["state"] == state) & (rolling_df["cases_avg"] >= 0)]\
                                    [["date", "cases_avg"]]
    return cases_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0

def getDailyDeaths(state):
    createDF("rolling")
    deaths_df = rolling_df[(rolling_df["state"] == state) & (rolling_df["deaths_avg"] >= 0)]\
                                    [["date", "deaths_avg"]]
    return deaths_df.reset_index().drop("index", axis=1) # remove old indexing, use new starting from 0


def lineChart(dataframe1, dataframe2, states, metric, animated):
    # make dates start same 
    if (dataframe1["date"][0] < dataframe2["date"][0]):
        dataframe1 = dataframe1[dataframe1["date"] >= dataframe2["date"][0]]
    elif (dataframe1["date"][0] > dataframe2["date"][0]):
        dataframe2 = dataframe2[dataframe2["date"] >= dataframe1["date"][0]]

    fig = plt.figure()
    fig.set_figwidth(9)
    fig.set_figheight(5)
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.subplots_adjust(bottom = 0.2, top = 0.9)
    plt.ylabel(metric)
    plt.xlabel('Dates')
    plt.title(metric + " Over Time", fontdict=titleFont)

    dataType = dataframe1.columns[1]

    if animated:
        dataPoints = len(dataframe1.index)
        # set legend up
        # plt.plot(dataframe1["date"][0], [0], colors[0])
        # plt.plot(dataframe2["date"][0], [0], colors[1])
        # plt.legend(states, loc="upper left")
        
        def animate(i):
            if (i % 3 == 0): # every other point to generate plot faster
                # plots the dataset from beginning to i
                plt.plot(dataframe1["date"][:i], dataframe1[dataType][:i], colors[0])
                plt.plot(dataframe2["date"][:i], dataframe2[dataType][:i], colors[1])
                plt.legend(states, loc="upper left")
                print(i)
                
        # save_count has +75 frames to give ending time, if no end time then use +1 (.index)   
        animator = FuncAnimation(fig, animate, repeat=False, interval=5, save_count=dataPoints + 75)
        animator.save(f"{createFolder('line_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric.replace(' ', '')}.gif", writer=PillowWriter(fps=30))

    
        # plt.show()
        return
    
    
    plt.plot(dataframe1["date"], dataframe1[dataType], colors[0])
    plt.plot(dataframe2["date"], dataframe2[dataType], colors[1])
    plt.legend(states, loc="upper left")
    plt.savefig(f"{createFolder('line_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric}.png")


def pieChart(dataframe1, dataframe2, states, metric, animated):
    # make dates start same 
    if (dataframe1["date"][0] < dataframe2["date"][0]):
        dataframe1 = dataframe1[dataframe1["date"] >= dataframe2["date"][0]]
        dataframe1 = dataframe1.reset_index().drop("index", axis=1)
    elif (dataframe1["date"][0] > dataframe2["date"][0]):
        dataframe2 = dataframe2[dataframe2["date"] >= dataframe1["date"][0]]
        dataframe2 = dataframe2.reset_index().drop("index", axis=1)

    labels = states[0], states[1]
    explode = (0.01, 0.01) 
    fig, ax = plt.subplots()
    
    if animated:
        def animate(i):
            if (i % 3 == 0): # every other point to generate plot faster
                try:
                    total = int(dataframe1.iloc[:,1][i]) + int(dataframe2.iloc[:,1][i])
                    def numbering(percent):
                        val = int(round(percent*total/100.0))
                        return val
                    ax.clear()
                    sizes = [int(dataframe1.iloc[:,1][i]), int(dataframe2.iloc[:,1][i])]
                    ax.pie(sizes, explode=explode, labels=labels, autopct=numbering, shadow=True, startangle=90)
                    ax.axis('equal')
                    ax.set_title(metric + f"\n{dataframe1.iloc[i]['date'].strftime('%B, %Y')}", fontdict=titleFont)
                except (ValueError, KeyError) as e: # animation continues for 75 more frames to give extra time, so stop it
                    animator.event_source.stop()
                
            
        animator = FuncAnimation(fig, animate, interval=1, save_count=len(dataframe1) + 75)
        animator.save(f"{createFolder('pie_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric.replace(' ', '')}.gif", writer=PillowWriter(fps=30))
        return # animation done, stop rest of function

    # plot still graph, not animated
    # later clean this part use variable instead of calling the df multiple times
    total = int(dataframe1.iloc[:,1][-1:]) + int(dataframe2.iloc[:,1][-1:])
    def numbering(percent):
        val = int(round(percent*total/100.0))
        return val
    # selects last index
    sizes = [int(dataframe1.iloc[:,1][-1:]), int(dataframe2.iloc[:,1][-1:])]
    ax.pie(sizes, explode=explode, labels=labels, autopct=numbering,
            shadow=True, startangle=90)
    ax.axis('equal')  
    ax.set_title(metric + f"\nAs of {dataframe1.iloc[-1]['date'].strftime('%B %d, %Y')}", fontdict=titleFont)
    plt.savefig(f"{createFolder('pie_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric}.png")


def barChart(dataframe1, dataframe2, states, metric, animated):
    # make dates start same 
    if (dataframe1["date"][0] < dataframe2["date"][0]):
        dataframe1 = dataframe1[dataframe1["date"] >= dataframe2["date"][0]]
        dataframe1 = dataframe1.reset_index().drop("index", axis=1)
    elif (dataframe1["date"][0] > dataframe2["date"][0]):
        dataframe2 = dataframe2[dataframe2["date"] >= dataframe1["date"][0]]
        dataframe2 = dataframe2.reset_index().drop("index", axis=1)

    states = [states[0], states[1]]
    # convert list into index for position
    position = range(len(states))
    
    fig = plt.figure()
    fig.set_figwidth(8)
    fig.set_figheight(5)
    plt.xlabel("U.S. States")
    plt.ylabel(metric)
    plt.xticks(position, states)


    if animated:
        def animate(i):
            if (i % 3 == 0): # every other point to generate plot faster
                try:
                    data = [int(dataframe1.iloc[:,1][i]), int(dataframe2.iloc[:,1][i])]
                    fig.clear()
                    plt.bar(position, data, color=colors)
                    plt.title(metric + f"\n{dataframe1.iloc[i]['date'].strftime('%B, %Y')}", fontdict=titleFont)
                    plt.xlabel("U.S. States")
                    plt.ylabel(metric)
                    plt.xticks(position, states)
                except (ValueError, KeyError) as e: # animation continues for 75 more frames to give extra time, so stop it
                    animator.event_source.stop()
                    
        animator = FuncAnimation(fig, animate, interval=1, save_count=len(dataframe1) + 75) # save_count=len(dataframe1) + 75
        animator.save(f"{createFolder('bar_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric.replace(' ', '')}.gif", writer=PillowWriter(fps=30))
        return # animation done, stop rest of function
    
    data = [int(dataframe1.iloc[:,1][-1:]), int(dataframe2.iloc[:,1][-1:])]
    plt.bar(position, data, color=colors)
    plt.title(metric + f"\nAs of {dataframe1.iloc[-1]['date'].strftime('%B %d, %Y')}", fontdict=titleFont)
    plt.savefig(f"{createFolder('bar_chart')}/{states[0].replace(' ', '')}Vs{states[1].replace(' ', '')}_{metric}.png")



# corresponds to the index of METRIC_TYPES from (GUI FILE HERE)
metricOptions = {1 : getCumulativeCases,
                 2 : getDailyCases,
                 3 : getCumulativeDeaths,
                 4 : getDailyDeaths}
    
# corresponds to the index of CHART_TYPES from (GUI FILE HERE)
inputOptions = {1 : lineChart,
                2 : pieChart,
                3 : barChart}



    



washingtonState = getCumulativeDeaths("Washington")


# kinda lags while generating graph, maybe instead of graphing every point just graph some?
# https://holypython.com/how-to-save-matplotlib-animations-the-ultimate-guide/
# scientific notation
# ## https://learnui.design/tools/data-color-picker.html
# random color (randomintnorep?) and let users choose
# organize code in classes








