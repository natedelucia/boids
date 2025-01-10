import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, bg="black", height=512, width=512, bd=0)
canvas.pack()
canvas.create_oval(240, 240, 260, 260, fill="red")
root.mainloop()
