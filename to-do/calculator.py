import tkinter as tk
import math

win = tk.Tk()
win.title("Calculator")
win.geometry("600x600")

win.grid_columnconfigure(0,weight=3)
win.grid_columnconfigure(1,weight=1)
win.grid_columnconfigure(2,weight=3)

win.grid_rowconfigure(0,weight=1)
win.grid_rowconfigure(1,weight=3)
win.grid_rowconfigure(2,weight=1)

# creating frame for bg of calculator
calFrame = tk.Frame(win, background='black', width=250, height=400, bd=3, relief=tk.RAISED)
calFrame.grid(row=1,column=1)
calFrame.grid_propagate(False)

# dividing frame for buttons
for i in range(4):
    calFrame.grid_columnconfigure(i,weight=1)

calFrame.grid_rowconfigure(0,weight=1)
calFrame.grid_rowconfigure(1,weight=1)

for j in range(2,8):
    calFrame.grid_rowconfigure(j,weight=1)

# calculator history
lastCal = tk.Label(calFrame,bg='black',bd=0,fg='lightgray',anchor='e',font=('Arial',16))
lastCal.grid(row=0,column=0,columnspan=4,sticky='nsew',padx=5)

# calculator screen
entryCurr = tk.Entry(calFrame,font=('Arial',28),justify='right',bg='black',fg='white',bd=0,insertbackground='white')
entryCurr.grid(row=1,column=0,columnspan=4,sticky='snew',padx=5,pady=5)

# button press
def click(clicked):
    entryCurr.insert(tk.END,clicked)

# backspace
def backspace():
    current = entryCurr.get()
    if current:
        entryCurr.delete(len(current)-1)

# clear entry
def clear_entry():
    text = entryCurr.get()
    parts = text.split()
    if parts:
        parts.pop()
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, " ".join(parts))
    

# equals to
def calculate():
    try:
        exp = entryCurr.get()
        result = eval(exp)
        lastCal.config(text=exp+'=')
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, str(result))
    except:
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, "Error")

# sqaure 
def square_func():
    try:
        num = float(entryCurr.get())
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, str(num**2))
    except:
        entryCurr.insert(0, "Error")

# square root
def root_func():
    try:
        num = float(entryCurr.get())
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, str(math.sqrt(num)))
    except:
        entryCurr.insert(0, "Error")

# revert
def reciprocal():
    try:
        num = float(entryCurr.get())
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, str(1/num))
    except:
        entryCurr.insert(0, "Error")

# +/-
def change_sign():
    try:
        num = float(entryCurr.get())
        entryCurr.delete(0, tk.END)
        entryCurr.insert(0, str(-num))
    except:
        pass

def clear():
    entryCurr.delete(0,tk.END)
    lastCal.config(text="")

# buttons - 2 row
mod = tk.Button(calFrame,text='%',bg='gray',fg='white',bd=0,command=lambda: click("%"))
mod.grid(row=2,column=0,sticky='nsew',padx=3,pady=3)

ce = tk.Button(calFrame,text='CE',bg='gray',fg='white',bd=0,command=clear_entry)
ce.grid(row=2,column=1,sticky='nsew',padx=3,pady=3)

c = tk.Button(calFrame,text='c',bg='gray',fg='white',bd=0,command = clear)
c.grid(row=2,column=2,sticky='nsew',padx=3,pady=3)

back = tk.Button(calFrame,text='⌫',bg='gray',fg='white',bd=0,command=backspace)
back.grid(row=2,column=3,sticky='nsew',padx=3,pady=3)

# button row 3
revert = tk.Button(calFrame,text='1/x',bg='gray',fg='white',bd=0,command=reciprocal)
revert.grid(row=3,column=0,sticky='nsew',padx=3,pady=3)

square = tk.Button(calFrame,text='x²',bg='gray',fg='white',bd=0,command=square_func)
square.grid(row=3,column=1,sticky='nsew',padx=3,pady=3)

root = tk.Button(calFrame,text='√',bg='gray',fg='white',bd=0,command=root_func)
root.grid(row=3,column=2,sticky='nsew',padx=3,pady=3)

# button - 3 col
div = tk.Button(calFrame,text='/',bg='#D4A017',fg='white',bd=0,command=lambda: click("/"))
div.grid(row=3,column=3,sticky='nsew',padx=3,pady=3)

mul = tk.Button(calFrame,text='x',bg='#D4A017',fg='white',bd=0,command=lambda: click("*"))
mul.grid(row=4,column=3,sticky='nsew',padx=3,pady=3)

sub = tk.Button(calFrame,text='-',bg='#D4A017',fg='white',bd=0,command=lambda: click("-"))
sub.grid(row=5,column=3,sticky='nsew',padx=3,pady=3)

add = tk.Button(calFrame,text='+',bg='#D4A017',fg='white',bd=0,command=lambda: click("+"))
add.grid(row=6,column=3,sticky='nsew',padx=3,pady=3)

ans = tk.Button(calFrame,text='=',bg='#D4A017',fg='white',bd=0,command=calculate)
ans.grid(row=7,column=3,sticky='nsew',padx=3,pady=3)

# button - 7 row
sign = tk.Button(calFrame,text='+/-',bg="#3B3B3B",fg='white',bd=0,command=change_sign)
sign.grid(row=7,column=0,sticky='nsew',padx=3,pady=3)

zero = tk.Button(calFrame,text='0',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("0"))
zero.grid(row=7,column=1,sticky='nsew',padx=3,pady=3)

decimal = tk.Button(calFrame,text='.',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("."))
decimal.grid(row=7,column=2,sticky='nsew',padx=3,pady=3)


# button- numbers

one = tk.Button(calFrame,text='1',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("1"))
one.grid(row=6,column=0,padx=3,pady=3,sticky='nsew')

two = tk.Button(calFrame,text='2',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("2"))
two.grid(row=6,column=1,padx=3,pady=3,sticky='nsew')

three = tk.Button(calFrame,text='3',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("3"))
three.grid(row=6,column=2,padx=3,pady=3,sticky='nsew')

four = tk.Button(calFrame,text='4',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("4"))
four.grid(row=5,column=0,padx=3,pady=3,sticky='nsew')

five = tk.Button(calFrame,text='5',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("5"))
five.grid(row=5,column=1,padx=3,pady=3,sticky='nsew')

six = tk.Button(calFrame,text='6',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("6"))
six.grid(row=5,column=2,padx=3,pady=3,sticky='nsew')

seven = tk.Button(calFrame,text='7',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("7"))
seven.grid(row=4,column=0,padx=3,pady=3,sticky='nsew')

eight = tk.Button(calFrame,text='8',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("8"))
eight.grid(row=4,column=1,padx=3,pady=3,sticky='nsew')

nine = tk.Button(calFrame,text='9',bg='#3B3B3B',fg='white',bd=0,command=lambda: click("9"))
nine.grid(row=4,column=2,padx=3,pady=3,sticky='nsew')

win.mainloop()