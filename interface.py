import tkinter as tk
first = tk.Tk()

tk.Label(first, text="Chip Translator").grid(row=0)
tk.Label(first, text="Chip start:").grid(row=1)
tk.Label(first, text="Chip end:").grid(row=2)
ChipStart = tk.Entry(first)
name = ChipStart.get()
ChipEnd = tk.Entry(first)
ChipStart.grid(row=1, column=1)
ChipEnd.grid(row=2, column=1)
print(name)
first.mainloop()
