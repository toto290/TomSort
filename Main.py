import tkinter as tk
import os
from pathlib import Path


class MainApplication(tk.Tk):
    def __init__(self, title):
        tk.Tk.__init__(self)

        # initial parameters
        self.mode = tk.IntVar()
        self.mode.set(0)    # start:0 sort:1 twin:2
        self.width = 500
        self.height = 500
        self.geometry('{}x{}'.format(str(self.width), str(self.height)))
        self.title(title)
        self.update_idletasks()

        # GUI creation
        self.menu = Menu(self)
        self.status = Status(self)
        self.frame_start = FrameModeStart(self, width=self.width, height=self.height)
        self.frame_sort = FrameModeSort(self, width=self.width, height=self.height)
        self.frame_twin = FrameModeTwin(self, width=self.width, height=self.height)
        self.mode_dict = {0: ('Start', self.frame_start), 1: ('Sort', self.frame_sort), 2: ('Twin', self.frame_twin)}

        # GUI initialization
        self.currentframe = self.mode_dict[0][1]
        self.status.statustext.set(self.mode_dict[0][0] + '-Mode')
        self.currentframe.pack()
        self.update_idletasks()

        # Binds
        self.bind("<Configure>", lambda e: self.resize())

    def switch_mode(self, num):
        print('Switch mode: ' + self.mode_dict[num][0] + '(' + str(num) + ')')
        self.mode.set(num)
        self.status.statustext.set(self.mode_dict[num][0] + '-Mode')
        self.currentframe.pack_forget()
        self.mode_dict[num][1].pack(side="bottom", fill="both", expand=True)
        self.update_idletasks()
        self.currentframe = self.mode_dict[num][1]

    def resize(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        print('Resize: ' + str(self.width) + 'x' + str(self.height))
        self.currentframe.config(width=self.width, height=self.height)
        self.update_idletasks()


class FrameModeStart(tk.Frame):
    def __init__(self, root, **kwargs):
        print('init: Start-Mode Frame')
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root


class FrameModeSort(tk.Frame):
    def __init__(self, root, **kwargs):
        print('init: Sort-Mode Frame')
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root
        self.left_frame = tk.Frame(self, bg='blue', height=int(1 * self.root.height), width=int(0.7 * self.root.width))
        self.right_frame = tk.Frame(self, bg='red', height=int(1 * self.root.height), width=int(0.3 * self.root.width))
        self.left_frame.pack(side='left', expand='1')
        self.right_frame.pack(side='right', expand='1')


class FrameModeTwin(tk.Frame):
    def __init__(self, parent, width, height):
        print('init: Twin-Mode Frame')
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.root = parent
        left_frame = tk.Frame(self, bg='green', height=600, width=600)
        right_frame = tk.Frame(self, bg='yellow', height=600, width=600)


class Menu(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=False)
        self.root.config(menu=self.menu)

        self.submenu_start = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Start', menu=self.submenu_start)

        self.submenu_modes = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.submenu_modes)
        self.submenu_modes.add_command(label='Sort Photos', command=lambda: self.root.switch_mode(1))
        self.submenu_modes.add_command(label='Find Twins', command=lambda: self.root.switch_mode(2))


class Status(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.statustext = tk.StringVar()
        self.statustext.set('idle')
        self.status = tk.Label(self.root, textvariable=self.statustext, bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')


if __name__ == '__main__':
    app = MainApplication('TomSort')
    app.mainloop()

'''
workfolder = Path("C:/Users/tomod/Desktop/FotoSortTest")

filesInFolder = os.listdir(workfolder)
print(len(filesInFolder))
f = open(workfolder / Path(filesInFolder[2]))
print(f)
'''