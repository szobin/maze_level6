import tkinter as tk
import sched as sd
import time as tm

from . import MAZE_LEVEL
from .conf import W_CANVAS, H_CANVAS, TIME_INTERVAL
from .board import Board
from .player import Player
from .mob import Mob
from solutions import guides


class App:

    def __init__(self, player_control_no=1, mob_control_no=1):
        self.window = tk.Tk()
        self.window.wm_title(f"Maze - level {MAZE_LEVEL} - variant {player_control_no}")
        self.scheduler = sd.scheduler(tm.time, tm.sleep)

        self.canvas = tk.Canvas(self.window, width=W_CANVAS, height=H_CANVAS, bg="gray")
        self.canvas.pack()
        self.set_window(W_CANVAS, H_CANVAS)

        self.stop = False
        self.restart_var = tk.IntVar()  # tk.IntVAR внутренняя переменная библиотеки tkinter

        self.board = Board(self.canvas, self.check_cell)
        self.player = Player(self.canvas, self.board, guides[player_control_no-1])
        self.mob = Mob(self.canvas, self.board, guides[mob_control_no - 1])

    def check_cell(self, sender, pos):
        if sender == self.player:
            if pos == self.mob.position:
                return False
        if sender == self.mob:
            if pos == self.player.position:
                return False
        return self.board.check(None, pos)

    def set_window(self, w, h):
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width // 2) - (w // 2)
        y = 6
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_close(self):
        self.stop = True
        self.restart_var.set(1)
        self.window.quit()

    def on_timer(self):
        if not self.player.move():
            self.game_over()
            self.reset_game()

        if self.stop:
            return

        self.mob.move()

        self.window.update()
        self.scheduler.enter(TIME_INTERVAL, 1, self.on_timer)

    def game_over(self):
        self.board.draw_game_over_panel(f"Score: {self.player.score}, steps: {self.player.step_count}")
        restart_button = tk.Button(self.window, text="RESTART", fg="white", bg="lawn green", font=("Tahoma", 24),
                                   width=12, height=1,
                                   command=lambda: self.restart_var.set(1))
        restart_button.place(anchor=tk.CENTER, relx=0.5, rely=0.62)
        restart_button.wait_variable(self.restart_var)
        restart_button.destroy()

    def reset_game(self):
        if self.stop:
            return
        self.board.reset()
        self.mob.respawn()
        self.player.respawn()

    def run(self):
        self.stop = False
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.board.draw()
        self.mob.draw()
        self.player.draw()
        # self.window.mainloop()
        self.scheduler.enter(TIME_INTERVAL, 1, self.on_timer)
        self.scheduler.run()
