# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:22:01 2021

@author: User
"""

from tkinter import *
import pioneer_field


class Cell(Button):
    '''Ячейка поля'''

    def __init__(self, master, value):
        super().__init__(master)
        self.value = value
        self.configure(command=self.check_value, width=3, height=1)

    def reveal(self):
        '''раскрывает ячейкую. если мина - красит в красный'''
        self.configure(text=self.value, relief=SUNKEN)

    def check_value(self):
        '''проверяет значение ячейки.
        если пусто - раскрывает и проверяет соседей.
        если мина - конец.
        если колво пустых клеток = колво мин - победа.'''
        if not self.master.master.defeat and not self.master.master.victory:
            self.reveal()
            self.master.master.step_counter += 1
            # print(self.master.master.step_counter)
            if self['text'] == '@':
                # self['bg'] = 'red'
                self.master.master.gameover()
                self.master.master.defeat = True
            elif self['text'] == ' ':
                coord = self.grid_info()['column'] + 1 + self.grid_info()['row'] * self.master.master.w
                neighbours_coord = [1, -1, -self.master.master.h, -self.master.master.h - 1,
                                    -self.master.master.h + 1, self.master.master.h - 1,
                                    self.master.master.h, self.master.master.h + 1]
                if self.grid_info()['column'] == 0:
                    neighbours_coord.remove(self.master.master.h - 1)
                    neighbours_coord.remove(-1)
                    neighbours_coord.remove(-self.master.master.h - 1)
                if self.grid_info()['column'] + 1 == self.master.master.h:
                    neighbours_coord.remove(-self.master.master.h + 1)
                    neighbours_coord.remove(1)
                    neighbours_coord.remove(self.master.master.h + 1)
                for n in neighbours_coord:
                    if 0 < (coord + n) <= (self.master.master.h * self.master.master.w):
                        if coord + n != 1 and self.master.children['!cell'+str(coord+n)]['text'] == '':
                            self.master.children['!cell'+str(coord+n)].reveal()
                            self.master.children['!cell'+str(coord+n)].check_value()
                        elif coord + n == 1 and self.master.children['!cell']['text'] == '':
                            self.master.children['!cell'].reveal()
                            self.master.children['!cell'].check_value()
            elif self.master.master.step_counter == self.master.master.h * self.master.master.w - self.master.master.mines:
                self.master.master.win()
                self.master.master.victory = True


class Status_line(Label):
    '''строка состояния. изначально отображает количество мин'''

    def __init__(self, master=Label):
        super().__init__()
        self.grid(row=0, column=2, sticky='e')
        # self.configure(text='mines: ' + str(self.master.mines))

    def gameover(self):
        self.configure(text='You Loose!')

    def win(self):
        self.configure(text='You Win!')


class Restart_bttn(Button):
    '''кнопка рестарта'''

    def __init__(self, master=Button):
        super().__init__()
        self.grid(row=0, column=1, sticky='n')
        self.configure(text='restart', command=self.restart)

    def restart(self):
        '''удаляет поле и статуслайн.
        запускает игру заново со старыми параметрами'''
        self.master.end_game()
        self.master.play()


class Timer(Label):
    '''таймер'''

    def __init__(self, master=Label):
        super().__init__()
        self.configure(text='Time:')
        self.grid(row=0, column=0, sticky='w')


class Game_menu(Menu):
    '''меню'''

    def __init__(self, master=Menu):
        super().__init__()
        self.menu1 = self.add_command(label='New game', command=self.newgame)

    def newgame(self):
        self.master.new_game()


class Mesh(Frame):
    '''поле. основано на матрице из модуля pioneer_field.py'''

    def __init__(self, master, field):
        super().__init__(master)
        self.grid(row=3, columnspan=3)
        self.mesh1 = self.create_mesh(field)

    def create_mesh(self, field):
        for row in range(self.master.h):
            for col in range(self.master.w):
                if int(field[row][col]) == 0:
                    btn_value = ' '
                elif int(field[row][col]) == -1:
                    btn_value = '@'
                else:
                    btn_value = int(field[row][col])
                self.btn = Cell(self, btn_value)
                self.btn['text'] = ''
                self.btn.grid(row=row, column=col)


class New_game_window(Tk):
    '''окно новой игры. здесь задаются параметры игры'''

    def __init__(self, master=Tk):
        super().__init__()
        self.ng_frame = Frame(self)
        self.ng_frame.grid()
        Label(self.ng_frame, text='SETTINGS').grid(column=0, row=0, columnspan=2)
        Label(self.ng_frame, text='width: ').grid(column=0, row=1)
        self.width_ent = Entry(self.ng_frame)
        self.width_ent.grid(column=1, row=1)
        Label(self.ng_frame, text='height: ').grid(column=0, row=2)
        self.height_ent = Entry(self.ng_frame)
        self.height_ent.grid(column=1, row=2)
        Label(self.ng_frame, text='mines: ').grid(column=0, row=3)
        self.mines_ent = Entry(self.ng_frame)
        self.mines_ent.grid(column=1, row=3)


class Game(Tk):
    def __init__(self, master=Tk):
        super().__init__()
        self.new_game()
        # self.h = int(self.settings.height_ent.get())
        # self.w = int(self.settings.width_ent.get())
        # self.mines = int(self.settings.mines_ent.get())
        self.configure(menu=Game_menu())
        # self.mine_img = PhotoImage(file='mine111.png')

    def play(self):
        self.restart_bttn = Restart_bttn(self)
        self.status = Status_line(self)
        self.timer = Timer(self)
        self.new_field = pioneer_field.create_field(self.h, self.w, self.mines)
        self.new_mesh = Mesh(self, self.new_field)
        self.step_counter = 0
        self.defeat = False
        self.victory = False
        self.mainloop()

    def new_game(self):
        # self.settings = New_game_window(self)
        self.h = int(input('высота: '))
        self.w = int(input('ширина: '))
        self.mines = int(input('мины: '))

    def end_game(self):
        self.new_mesh.destroy()
        self.status.destroy()
        self.timer.destroy()
        self.restart_bttn.destroy()

    def gameover(self):
        for bttn in self.new_mesh.children:
            self.new_mesh.children[bttn].reveal()
            if self.new_mesh.children[bttn]['text'] == '@':
                self.new_mesh.children[bttn]['bg'] = 'red'
        self.status.gameover()

    def win(self):
        for bttn in self.new_mesh.children:
            self.new_mesh.children[bttn].reveal()
            if self.new_mesh.children[bttn]['text'] == '@':
                self.new_mesh.children[bttn]['bg'] = 'green'
        self.status.win()


new_game = Game()
new_game.play()
