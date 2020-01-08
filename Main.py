import tkinter as tk
import tkinter.filedialog
import os
import datetime
from pathlib import Path
from PIL import Image, ImageTk


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

        # init logic modules
        self.photosort = PhotoSort()

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
        #print('Resize: ' + str(self.width) + 'x' + str(self.height))
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
        image = Image.open(Path.joinpath(path_images, "girl_with_camera.png"))
        self.current_image = ImageTk.PhotoImage(image.resize((300, 200), Image.ANTIALIAS))
        self.photoframe = tk.Label(self.c_photo, image=self.current_image)
        self.photoframe.image = self.current_image
        self.photoframe.pack(fill='both', expand=1)

        self.c_quickfuns = tk.Frame(self)
        self.c_quickfuns.grid(row=3, column=0)

        # work path
        self.c_workpath = tk.Frame(self)
        self.c_workpath.grid(row=0, column=1, sticky='nwe', pady=self.pad, padx=self.pad)
        self.workpath_label = tk.Label(self.c_workpath, text=self.root.photosort.workfolder, relief='sunken')
        self.workpath_button = tk.Button(self.c_workpath, text='change')
        self.workpath_label.pack(side='left', expand=True)
        self.workpath_button.pack(side='right')
        self.workpath_button.bind('<Button-1>', lambda e: self.button_workpath())

        # meta data
        self.c_metadata = tk.Frame(self)
        self.c_metadata.grid(row=1, column=1)

        self.c_tags = tk.Frame(self)
        self.c_tags.grid(row=2, column=1)

        self.c_newtag = tk.Frame(self)
        self.c_newtag.grid(row=3, column=1)

    def button_workpath(self):
        self.root.photosort.set_workfolder(tk.filedialog.askdirectory())
        self.workpath_label.configure(text=self.root.photosort.get_workfolder())

    def get_resized_image(self, image, widget):
        x_i, y_i = image.size
        x_w, y_w = widget.winfo_width(), widget.winfo_height()
        ratio_i = x_i/y_i
        ratio_w = x_w/y_w
        if(ratio_i >= r):


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


# ===== Logic Modules =====
class PhotoSort:
    def __init__(self):
        self.workfolder = Path("empty")
        self.validfiles = validfototypes
        self.photos = []

    def set_workfolder(self, wf):
        self.workfolder = Path(wf)
        print("PhotoSort: workfolder changed to " + wf)
        self.scan_folder()

    def get_workfolder(self):
        return str(self.workfolder)

    def scan_folder(self):
        files = os.listdir(self.workfolder)
        photolist = []
        for img_name in files:
            if os.path.splitext(img_name)[1] in self.validfiles:
                photolist.append(Photo(img_name))
            else:
                files.remove(img_name)
        self.photos = photolist
        self.print_photo_overview(0)

    def print_photo_overview(self, n):
        print("name: " + str(self.photos[n].oldname))
        print("path: " + str(self.photos[n].path))
        print("date: " + str(self.photos[n].date))
        print("tags: " + str(self.photos[n].tags))
        print("reso: " + str(self.photos[n].reso))


class Photo:
    def __init__(self, img):
        self.oldname = img
        self.path = Path.joinpath(app.photosort.workfolder, self.oldname)
        self.date = datetime.datetime.fromtimestamp(self.path.stat().st_mtime)
        self.tags = []
        im = Image.open(self.path)
        self.x, self.y = im.size
        self.reso = '{}x{}'.format(self.x, self.y)


# ===== Global Vars =====
colourdict = {0: '#FFFFFF', 1: '#354668', 2: '#27334A', 3: '#1C2536', 4: '#121926', 5: '#0B0F17'}
validfototypes = ['.jpg', '.JPG', '.png', '.PNG']
path_images = Path(r"C:\Users\tomod\OneDrive\06 Programmierung\01 Python\01 Projekte\TomSort\images")

# ===== Program =====
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