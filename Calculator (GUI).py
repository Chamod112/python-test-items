from tkinter import *

root = Tk()
root.title("Calculator")

entry = Entry(root, width=25, borderwidth=5)
entry.grid(row=0, column=0, columnspan=4)

def click(num):
    entry.insert(END, num)

def clear():
    entry.delete(0, END)

def calculate():
    try:
        result = eval(entry.get())
        clear()
        entry.insert(0, result)
    except:
        clear()
        entry.insert(0, "Error")

buttons = [
    ('7',1,0),('8',1,1),('9',1,2),
    ('4',2,0),('5',2,1),('6',2,2),
    ('1',3,0),('2',3,1),('3',3,2),
    ('0',4,1)
]

for (text,row,col) in buttons:
    Button(root, text=text, width=5, command=lambda t=text: click(t)).grid(row=row, column=col)

Button(root, text="C", width=5, command=clear).grid(row=4, column=0)
Button(root, text="=", width=5, command=calculate).grid(row=4, column=2)

root.mainloop()
