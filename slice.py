
from math import sqrt
import cv2

class Slice :
    def __slice(self) :
        return_pieces = []
        return_piece_paths = []

        for i in range(int(sqrt(self.piece_count))) :
            for j in range(int(sqrt(self.piece_count))) :
                temp_x = self.piece_width * i
                temp_y = self.piece_width * j
                
                piece = self.img[temp_x:temp_x+self.piece_width, temp_y:temp_y+self.piece_height]
                piece_path = "img/piece{}{}.jpg".format(i + 1, j + 1)

                return_pieces.append(piece)
                return_piece_paths.append(piece_path)
                cv2.imwrite(piece_path, piece)

        return return_pieces, return_piece_paths

    def __init__(self, img_path, piece_count, width=500, height=500) : 
        self.img_path = img_path
        self.width = width
        self.height = height
        self.piece_count = piece_count

        self.img = cv2.resize(cv2.imread(img_path, cv2.IMREAD_COLOR), (self.width, self.height))

        self.piece_width = int(self.width / (sqrt(self.piece_count)))
        self.piece_height = int(self.height / (sqrt(self.piece_count)))

        self.pieces, self.piece_paths = self.__slice() 

