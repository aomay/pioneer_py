# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:30:18 2021

@author: User
"""

import numpy as np
import random


def planting(matrix, q):
    '''случайно расставляет мины(-1) по полю
    h - field height
    w - field width
    q - number of mines'''
    h = matrix.shape[0]
    w = matrix.shape[1]
    mines_pos = np.array(random.sample(range(h*w), k=q)) + 1
    # mines_pos = [10, 16, 4, 11, 4, 2]
    count = 0
    for i in range(h):
        for j in range(w):
            count += 1
            if count in mines_pos:
                matrix[i][j] = -1


def find_num(matrix, i, j):
    h = matrix.shape[0]
    w = matrix.shape[1]
    for n in (-1, 0, 1):
        for k in (-1, 0, 1):
            if ((0 <= j+k < w)
                    and (0 <= i+n < h)
                    and not (n == 0 and k == 0)
                    and (matrix[i+n][j+k] == -1)):
                matrix[i][j] += 1


def populate_field(matrix):
    '''определяет число в каждой ячейке(количество мин-соседей)'''
    h = matrix.shape[0]
    w = matrix.shape[1]
    for i in range(h):
        for j in range(w):
            if matrix[i][j] != -1:
                find_num(matrix, i, j)


def create_field(height, width, mines):
    matrix = np.zeros((height, width))
    planting(matrix, mines)
    populate_field(matrix)
    return matrix
