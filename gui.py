import tkinter as tk
from PIL import ImageTk, Image



def test_command():
    print("yes")
    
window = tk.Tk()


canvas = tk.Canvas(window, width=600, height= 300)
canvas.grid(columnspan=3, rowspan=3)

# image
virus_sprite = ImageTk.PhotoImage(Image.open("covid.png"))
virus_label = tk.Label(image=virus_sprite)
virus_label.image = virus_sprite
virus_label.grid(column=1, row=0)

# text
testtext = tk.Label(window, text="Choose a state to view the COVID-19 metrics:", font="Georgia")
testtext.grid(columnspan=3, column=0, row=1)

# button
buttontext = tk.StringVar()
buttontext.set("Button Example")
testbutton = tk.Button(window, textvariable=buttontext, command=test_command, font="Georgia", bg="#20bebe", fg="white", height=2, width=15)
testbutton.grid(column=1, row=2)




canvas = tk.Canvas(window, width=600, height= 200)
canvas.grid(columnspan=3)





window.mainloop()
