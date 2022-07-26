
from PIL import ImageTk, Image
from playsound import playsound 
from threading import Thread
from slice import *
import tkinter as tk
import random

class Puzzle :
    def __get_clicked_piece(self, x, y) :
        for i in range(len(self.pieces)) :
            x1, x2 = self.pieces[i]["x_range"]
            y1, y2 = self.pieces[i]["y_range"]

            if x1 <= x <= x2 and y1 <= y <= y2 :
                return i

        return None

    def __get_table_on(self, x, y) :
        for i in range(len(self.table)) : 
            x1, x2 = self.table[i]["x_range"]
            y1, y2 = self.table[i]["y_range"]

            if x1 <= x <= x2 and y1 <= y <= y2 :
                return i

        return None

    def __add_pinned_piece(self, piece_index) :
        if piece_index not in self.pinned_pieces :
            self.pinned_pieces.append(piece_index)

    def __delete_pinned_piece(self, piece_index) :
        if piece_index in self.pinned_pieces :
            # print(pieces[pinned_pieces.index(piece_index)]["path"])

            del self.pinned_pieces[self.pinned_pieces.index(piece_index)]

    def __pin_piece(self) :
        for i in range(len(self.pinned_pieces)) :
            self.pieces[self.pinned_pieces[i]]["piece"] = ImageTk.PhotoImage(Image.open(self.pieces[self.pinned_pieces[i]]["path"]))
            x1, y1 = self.pieces[self.pinned_pieces[i]]["x_range"][0] + int(self.pc.piece_width / 2), self.pieces[self.pinned_pieces[i]]["y_range"][0] + int(self.pc.piece_height / 2)
        
            self.canvas.create_image(x1, y1, image=self.pieces[self.pinned_pieces[i]]["piece"])

    def __process_click(self, x, y) :
        clicked_piece_index = self.__get_clicked_piece(x, y)

        if clicked_piece_index != None :
            self.target_piece_index = clicked_piece_index 

    def __process_table(self, x, y) :
        if self.target_piece_index != None :
            table_on_index = self.__get_table_on(x, y)

            if table_on_index != None :
                self.canvas.delete(self.table[table_on_index]["table"])

                x1, x2 = self.table[table_on_index]["x_range"]
                y1, y2 = self.table[table_on_index]["y_range"]

                self.table[table_on_index]["table"] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

                if self.target_table_index != None and self.target_table_index != table_on_index :
                    self.canvas.delete(self.table[self.target_table_index]["table"])

                    x1, x2 = self.table[self.target_table_index]["x_range"]
                    y1, y2 = self.table[self.target_table_index]["y_range"]

                    self.table[self.target_table_index]["table"] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

                self.target_table_index = table_on_index

            elif self.target_table_index != None :
                self.canvas.delete(self.table[self.target_table_index]["table"])

                x1, x2 = self.table[self.target_table_index]["x_range"]
                y1, y2 = self.table[self.target_table_index]["y_range"]
                
                self.table[self.target_table_index]["table"] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def __process_piece(self, x, y) :
        if self.target_piece_index != None :
            if self.pieces[self.target_piece_index]["is_set"] :
                self.pieces[self.target_piece_index]["is_set"] = False

                x1, x2 = self.pieces[self.target_piece_index]["x_range"]
                y1, y2 = self.pieces[self.target_piece_index]["y_range"]

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

            self.__delete_pinned_piece(self.target_piece_index)
            self.__pin_piece()

            self.pieces[self.target_piece_index]["piece"] = ImageTk.PhotoImage(Image.open(self.pieces[self.target_piece_index]["path"]))
            self.pieces[self.target_piece_index]["x_range"] = (x - int(self.pc.piece_width / 2) , x + int(self.pc.piece_width / 2))
            self.pieces[self.target_piece_index]["y_range"] = (y - int(self.pc.piece_height / 2), y + int(self.pc.piece_height / 2))

            self.canvas.create_image(x, y, image=self.pieces[self.target_piece_index]["piece"])  

    def __process_pinned_piece(self, x, y) :
        if self.target_piece_index != None :
            table_on_index = self.__get_table_on(x, y)

            if table_on_index != None :
                self.canvas.delete(self.table[table_on_index]["table"])

                x1, x2 = self.table[table_on_index]["x_range"]
                y1, y2 = self.table[table_on_index]["y_range"]

                self.table[table_on_index]["table"] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="")

                self.pieces[self.target_piece_index]["x_range"] = (x1, x1 + self.pc.piece_width)
                self.pieces[self.target_piece_index]["y_range"] = (y1, y1 + self.pc.piece_height)

                Thread(target=playsound, args=("sound/ttak.mp3",)).start()

                self.__add_pinned_piece(self.target_piece_index)
                self.__pin_piece()

    def __callback(self, e):
        Thread(target=self.__process_click, args=(e.x, e.y,)).start()
        # process_click(e.x, e.y)

    def __move(self, e) :
        self.__process_table(e.x, e.y)
        self.__process_piece(e.x, e.y)

    def __end(self, e) :
        Thread(target=self.__process_pinned_piece, args=(e.x, e.y,)).start()
        # process_pinned_piece(e.x, e.y)

    def __init__(self, img_path, piece_count, window_width = 1300, canvas_width = 1300, canvas_height = 700, window_height = 700, piece_width=600, piece_height=600) :
        self.img_path = img_path
        self.piece_count = piece_count
        self.piece_width = piece_width
        self.piece_height = piece_height

        self.window = tk.Tk()
        self.window_width = window_width
        self.window_height = window_height

        self.window.title("puzzle")
        self.window.geometry("{}x{}".format(self.window_width, self.window_height))
        self.window.resizable(False, False)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.pc = Slice(self.img_path, self.piece_count, width=self.piece_width, height=self.piece_height)
        self.copy_pieces = [(self.pc.pieces[i], self.pc.piece_paths[i]) for i in range(len(self.pc.pieces))]
        self.pieces = []
        self.table = []

        random.shuffle(self.copy_pieces)

        self.target_piece_index = None
        self.target_table_index = None
        self.pinned_pieces = []
        self.padding_value = 50 #default

    def show(self) :
        for i in range(int(sqrt(self.pc.piece_count))) :
            for j in range(int(sqrt(self.pc.piece_count))) :
                piece_info = self.copy_pieces[int(i * sqrt(self.pc.piece_count) + j)]
                piece = ImageTk.PhotoImage(Image.open(piece_info[1]))
                piece_x = self.pc.piece_width * j + self.pc.piece_width / 2
                piece_y = self.pc.piece_height * i + self.pc.piece_height / 2 + self.padding_value

                table_x = self.canvas_width / 2 + self.pc.piece_width * j
                table_y = self.pc.piece_height * i + self.padding_value

                self.canvas.create_image(piece_x, piece_y, image=piece)
                rectangle = self.canvas.create_rectangle(table_x, table_y, table_x + self.pc.piece_width, table_y + self.pc.piece_height, fill="white")
                
                self.pieces.append({
                    "path" : piece_info[1],
                    "piece" : piece,
                    "x_range" : (self.pc.piece_width * j, self.pc.piece_width * (j + 1)),
                    "y_range" : (self.pc.piece_height * i + self.padding_value, self.pc.piece_height * (i + 1) + self.padding_value),
                    "is_set" : True
                })

                self.table.append({
                    "table" : rectangle,
                    "x_range": (table_x, table_x + self.pc.piece_width),
                    "y_range" : (table_y, table_y + self.pc.piece_height)
                })

        self.canvas.bind("<Button-1>", self.__callback)
        self.canvas.bind("<B1-Motion>", self.__move)
        self.canvas.bind("<ButtonRelease-1>", self.__end)

        self.window.mainloop()
