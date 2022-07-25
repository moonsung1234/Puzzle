
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

pc = Slice("img/nature.jpg", 4, width=600, height=600)
copy_pieces = [(pc.pieces[i], pc.piece_paths[i]) for i in range(len(pc.pieces))]
pieces = []
table = []

random.shuffle(copy_pieces)

target_piece_index = None
target_table_index = None
padding_value = 50

for i in range(int(sqrt(pc.piece_count))) :
    for j in range(int(sqrt(pc.piece_count))) :
        piece_info = copy_pieces[int(i * sqrt(pc.piece_count) + j)]
        piece = ImageTk.PhotoImage(Image.open(piece_info[1]))
        piece_x = pc.piece_width * j + pc.piece_width / 2
        piece_y = pc.piece_height * i + pc.piece_height / 2 + padding_value

        table_x = canvas_width / 2 + pc.piece_width * j
        table_y = pc.piece_height * i + padding_value

        pieces.append({
            "path" : piece_info[1],
            "piece" : piece,
            "x_range" : (pc.piece_width * j, pc.piece_width * (j + 1)),
            "y_range" : (pc.piece_height * i + padding_value, pc.piece_height * (i + 1) + padding_value),
            "is_set" : True
        })

        table.append({
            "x_range": (table_x, table_x + pc.piece_width),
            "y_range" : (table_y, table_y + pc.piece_height)
        })

        canvas.create_image(piece_x, piece_y, image=piece)
        canvas.create_rectangle(table_x, table_y, table_x + pc.piece_width, table_y + pc.piece_height, fill="white")

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

def callback(e):
    global target_piece_index

    clicked_piece_index = get_clicked_piece(e.x, e.y)

    if clicked_piece_index != None :
        target_piece_index = clicked_piece_index 

def move(e) :
    global target_piece_index, target_table_index

    if target_piece_index != None :
        # process about table
        table_on_index = get_table_on(e.x, e.y)

        if table_on_index != None :
            x1, x2 = table[table_on_index]["x_range"]
            y1, y2 = table[table_on_index]["y_range"]

            canvas.create_rectangle(x1, y1, x2, y2, fill="red")

            if target_table_index != None and target_table_index != table_on_index :
                x1, x2 = table[target_table_index]["x_range"]
                y1, y2 = table[target_table_index]["y_range"]

                canvas.create_rectangle(x1, y1, x2, y2, fill="white")

            target_table_index = table_on_index

        elif target_table_index != None :
            x1, x2 = table[target_table_index]["x_range"]
            y1, y2 = table[target_table_index]["y_range"]
            
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")

        # process about piece
        if pieces[target_piece_index]["is_set"] :
            pieces[target_piece_index]["is_set"] = False

            x1, x2 = pieces[target_piece_index]["x_range"]
            y1, y2 = pieces[target_piece_index]["y_range"]

            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

        pieces[target_piece_index]["piece"] = ImageTk.PhotoImage(Image.open(pieces[target_piece_index]["path"]))
        pieces[target_piece_index]["x_range"] = (e.x - int(pc.piece_width / 2) , e.x + int(pc.piece_width / 2))
        pieces[target_piece_index]["y_range"] = (e.y - int(pc.piece_height / 2), e.y + int(pc.piece_height / 2))

        canvas.create_image(e.x, e.y, image=pieces[target_piece_index]["piece"])

def end(e) :
    global target_piece_index, target_table_index

    if target_piece_index != None :
        table_on_index = get_table_on(e.x, e.y)

        if table_on_index != None :
            x1, x2 = table[table_on_index]["x_range"]
            y1, y2 = table[table_on_index]["y_range"]

            canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")

            pieces[target_piece_index]["piece"] = ImageTk.PhotoImage(Image.open(pieces[target_piece_index]["path"]))
            pieces[target_piece_index]["x_range"] = (x1 , x1 + pc.piece_width)
            pieces[target_piece_index]["y_range"] = (y1, y1 + pc.piece_height)

            canvas.create_image(x1 + int(pc.piece_width / 2), y1 + int(pc.piece_height / 2), image=pieces[target_piece_index]["piece"])

            thread = Thread(target=playsound, args=("sound/ttak.mp3",))
            thread.start()

canvas.bind("<Button-1>", callback)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", end)

window.mainloop()