import tkinter as tk

from ScrollableFrame import ScrollableFrame

root = tk.Tk()

frame = ScrollableFrame(root)
frame2 = ScrollableFrame(root)

for i in range(25):
    tk.Label(frame.scrollable_frame, text="Test1").grid(row=i, column=1)

for i in range(25):
    tk.Label(frame2.scrollable_frame, text="Test2").grid(row=i, column=1)

frame.grid(row=0, column=0)
frame2.grid(row=0, column=1)
root.mainloop()