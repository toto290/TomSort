import tkinter as tk
import os
from pathlib import Path


class MainApplication(tk.Frame):
    def __init__(self, parent, title):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mode = 0        # start:0 sort:1 twin:2
        self.parent.state('zoomed')
        self.parent.title(title)

        self.menu = Menu(self.parent, self)
        self.status = Status(self.parent)

        self.modelabtxt = tk.StringVar()
        self.modelabtxt = str(self.mode)
        self.modelab = tk.Label(self.parent, text=self.modelabtxt)
        self.modelab.pack()

        self.updateGUI()


    def updateGUI(self):
        self.update_idletasks()
        self.update()
        print(self.mode)
        #self.parent.after(1000, self.updateGUI)


    def draw_mode_sort(self):
        left_frame = tk.Frame(root, bg='blue', height=600, width=600)
        left_frame.pack(side='left', expand='0')
        right_frame = tk.Frame(root, bg='red', height=600, width=600)
        right_frame.pack(side='right', expand='0')

    # def draw_mode_twin(self):


class Menu(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.app = app
        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.submenu_start = tk.Menu(self.menu)
        self.menu.add_cascade(label='Start', menu=self.submenu_start)

        self.submenu_modes = tk.Menu(self.menu)
        self.menu.add_cascade(label='Modes', menu=self.submenu_modes)
        self.submenu_modes.add_command(label='Sort Photos', command=self.activate_mode_sort)
        self.submenu_modes.add_command(label='Find Twins', command=self.activate_mode_twin)

    def activate_mode_sort(self):
        self.app.mode = 1
        self.app.updateGUI()
        print('Mode changed to: Sorting')
        
    def activate_mode_twin(self):
        self.app.mode = 2
        self.app.updateGUI()
        print('Mode changed to: TwinFinding')


class Status(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.status = tk.Label(self.parent, text='idle', bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')


'''
        self.screenX = self.root.winfo_screenmmwidth()
        self.screenY = self.root.winfo_screenheight()
'''

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root, 'TomSort').pack(side="top", fill="both", expand=True)
    root.mainloop()

'''
workfolder = Path("C:/Users/tomod/Desktop/FotoSortTest")

filesInFolder = os.listdir(workfolder)
print(len(filesInFolder))
f = open(workfolder / Path(filesInFolder[2]))
print(f)
'''