import tkinter as tk
import re

root = tk.Tk()
root.title("Calculator")
root.geometry("400x700")
root.resizable(False, False)
root.configure(bg="black")

current_input = ""
previous_result = ""

COLORS = {
    "display_bg": "#000000",
    "display_fg": "#FFFFFF",
    "light_gray": "#A5A5A5",
    "dark_gray": "#333333",
    "orange": "#FF9500",
    "orange_pressed": "#FFB74D",
    "gray_pressed": "#737373",
    "dark_gray_pressed": "#5A5A5A",
    "light_gray_pressed": "#B5B5B5"
}

def update_display():
    if current_input:
        display_text.set(current_input)
    else:
        display_text.set(previous_result if previous_result else "0")

display_text = tk.StringVar()
display_text.set("0")

display = tk.Label(root, 
                   textvariable=display_text,
                   font=("Helvetica Neue", 72, "normal"),
                   bg=COLORS["display_bg"],
                   fg=COLORS["display_fg"],
                   anchor="e",
                   padx=30)
display.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(100, 20))

def on_number_click(num):
    global current_input
    
    if len(current_input) >= 12:
        return
        
    if current_input == "0" or current_input == "Error":
        current_input = str(num)
    else:
        current_input += str(num)
    
    update_display()

def on_operation_click(op):
    global current_input, previous_result
    
    if not current_input:
        if previous_result:
            current_input = previous_result
        else:
            current_input = "0"
    
    operators = ['+', '-', '×', '÷']
    if current_input and current_input[-1] in operators:
        current_input = current_input[:-1]
    
    op_symbol = op
    if op == "*":
        op_symbol = "×"
    elif op == "/":
        op_symbol = "÷"
    
    current_input += op_symbol
    update_display()

def on_clear():
    global current_input, previous_result
    current_input = ""
    previous_result = ""
    display_text.set("0")

def on_clear_entry():
    global current_input
    current_input = ""
    update_display()

def on_delete():
    global current_input
    if current_input:
        current_input = current_input[:-1]
        update_display()
    else:
        display_text.set("0")

def on_decimal():
    global current_input
    
    if not current_input:
        current_input = "0."
    elif '.' not in current_input.split()[-1]:
        current_input += "."
    elif current_input[-1] in ['+', '-', '×', '÷']:
        current_input += "0."
    
    update_display()

def on_percentage():
    global current_input
    
    try:
        if current_input:
            expression = current_input.replace("×", "*").replace("÷", "/")
            result = eval(expression)
            current_input = str(result / 100)
        elif previous_result:
            current_input = str(float(previous_result) / 100)
        update_display()
    except:
        current_input = "Error"
        update_display()

def on_equals():
    global current_input, previous_result
    
    if not current_input:
        return
    
    try:
        expression = current_input.replace("×", "*").replace("÷", "/")
        result = eval(expression)
        
        if result.is_integer():
            result_str = str(int(result))
        else:
            result_str = "{:g}".format(result)
        
        if len(result_str) > 12:
            result_str = "{:.10e}".format(result)
        
        previous_result = result_str
        current_input = ""
        display_text.set(result_str)
    except:
        current_input = ""
        previous_result = ""
        display_text.set("Error")

def on_plus_minus():
    global current_input
    
    if not current_input:
        if previous_result:
            current_input = previous_result
        else:
            return
    
    parts = re.split(r'([+\-×÷])', current_input)
    
    if parts:
        last_num = parts[-1]
        if last_num and last_num != "Error":
            if last_num.startswith('-'):
                parts[-1] = last_num[1:]
            else:
                parts[-1] = '-' + last_num
            current_input = ''.join(parts)
            update_display()

class CircularButton:
    def __init__(self, parent, text, color="dark_gray", command=None, row=0, col=0, col_span=1):
        self.parent = parent
        self.text = text
        self.color = color
        self.command = command
        self.row = row
        self.col = col
        self.col_span = col_span
        
        if text in ['AC', '±', '%']:
            font_size = 30
            text_color = "#000000"
        elif text in ['+', '-', '×', '÷', '=']:
            font_size = 40
            text_color = "#FFFFFF"
        elif text == '0':
            font_size = 28
            text_color = "#FFFFFF"
        else:
            font_size = 32
            text_color = "#FFFFFF"
        
        self.canvas = tk.Canvas(parent, 
                                width=80, 
                                height=80, 
                                bg="black", 
                                highlightthickness=0,
                                relief="flat")
        
        self.circle = self.canvas.create_oval(2, 2, 78, 78, 
                                             fill=COLORS[color], 
                                             outline=COLORS[color])
        
        self.text_id = self.canvas.create_text(40, 40, 
                                              text=text,
                                              font=("Helvetica Neue", font_size, "normal"),
                                              fill=text_color)
        
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        
        self.original_color = COLORS[color]
        self.pressed_color = COLORS.get(f"{color}_pressed", self.original_color)
        
        self.canvas.grid(row=row, column=col, columnspan=col_span, 
                         padx=3, pady=3, sticky="nsew")
    
    def on_press(self, event):
        self.canvas.itemconfig(self.circle, fill=self.pressed_color)
    
    def on_release(self, event):
        self.canvas.itemconfig(self.circle, fill=self.original_color)
        if self.command:
            self.command()
    
    def on_enter(self, event):
        current_color = self.canvas.itemcget(self.circle, "fill")
        if current_color == self.original_color:
            self.canvas.itemconfig(self.circle, fill=self.pressed_color)
    
    def on_leave(self, event):
        self.canvas.itemconfig(self.circle, fill=self.original_color)

