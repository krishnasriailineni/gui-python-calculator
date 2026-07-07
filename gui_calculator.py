import tkinter as tk

# Create window
root = tk.Tk()
root.title("Pro Calculator")
root.geometry("340x520")
root.configure(bg="#1e1e1e")

# Entry (display)
entry = tk.Entry(root, width=22, font=("Arial", 22), bd=8,
                 relief="ridge", justify="right")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15)

# History list
history = []

# Functions
def click(value):
    entry.insert(tk.END, str(value))

def clear():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current[:-1])

def calculate():
    try:
        expression = entry.get()
        result = eval(expression)

        history.append(f"{expression} = {result}")

        # Save to file
        with open("history.txt", "a") as f:
            f.write(f"{expression} = {result}\n")

        entry.delete(0, tk.END)
        entry.insert(0, result)

    except ZeroDivisionError:
        entry.delete(0, tk.END)
        entry.insert(0, "Cannot divide by 0")
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("300x300")
    history_window.configure(bg="#1e1e1e")

    text_area = tk.Text(history_window, bg="#1e1e1e",
                        fg="white", font=("Arial", 12))
    text_area.pack(fill="both", expand=True)

    # Load from file if exists
    try:
        with open("history.txt", "r") as f:
            text_area.insert(tk.END, f.read())
    except:
        text_area.insert(tk.END, "No history yet.")

# Keyboard support
def key_event(event):
    key = event.char

    if key in "0123456789+-*/.%":
        click(key)
    elif key == "\r":  # Enter key
        calculate()
    elif key == "\x08":  # Backspace
        backspace()

root.bind("<Key>", key_event)

# Button style
btn_style = {
    "font": ("Arial", 12, "bold"),
    "width": 5,
    "height": 2,
    "bd": 3
}

# Buttons layout
buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('%',4,1), ('//',4,2), ('+',4,3),
    ('**',5,0), ('C',5,1), ('⌫',5,2), ('=',5,3),
    ('H',6,0)
]

# Create buttons
for (text, row, col) in buttons:
    if text == "C":
        action = clear
        color = "#ff4d4d"
    elif text == "=":
        action = calculate
        color = "#4CAF50"
    elif text == "H":
        action = show_history
        color = "#2196F3"
    elif text == "⌫":
        action = backspace
        color = "#ff944d"
    elif text in ['+', '-', '*', '/', '%', '//', '**']:
        action = lambda x=text: click(x)
        color = "#ffd11a"
    else:
        action = lambda x=text: click(x)
        color = "#333333"

    tk.Button(root, text=text, bg="white", fg="black",
              command=action, **btn_style).grid(row=row, column=col, padx=5, pady=5)

# Run app
root.mainloop()
