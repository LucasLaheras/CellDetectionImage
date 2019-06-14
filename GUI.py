from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image, ImageGrab
from CellDetectionImage import CellDetectionImage

# TODO open image
# TODO select in result image and show original image


class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'white'

    def __init__(self):
        self.root = Tk()
        self.i = 1

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0, columnspan=2)

        # self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        # self.brush_button.grid(row=0, column=1, columnspan=2)

        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=0, column=2, columnspan=2)

        # self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        # self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4, columnspan=2)

        img = Image.open('Images/' + str(self.i) + '.jpg').resize((600, 600), Image.ANTIALIAS)
        self.imgOrig = ImageTk.PhotoImage(img)

        # TODO execute cellDetectionImage algorithm on image selected
        img = Image.open('Images/imagem segmentada.png').resize((600, 600), Image.ANTIALIAS)
        # img = CellDetectionImage(img)
        self.imgResult = ImageTk.PhotoImage(img)

        self.label_image = Label(self.root, image=self.imgResult)
        self.label_image.grid(row=1, column=1, columnspan=2)

        self.c = Canvas(self.root, bg='white', width=600, height=600, highlightthickness=0)
        self.c.create_image(0, 0, image=self.imgOrig, anchor=NW)
        self.c.grid(row=1, column=3, columnspan=2)

        # self.last_image = Button(self.root, text='Last image', command=self.last_img)
        # self.last_image.grid(row=2, column=0, columnspan=2)

        self.last_original = Button(self.root, text='Original image', command=self.original_img)
        self.last_original.grid(row=2, column=2, columnspan=2)

        # self.next_image = Button(self.root, text='Next image', command=self.next_img)
        # self.next_image.grid(row=2, column=4, columnspan=2)

        self.zoom_button = Scale(self.root, from_=1, to=100, orient=VERTICAL)
        self.zoom_button.grid(row=1, column=5)

        self.btn_apply = Button(self.root, text='Apply', command=self.apply_modification)
        self.btn_apply.grid(row=3, columnspan=5)

        self.setup()
        self.root.mainloop()

    # TODO change the selection
    def apply_modification(self):
        pass

    # TODO create a new method to save, because this not work
    def save(self):

        file = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics', '*.png')])
        if file:
            x = self.c.winfo_x() + self.root.winfo_rootx()
            y = self.c.winfo_y() + self.root.winfo_rooty()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()

            print(self.root.winfo_rootx(), self.root.winfo_rooty(), self.c.winfo_x(), self.c.winfo_y(), self.c.winfo_width(), self.c.winfo_height(), x, y, x1, y1)

            PIL.ImageGrab.grab().crop(bbox=self.c).save(file + '.png')

    def open_file(self):
        self.root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("Images files", "*.png"), ("Images files", "*.jpg"),
                                                              ("All files", "*.*")))
        img = Image.open(self.root.filename).resize((600, 600), Image.ANTIALIAS)
        self.imgOrig = ImageTk.PhotoImage(img)

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgOrig, anchor=NW)

        # TODO execute cellDetectionImage algorithm on image selected
        img = Image.open('Images/imagem segmentada.png').resize((600, 600), Image.ANTIALIAS)
        self.imgResult = ImageTk.PhotoImage(img)

        self.label_image.configure(image=self.imgResult)

    def original_img(self):
        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgOrig, anchor=NW)

    def last_img(self):
        self.i -= 1

        img = Image.open('Images/' + str(self.i) + '.jpg').resize((600, 600), Image.ANTIALIAS)
        self.imgOrig = ImageTk.PhotoImage(img)

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgOrig, anchor=NW)

        img = Image.open('Images/imagem segmentada.png').resize((600, 600), Image.ANTIALIAS)
        self.imgResult = ImageTk.PhotoImage(img)

        self.label_image.configure(image=self.imgResult)

    # TODO check the last updated image
    def next_img(self):
        self.i += 1

        if (self.i > 10):
            self.end_file()
            return

        img = Image.open('Images/' + str(self.i) + '.jpg').resize((600, 600), Image.ANTIALIAS)
        self.imgOrig = ImageTk.PhotoImage(img)

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgOrig, anchor=NW)

        # TODO execute cellDetectionImage algorithm on image selected
        img = Image.open('Images/imagem segmentada.png').resize((600, 600), Image.ANTIALIAS)
        self.imgResult = ImageTk.PhotoImage(img)

        self.label_image.configure(image=self.imgResult)

    # TODO configure the exit with a pop-up
    def end_file(self):
        self.root.destroy()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    #def use_brush(self):
    #    self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    #def use_eraser(self):
    #    self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
