# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:22:01 2021

@author: User
"""

from tkinter import *
import numpy as np
import pioneer_field


class Sell(Button):
    def __init__(self, master, value):
        super().__init__(master)
        self.value = value
        self.configure(command=self.reveal, width=3, height=1)

    def reveal(self):
        self.configure(text=self.value)


class Mesh(Frame):
    def __init__(self, master, field):
        super().__init__(master)
        self.grid()
        self.create_mesh(field)

    def create_mesh(self, field):
        h = field.shape[0]
        w = field.shape[1]
        for row in range(h):
            for col in range(w):
                btn_value = int(field[row][col])
                btn = Sell(self, btn_value)
                btn['text'] = ''
                btn.grid(row=row, column=col)

    # def check_area(self, sell):
    #     h = field.shape[0]
    #     w = field.shape[1]
    #     for n in (-1, 0, 1):
    #         for k in (-1, 0, 1):
    #             if ((0 <= j+k < w) and (0 <= i+n < h) and not (n == 0 and k == 0) and (sell[i+n][j+k][text]=='') and (sell[i+n][j+k] == 0)):
    #                 sell[i+n][j+k].reveal()
    #                 sell[i+n][j+k].check_neighbors(self)
    #             elif ((0 <= j+k < w) and (0 <= i+n < h) and not (n == 0 and k == 0) and (sell[i+n][j+k][text]=='') and (sell[i+n][j+k] != 0)):
    #                 sell[i+n][j+k].reveal()


def main():
    root = Tk()
    root.title('pioneer')
    h = 10
    w = 10
    m = 10
    field1 = pioneer_field.create_field(h, w, m)
    app = Mesh(root, field1)
    root.mainloop()


main()


# class Game(object):
#     def __init__(self):
#         self.root = Tk()
#         # self.root.geometry('200x200')
#         self.root.title('pioneer')
#         app = Application(self.root)
#         self.play(self.root)

#     def play(self, root):
#         root.mainloop()


# game1 = Game()
