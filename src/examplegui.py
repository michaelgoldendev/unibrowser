import tkinter as tk
root = tk.Tk()

root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)

w = tk.Label(root,  
             text="Is your character real?",
             fg = "black",
             bg = "white",
             font = "Helvetica 24")
w.pack()



root.mainloop()