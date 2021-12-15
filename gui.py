from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from backend import *

def generateGraphBtn():
    state1Input = state1Combobox.get()
    state2Input = state2Combobox.get()
    metricInput = metricCombobox.get()
    chartInput = chartCombobox.get()
    animationInput = animationCombobox.get()

    errorMessage = "Be sure to select from the available options -- the following options are missing/incorrect:\n\n"
    originalErrorLen = len(errorMessage)
    if (not state1Input) or (state1Input not in STATES): errorMessage += "State 1\n"
    if (not state2Input) or (state2Input not in STATES): errorMessage += "State 2\n"
    if (not metricInput) or (metricInput not in METRIC_TYPES): errorMessage += "Metric Type\n"
    if (not chartInput) or (chartInput not in CHART_TYPES): errorMessage += "Chart Type\n"
    if (not animationInput) or (animationInput not in ANIMATED_OPTIONS): errorMessage += "Animation Option"

    if (len(errorMessage) > originalErrorLen): # there's an error since message added on
        showerror("Input Fields Incorrect", errorMessage)
    else: # no error
        state1df = metricOptions[METRIC_TYPES.index(metricInput)](state1Input)
        state2df = metricOptions[METRIC_TYPES.index(metricInput)](state2Input)
        inputOptions[CHART_TYPES.index(chartInput)](state1df, state2df, [state1Input, state2Input], metricInput, animatedInput(animationInput))
        showinfo("Graphic Generated", "Your graphic has been sucessfully generated!")

def animatedInput(selection):
    if ANIMATED_OPTIONS.index(selection) == 1:
        return True
    return False

STATES = [""] + sorted(cumulative_df["state"].drop_duplicates().tolist())
METRIC_TYPES = ["", "Total Cumulative Cases", "Daily New Cases (Rolling Avg.)", "Total Cumulative Deaths", "Daily New Deaths (Rolling Avg.)"] 
CHART_TYPES = ["", "Line Chart", "Pie Chart", "Bar Chart"]
ANIMATED_OPTIONS = ["", "Animated (Saved as .gif)", "No Animation (Image as .png)"] 


### Tkinter 
window = Tk()
window.geometry("820x500")
window.configure(bg = "#FFFFFF")
window.title("COVID-19 Comparison Graph Generator")
icon = PhotoImage(file = "assets/virus_icon.png")
window.iconphoto(True, icon)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 500,
    width = 820,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"assets/background.png")
background = canvas.create_image(
    410.0, 250.0,
    image=background_img)

canvas.create_text( # center, bold doesn't work, try different method
    410.0, 45.0,
    text = "COVID-19 Comparison Graph Generator",
    fill = "#30882d",
    font = ("Georgia", 24, "underline"),
    justify = "center")

canvas.create_text( 
    409.0, 103.0,
    text = "Enter two states and choose from the following options \nto generate a graph. The graph will be automatically \ndownloaded into the \"graphs\" folder.",
    fill = "#000000",
    font = ("Georgia", 14),
    justify = "center")

canvas.create_text(
    409.5, 189.0,
    text = "v.s",
    fill = "#30882d",
    font = ("Georgia", 20))

# State 1 Input
state1Combobox = ttk.Combobox(window, value=STATES)
state1Combobox.current(0)
state1Combobox.place(
    x = 190.0, y = 168,
    width = 151.0,
    height = 36)

canvas.create_text(
    265.5, 154.5,
    text = "State 1 ",
    fill = "#000000",
    font = ("Georgia", 14))

# State 2 Input
state2Combobox = ttk.Combobox(window, value=STATES)
state2Combobox.current(0)
state2Combobox.place(
    x = 479.0, y = 168,
    width = 151.0,
    height = 36)

canvas.create_text(
    554.5, 154.5,
    text = "State 2 ",
    fill = "#000000",
    font = ("Georgia", 14))

# Metric Type Input
metricCombobox = ttk.Combobox(window, value=METRIC_TYPES)
metricCombobox.current(0)
metricCombobox.place(
    x = 302.0, y = 242,
    width = 214.0,
    height = 33)

canvas.create_text(
    352, 227.5,
    text = "Metric Type",
    fill = "#000000",
    font = ("Georgia", 14))

# Chart Type Input
chartCombobox = ttk.Combobox(window, value=CHART_TYPES)
chartCombobox.current(0)
chartCombobox.place(
    x = 302.0, y = 305,
    width = 214.0,
    height = 33)

canvas.create_text(
    347.5, 291.5,
    text = "Chart Type",
    fill = "#000000",
    font = ("Georgia", 14))

# Animation Input
animationCombobox = ttk.Combobox(window, value=ANIMATED_OPTIONS)
animationCombobox.current(0)
animationCombobox.place(
    x = 302.0, y = 371,
    width = 214.0,
    height = 33)

canvas.create_text(
    347.5, 357.5,
    text = "Animation",
    fill = "#000000",
    font = ("Georgia", 14))

# Generate Graph Btn
btnImg = PhotoImage(file = f"assets/button.png")
btn = Button(
    image = btnImg,
    borderwidth = 0,
    highlightthickness = 0,
    command = generateGraphBtn,
    relief = "flat")

btn.place(
    x = 316, y = 427,
    width = 188,
    height = 48)

window.resizable(False, False)
window.mainloop()
