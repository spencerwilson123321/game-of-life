#!/usr/bin/env python3
import tkinter
import time
import threading


class Game:
    def __init__(self, cells, rowsize, colsize):
        self.cells = cells
        self.rowsize = rowsize
        self.colsize = colsize
        self.tickrate = 5.0
        self.tickperiod = 1.0 / self.tickrate
        self.running = False
        self.gamethread = None

    def in_bounds(self, index):
        return 0 <= index <= len(self.cells)-1

    def get_alive_neighbors(self, index):
        neighbor_positions = [index-self.rowsize-1, index-self.rowsize, index-self.rowsize+1,
                              index-1, index+1,
                              index+self.rowsize-1, index+self.rowsize, index+self.rowsize+1]
        n = 0
        for index in neighbor_positions:
            if self.in_bounds(index):
                if self.cells[index].alive:
                    n += 1
        return n

    def tick(self):
        states = []
        for i in range(0, len(self.cells)):
            n = self.get_alive_neighbors(i)
            if not self.cells[i].alive and n == 3:
                states.append(True)
            elif self.cells[i].alive and (n == 2 or n == 3):
                states.append(True)
            else:
                states.append(False)
        for i in range(0, len(self.cells)):
            self.cells[i].alive = states[i]
            self.cells[i].display()
        time.sleep(self.tickperiod)

    def start(self):
        self.gamethread = threading.Thread(target=self.gameloop)
        self.gamethread.start()

    def gameloop(self):
        self.running = True
        while self.running:
            self.tick()

    def stop(self):
        self.running = False


class Cell:
    def __init__(self, parent, x, y):
        self.alive = False
        self.width = 20
        self.height = 20
        self.position = (x, y)
        self.frame = tkinter.Frame(parent, width=self.width, height=self.height, background="grey", borderwidth=1,
                                   relief="solid")
        self.frame.bind("<Button-1>", lambda event: self.onclick())
        self.display()

    def onclick(self):
        self.alive = not self.alive
        self.display()

    def display(self):
        if self.alive:
            self.frame.configure(background="white")
        else:
            self.frame.configure(background="grey")
        self.frame.grid(row=self.position[1], column=self.position[0])


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Game of Life")
    window_width = 640
    window_height = 480
    window.minsize(window_width, window_height)

    grid = tkinter.Frame(window)
    num_rows = 10
    num_cols = 10
    cells = []
    for y in range(num_rows):
        for x in range(num_cols):
            cells.append(Cell(grid, x, y))
    grid.pack()

    game = Game(cells, num_rows, num_cols)

    start = tkinter.Button(window, text="START")
    start.bind("<Button-1>", lambda event: game.start())
    start.pack()

    stop = tkinter.Button(window, text="STOP")
    stop.bind("<Button-1>", lambda event: game.stop())
    stop.pack()

    window.mainloop()
