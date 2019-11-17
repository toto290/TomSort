import tkinter as tk
import os
from pathlib import Path


class MainApplication(tk.Tk):
    def __init__(self, title):
        tk.Tk.__init__(self)

        # initial parameters
        self.mode = tk.IntVar()
        self.mode.set(0)    # start:0 sort:1 twin:2
        self.state('zoomed')
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.geometry('{}x{}'.format(str(self.width), str(self.height)))
        self.title(title)
        self.update_idletasks()

        # GUI creation
        self.menu = Menu(self)
        self.status = Status(self)
        self.frame_start = FrameModeStart(self, width=self.width, height=self.height, bg=colourdict[3])
        self.frame_sort = FrameModeSort(self, width=self.width, height=self.height, bg=colourdict[3])
        self.frame_twin = FrameModeTwin(self, width=self.width, height=self.height, bg=colourdict[3])
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
        tk.Frame.__init__(self, root, **kwargs)
        print('init: Start-Mode Frame')
        self.root = root


class FrameModeSort(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        print('init: Sort-Mode Frame')
        self.root = root
        self.pad = 20
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=500)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, minsize=60)

        self.c_photo = tk.Frame(self)
        self.c_photo.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.c_photo.configure(bg='white', bd=5, relief='groove')
        self.photoframe = tk.Label(self.c_photo, text="hier könnte ihr foto stehen")
        self.photoframe.pack(fill='both', expand=True)

        self.c_quickfuns = tk.Frame(self)
        self.c_quickfuns.grid(row=3, column=0)

        # workpath
        self.c_workpath = tk.Frame(self)
        self.c_workpath.grid(row=0, column=1, sticky='nwe', pady=self.pad, padx=self.pad)
        self.workpath_label = tk.Label(self.c_workpath, text='//dies/ist/ein/Beispielpfad', relief='sunken')
        self.workpath_button = tk.Button(self.c_workpath, text='change work folder')
        self.workpath_label.pack(side='left', expand=True)
        self.workpath_button.pack(side='right')

        self.c_metadata = tk.Frame(self)
        self.c_metadata.grid(row=1, column=1)

        self.c_tags = tk.Frame(self)
        self.c_tags.grid(row=2, column=1)

        self.c_newtag = tk.Frame(self)
        self.c_newtag.grid(row=3, column=1)


class FrameModeTwin(tk.Frame):
    def __init__(self, root, **kwargs):
        print('init: Twin-Mode Frame')
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root


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


# Program
colourdict = {0: '#FFFFFF', 1: '#354668', 2: '#27334A', 3: '#1C2536', 4: '#121926', 5: '#0B0F17'}
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