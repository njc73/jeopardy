import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sys
import time
import os

def search():
    category = dropdown.get().strip().lower()
    if not category: # 
        messagebox.showwarning("invalid category :/")
        return
    
    results = j[j["category"].str.lower() == category]
    
    res.delete(1.0, tk.END)
    
    if results.empty:
        res.insert(tk.END, "no results found :(")
    else:
        for _, row in results.iterrows():
            q = row.get("question", "no questions found")
            a = row.get("answer", "no answers found")
            res.insert(tk.END, f"Q: {q}\nA: {a}\n\n")

j = pd.read_csv("data.tsv", sep = "\t")

cats = sorted(j["category"].dropna().unique())

app = tk.Tk()
app.title("jeopardy database")

dropdown = ttk.Combobox(app, values = cats, width = 50)
dropdown.grid(row = 0, column = 1, padx = 10, pady = 10)
dropdown.set("select a category")

tk.Label(app, text = "enter category: ").grid(row = 0, column = 0, padx = 10, pady = 10)
entry = tk.Entry(app, width = 50)
entry.grid(row = 0, column = 2, padx = 10, pady = 10)

butt = tk.Button(app, text = "find questions", command = search)
butt.grid(row = 0, column = 3, padx = 10, pady = 10)

res = tk.Text(app, wrap = tk.WORD, width = 100, height = 25)
res.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 10)

app.mainloop()