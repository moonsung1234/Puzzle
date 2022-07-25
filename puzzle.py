
from PIL import ImageTk, Image
from playsound import playsound 
from threading import Thread
from slice import *
import tkinter as tk
import random

window = tk.Tk()
window_width = 1300
window_height = 700

window.title("puzzle")
window.geometry("{}x{}".format(window_width, window_height))
window.resizable(False, False)

canvas_width = 1300
canvas_height = 700
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

pc = Slice("img/nature.jpg", 9, width=600, height=600)
copy_pieces = [(pc.pieces[i], pc.piece_paths[i]) for i in range(len(pc.pieces))]
pieces = []
table = []

random.shuffle(copy_pieces)

target_piece_index = None
target_table_index = None
pinned_pieces = []
padding_value = 50

for i in range(int(sqrt(pc.piece_count))) :
    for j in range(int(sqrt(pc.piece_count))) :
        piece_info = copy_pieces[int(i * sqrt(pc.piece_count) + j)]
        piece = ImageTk.PhotoImage(Image.open(piece_info[1]))
        piece_x = pc.piece_width * j + pc.piece_width / 2
        piece_y = pc.piece_height * i + pc.piece_height / 2 + padding_value

        table_x = canvas_width / 2 + pc.piece_width * j
        table_y = pc.piece_height * i + padding_value

        canvas.create_image(piece_x, piece_y, image=piece)
        rectangle = canvas.create_rectangle(table_x, table_y, table_x + pc.piece_width, table_y + pc.piece_height, fill="white")
        
        pieces.append({
            "path" : piece_info[1],
            "piece" : piece,
            "x_range" : (pc.piece_width * j, pc.piece_width * (j + 1)),
            "y_range" : (pc.piece_height * i + padding_value, pc.piece_height * (i + 1) + padding_value),
            "is_set" : True,
            "pinned_table_index" : None
        })

        table.append({
            "table" : rectangle,
            "x_range": (table_x, table_x + pc.piece_width),
            "y_range" : (table_y, table_y + pc.piece_height)
        })

def get_clicked_piece(x, y) :
    for i in range(len(pieces)) :
        x1, x2 = pieces[i]["x_range"]
        y1, y2 = pieces[i]["y_range"]

        if x1 <= x <= x2 and y1 <= y <= y2 :
            return i

    return None

def get_table_on(x, y) :
    for i in range(len(table)) : 
        x1, x2 = table[i]["x_range"]
        y1, y2 = table[i]["y_range"]

        if x1 <= x <= x2 and y1 <= y <= y2 :
            return i

    return None

def add_pinned_piece(piece_index) :
    if piece_index not in pinned_pieces :
        pinned_pieces.append(piece_index)

def delete_pinned_piece(piece_index) :
    if piece_index in pinned_pieces :
        # print(pieces[pinned_pieces.index(piece_index)]["path"])

        del pinned_pieces[pinned_pieces.index(piece_index)]

def check_pinned_table(table_index) :
    for i in range(len(pinned_pieces)) :
        if pieces[pinned_pieces[i]]["pinned_table_index"] == table_index :
            return True
    
    return False

def pin_piece() :
    for i in range(len(pinned_pieces)) :
        pieces[pinned_pieces[i]]["piece"] = ImageTk.PhotoImage(Image.open(pieces[pinned_pieces[i]]["path"]))
        x1, y1 = pieces[pinned_pieces[i]]["x_range"][0] + int(pc.piece_width / 2), pieces[pinned_pieces[i]]["y_range"][0] + int(pc.piece_height / 2)
      
        canvas.create_image(x1, y1, image=pieces[pinned_pieces[i]]["piece"])

def process_click(x, y) :
    global target_piece_index

    clicked_piece_index = get_clicked_piece(x, y)

    if clicked_piece_index != None :
        target_piece_index = clicked_piece_index 

def process_table(x, y) :
    global target_piece_index, target_table_index

    if target_piece_index != None :
        table_on_index = get_table_on(x, y)

        if table_on_index != None and not check_pinned_table(table_on_index) :
            canvas.delete(table[table_on_index]["table"])

            x1, x2 = table[table_on_index]["x_range"]
            y1, y2 = table[table_on_index]["y_range"]

            table[table_on_index]["table"] = canvas.create_rectangle(x1, y1, x2, y2, fill="red")

            if target_table_index != None and target_table_index != table_on_index :
                canvas.delete(table[target_table_index]["table"])

                x1, x2 = table[target_table_index]["x_range"]
                y1, y2 = table[target_table_index]["y_range"]

                table[target_table_index]["table"] = canvas.create_rectangle(x1, y1, x2, y2, fill="white")

            target_table_index = table_on_index

        elif target_table_index != None and not check_pinned_table(target_table_index) :
            canvas.delete(table[target_table_index]["table"])

            x1, x2 = table[target_table_index]["x_range"]
            y1, y2 = table[target_table_index]["y_range"]
            
            table[target_table_index]["table"] = canvas.create_rectangle(x1, y1, x2, y2, fill="white")

def process_piece(x, y) :
    global target_piece_index, target_table_index

    if target_piece_index != None :
        if pieces[target_piece_index]["is_set"] :
            pieces[target_piece_index]["is_set"] = False

            x1, x2 = pieces[target_piece_index]["x_range"]
            y1, y2 = pieces[target_piece_index]["y_range"]

            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

        delete_pinned_piece(target_piece_index)
        pin_piece()

        pieces[target_piece_index]["piece"] = ImageTk.PhotoImage(Image.open(pieces[target_piece_index]["path"]))
        pieces[target_piece_index]["x_range"] = (x - int(pc.piece_width / 2) , x + int(pc.piece_width / 2))
        pieces[target_piece_index]["y_range"] = (y - int(pc.piece_height / 2), y + int(pc.piece_height / 2))

        canvas.create_image(x, y, image=pieces[target_piece_index]["piece"])  

def process_pinned_piece(x, y) :
    global target_piece_index, target_table_index

    if target_piece_index != None :
        table_on_index = get_table_on(x, y)

        if table_on_index != None :
            canvas.delete(table[table_on_index]["table"])

            x1, x2 = table[table_on_index]["x_range"]
            y1, y2 = table[table_on_index]["y_range"]

            table[table_on_index]["table"] = canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")

            pieces[target_piece_index]["x_range"] = (x1, x1 + pc.piece_width)
            pieces[target_piece_index]["y_range"] = (y1, y1 + pc.piece_height)

            thread = Thread(target=playsound, args=("sound/ttak.mp3",))
            thread.start()

            add_pinned_piece(target_piece_index)
            pin_piece()

def callback(e):
    Thread(target=process_click, args=(e.x, e.y,)).start()
    # process_click(e.x, e.y)

def move(e) :
    process_table(e.x, e.y)
    process_piece(e.x, e.y)

def end(e) :
    Thread(target=process_pinned_piece, args=(e.x, e.y,)).start()
    # process_pinned_piece(e.x, e.y)

canvas.bind("<Button-1>", callback)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", end)

window.mainloop()