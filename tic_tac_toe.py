import sys
import os
import ctypes
import subprocess
from tkinter import (
    Tk,
    Frame,
    Widget,
    Label,
    Button,
    messagebox,
    font,
    YES,
    NO,
    TOP,
    BOTTOM,
    LEFT,
    RIGHT,
    BOTH,
    X,
    Y,
)
import pkg_resources
from itertools import cycle


class GuiClass(Frame):
    """gui application for showing local network guests; allows for deauth"""
    def __init__(self, master):
        super().__init__(master)
        
    def run_gui(self):
        """create widgets"""
        self.to_reset = False
        self.chars_cycle = cycle(['X', 'O'])
        self.font = font.Font(family="Lucida console", size=32, weight="normal")
        self.original_color = self.master.cget("background")
        
        # *********** init gui ***********
        # self.hide_console()
        self.master.minsize(300, 300)  # width, height (minimal values for window)
        self.master.geometry("{}x{}".format(300, 300))
        self.master.resizable(width=False, height=False)
        self.master.wm_title("tic-tac-toe")
        self.pack()
        
        # *********** widgets ***********
        self.buttons_ids = {}
        counter = 0
        for x in range(3):
            row = Frame(self.master)
            row.pack(expand=YES, fill=BOTH, side=TOP)
            for y in range(3):
                counter += 1
                button = Button(row, font=self.font, text=" ", command=lambda q=counter: self.click_button(q), justify="center")
                button.pack(expand=YES, fill=BOTH, side=LEFT)
                self.buttons_ids[counter] = button
                
        # *********** lift, get focus ***********
        self.master.update()
        self.master.attributes("-topmost", False)
        self.master.lift()  # move window to the top
        self.master.focus_force()
        return None
        
    def reset_board(self):
        """reset board for next play"""
        for x in range(1, 10):
            self.buttons_ids[x].config(bg=self.original_color)
            self.buttons_ids[x].config(text=' ')
        self.chars_cycle = cycle(['X', 'O'])
        self.to_reset = False
        return None
        
    def check_winner(self):
        """check who wins"""
        possible_wins = [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7),
            ]
        for row in possible_wins:
            row_items = [self.buttons_ids[val]['text'] for val in row]
            row_items = [item for item in row_items if item.strip()]
            if len(row_items) == 3 and len(list(set(row_items))) == 1:
                print('[+] winner: {}'.format(row_items[0]))
                # ******** change sqaures background ********
                for square_id in row:
                    self.buttons_ids[square_id].config(bg='green')
                return True
        return False
        
    def click_button(self, number):
        '''click button'''
        # ******** check if table is full ********
        table_items = []
        for x in range(1, 10):
            text = self.buttons_ids[x]['text']
            if text.strip():
                table_items.append(text)
        if len(table_items) == 9:
            print('[:] table is full - draw')
            self.to_reset = True
            
        # ******** perform board reset if needed ********
        if self.to_reset:
            self.reset_board()
            return None
            
        # ******** check if button was clicked before ********
        text = self.buttons_ids[number]['text']
        if text.strip():
            print('[-] already clicked!')
            return False
            
        # ******** perform click ********
        # print('[*] clicked: {}'.format(number))
        char = next(self.chars_cycle)
        self.buttons_ids[number].config(text=char)
        
        # ******** check win status ********
        win_status = self.check_winner()
        if win_status:
            self.to_reset = True
            
        return None
        
    @staticmethod
    def hide_console():
        """hide console window"""
        if os.name == "nt":
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0
            )
        return None
        
        
if __name__ == "__main__":
    gui = GuiClass(master=Tk())
    gui.run_gui()
    