buttons_frame = tk.Frame(root, bg="black")
buttons_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

buttons = []

buttons.append(CircularButton(buttons_frame, "AC", "light_gray", on_clear_entry, 0, 0))
buttons.append(CircularButton(buttons_frame, "±", "light_gray", on_plus_minus, 0, 1))
buttons.append(CircularButton(buttons_frame, "%", "light_gray", on_percentage, 0, 2))
buttons.append(CircularButton(buttons_frame, "÷", "orange", lambda: on_operation_click("/"), 0, 3))

buttons.append(CircularButton(buttons_frame, "7", "dark_gray", lambda: on_number_click(7), 1, 0))
buttons.append(CircularButton(buttons_frame, "8", "dark_gray", lambda: on_number_click(8), 1, 1))
buttons.append(CircularButton(buttons_frame, "9", "dark_gray", lambda: on_number_click(9), 1, 2))
buttons.append(CircularButton(buttons_frame, "×", "orange", lambda: on_operation_click("*"), 1, 3))

buttons.append(CircularButton(buttons_frame, "4", "dark_gray", lambda: on_number_click(4), 2, 0))
buttons.append(CircularButton(buttons_frame, "5", "dark_gray", lambda: on_number_click(5), 2, 1))
buttons.append(CircularButton(buttons_frame, "6", "dark_gray", lambda: on_number_click(6), 2, 2))
buttons.append(CircularButton(buttons_frame, "-", "orange", lambda: on_operation_click("-"), 2, 3))

buttons.append(CircularButton(buttons_frame, "1", "dark_gray", lambda: on_number_click(1), 3, 0))
buttons.append(CircularButton(buttons_frame, "2", "dark_gray", lambda: on_number_click(2), 3, 1))
buttons.append(CircularButton(buttons_frame, "3", "dark_gray", lambda: on_number_click(3), 3, 2))
buttons.append(CircularButton(buttons_frame, "+", "orange", lambda: on_operation_click("+"), 3, 3))

class WideCircularButton:
    def __init__(self, parent, text, color="dark_gray", command=None, row=0, col=0, col_span=2):
        self.parent = parent
        self.text = text
        self.color = color
        self.command = command
        self.row = row
        self.col = col
        self.col_span = col_span
        
        self.canvas = tk.Canvas(parent, 
                                width=166,
                                height=80, 
                                bg="black", 
                                highlightthickness=0,
                                relief="flat")
        
        self.shape = self.canvas.create_rounded_rectangle(2, 2, 164, 78, 
                                                         radius=40,
                                                         fill=COLORS[color], 
                                                         outline=COLORS[color])
        
        self.text_id = self.canvas.create_text(50, 40, 
                                              text=text,
                                              font=("Helvetica Neue", 28, "normal"),
                                              fill="#FFFFFF",
                                              anchor="w")
        
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        
        self.original_color = COLORS[color]
        self.pressed_color = COLORS.get(f"{color}_pressed", self.original_color)
        
        self.canvas.grid(row=row, column=col, columnspan=col_span, 
                         padx=3, pady=3, sticky="nsew")
    
    def on_press(self, event):
        self.canvas.itemconfig(self.shape, fill=self.pressed_color)
    
    def on_release(self, event):
        self.canvas.itemconfig(self.shape, fill=self.original_color)
        if self.command:
            self.command()
    
    def on_enter(self, event):
        current_color = self.canvas.itemcget(self.shape, "fill")
        if current_color == self.original_color:
            self.canvas.itemconfig(self.shape, fill=self.pressed_color)
    
    def on_leave(self, event):
        self.canvas.itemconfig(self.shape, fill=self.original_color)

def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

wide_zero_button = WideCircularButton(buttons_frame, "0", "dark_gray", 
                                     lambda: on_number_click(0), 4, 0, 2)
buttons.append(CircularButton(buttons_frame, ".", "dark_gray", on_decimal, 4, 2))
buttons.append(CircularButton(buttons_frame, "=", "orange", on_equals, 4, 3))

for i in range(5):
    buttons_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    buttons_frame.grid_columnconfigure(i, weight=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

def on_key_press(event):
    key = event.char
    if key in '0123456789':
        on_number_click(key)
    elif key in '+-*/':
        on_operation_click(key)
    elif key == '\r' or key == '=':
        on_equals()
    elif key == '\x08':
        on_delete()
    elif key == '\x1b':
        on_clear()
    elif key == '.':
        on_decimal()
    elif key == '%':
        on_percentage()
    elif key == 'c' or key == 'C':
        on_clear_entry()

root.bind('<Key>', on_key_press)
display.focus_set()

root.mainloop()