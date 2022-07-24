
from PIL import ImageTk, Image
from matplotlib import image
from slice import *
import tkinter as tk
import os

window = tk.Tk()

window.title("puzzle")
window.geometry("1300x700")
window.resizable(False, False)

canvas = tk.Canvas(window, width=1200, height=700, bg="white")
canvas.pack(pady=20)

pc = Slice("img/nature.jpg", 9, width=600, height=600)
pieces = []

target_piece_index = None

for i in range(int(sqrt(pc.piece_count))) :
    for j in range(int(sqrt(pc.piece_count))) :
        piece = ImageTk.PhotoImage(Image.open(pc.piece_paths[int(i * sqrt(pc.piece_count) + j)]))
        piece_x = pc.piece_width * j + pc.piece_width / 2
        piece_y = pc.piece_height * i + pc.piece_height / 2

        canvas.create_image(piece_x, piece_y, image=piece)
        pieces.append({
            "path" : pc.piece_paths[int(i * sqrt(pc.piece_count) + j)],
            "piece" : piece,
            "x_range" : (pc.piece_width * (j), pc.piece_width * (j + 1) ),
            "y_range" : (pc.piece_height * (i), pc.piece_height * (i + 1))
        })

canvas.create_image(1000, 100, image=ImageTk.PhotoImage(Image.open(pc.piece_paths[0])))

def get_clicked_piece(x, y) :
    for i in range(len(pieces)) :
        x1, x2 = pieces[i]["x_range"]
        y1, y2 = pieces[i]["y_range"]

        if x1 <= x <= x2 and y1 <= y <= y2 :
            return i

    return None

def key(e) :
    print("pressed ", repr(e.char))

def callback(e):
    global target_piece_index

    clicked_piece_index = get_clicked_piece(e.x, e.y)

    if clicked_piece_index != None :
        target_piece_index = clicked_piece_index 

        print(pieces[target_piece_index]["path"])
        print(clicked_piece_index)

def move(e) :
    global target_piece_index

    if target_piece_index != None :
        pieces[target_piece_index]["piece"] = ImageTk.PhotoImage(Image.open(pieces[target_piece_index]["path"]))
        pieces[target_piece_index]["x_range"] = (e.x - int(pc.piece_width / 2) , e.x + int(pc.piece_width / 2))
        pieces[target_piece_index]["y_range"] = (e.y - int(pc.piece_height / 2), e.y + int(pc.piece_height / 2))

        canvas.create_image(e.x, e.y, image=pieces[target_piece_index]["piece"])

        print(e.x, e.y)

canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.bind("<B1-Motion>", move)

window.mainloop()