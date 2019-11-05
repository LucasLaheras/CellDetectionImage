from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw
import cv2
import numpy as np
from CellDetectionImage import CellDetectionImage
import os
import tkinter as tk
from tkinter import ttk
from circular_queue import CircularQueue
import random

nomeArquivoPadraoOuro = 'PO.png'
guiX = 650
guiY = 650
number_last_images = 10
cont_images = 0


class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')


class GUI(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'white'

    def __init__(self):
        self.root = Tk()
        self.root.filename = "C:\\Users\\lucas\\PycharmProjects\\CellDetectionImage\\Images"

        self.timeline = CircularQueue()

        vbar = AutoScrollbar(self.root, orient='vertical')
        hbar = AutoScrollbar(self.root, orient='horizontal')
        vbar.grid(row=2, column=6, sticky='ns')
        hbar.grid(row=3, column=3, columnspan=2, sticky='we')

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="Abrir", command=self.open_file)
        self.filemenu.add_command(label="Salvar", command=self.save)
        self.filemenu.add_command(label="Resetar", command=self.resetImage)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Sair", command=self.root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=self.filemenu)

        # pen button
        self.pen_button = Button(self.root, text='Pen', command=self.use_pen, relief=SUNKEN)
        self.pen_button.grid(row=1, column=0)

        # self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        # self.brush_button.grid(row=0, column=1, columnspan=2)

        # self.color_button = Button(self.root, text='Color', command=self.choose_color)
        # self.color_button.grid(row=0, column=2, columnspan=2)

        # eraser button
        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=1, column=1)

        # slider size pen and eraser
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=3)

        # move button
        self.btn_move = Button(self.root, text='Move', command=self.use_move)
        self.btn_move.grid(row=1, column=4)

        # open first image to iterate
        #imageCV = Image.open('Images/result-cell-1.png').resize((guiX, guiY), Image.ANTIALIAS)
        self.imageCV = cv2.imread('Images/first image.png')
        self.lin, self.col, _ = self.imageCV.shape
        #self.imageCV = CellDetectionImage(self.imageCV)

        # modified image in interface
        self.imageCV600cell = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(self.imageCV600cell))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        self.label_image = Label(self.root, image=self.goldImage)
        self.label_image.grid(row=2, column=0, columnspan=3)
        self.label_image.bind("<Button>", self.select_area)

        self.imgright = np.copy(self.imageCV)
        self.imgOriginalCV = self.imgright.copy()

        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.image1.getcolors()
        self.draw = ImageDraw.Draw(self.image1)

        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.90

        self.c = Canvas(self.root, bg='white', width=guiX, height=guiY, highlightthickness=0,
                        xscrollcommand=hbar.set, yscrollcommand=vbar.set, cursor="pencil")
        self.c.grid(row=2, column=3, columnspan=2, sticky='nswe')
        self.text = self.c.create_text(0, 0, anchor='nw')
        self.show_image()
        #self.imgLeft = ImageTk.PhotoImage(Image.open('Images/first image.png').resize((guiX, guiY), Image.ANTIALIAS))

        #self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

        vbar.configure(command=self.c.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.c.xview)
        # Make the canvas expandable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.c.bind('<ButtonPress-1>', self.move_from)
        self.c.bind('<B1-Motion>', self.move_to)
        self.c.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.c.bind('<Button-5>', self.wheel)  # only with Linux, wheel scroll down
        self.c.bind('<Button-4>', self.wheel)  # only with Linux, wheel scroll up

        self.c.configure(scrollregion=self.c.bbox('all'))

        # self.last_image = Button(self.root, text='Last image', command=self.last_img)
        # self.last_image.grid(row=2, column=0, columnspan=2)

        self.last_original = Button(self.root, text='Original image', command=self.original_img)
        self.last_original.grid(row=4, column=0, columnspan=3)

        # slider size of area
        self.choose_area = Scale(self.root, from_=0, to=80, orient=HORIZONTAL, command=self.remove_area, length=300)
        self.choose_area.grid(row=3, column=0)


        # self.next_image = Button(self.root, text='Next image', command=self.next_img)
        # self.next_image.grid(row=2, column=4, columnspan=2)

        self.btn_apply = Button(self.root, text='Apply', command=self.apply_modification)
        self.btn_apply.grid(row=4, column=3, columnspan=3)

        self.btn_undo = Button(self.root, text='UNDO', command=self.undo)
        self.btn_undo.grid(row=0, column=0)

        self.btn_redo = Button(self.root, text='REDO', command=self.redo)
        self.btn_redo.grid(row=0, column=1)

        self.label_image1 = np.zeros([guiX, guiY], dtype=np.uint8)

        self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        self.imageInMermory[self.imageInMermory > 0] = 255

        self.open_file()
        self.move_on = False

        self.setup()
        self.translatePortuguese()
        self.root.mainloop()

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        self.c.delete(ALL)
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)
        self.c.scale('all', x, y, scale, scale)
        self.show_image()
        self.c.configure(scrollregion=self.c.bbox('all'))

    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.c.delete(self.imageid)
            self.imageid = None
            self.c.imagetk = None  # delete previous image from the canvas
        width, height, _ = self.imageCV.shape
        new_size = int(self.imscale * width), int(self.imscale * height)
        if new_size[0] < guiX or new_size[1] < guiY:
            self.imscale /= self.delta
            new_size = (guiX, guiY)

        im1 = cv2.cvtColor(self.imgOriginalCV, cv2.COLOR_BGR2RGB)
        im2 = cv2.cvtColor(np.array(self.image1), cv2.COLOR_BGR2RGB)
        self.imgright = cv2.add(im1, im2)
        self.imgright = cv2.resize(self.imgright, new_size)

        imagetk = ImageTk.PhotoImage(Image.fromarray(self.imgright))

        # Use self.text object to set proper coordinates
        self.imageid = self.c.create_image(0, 0, anchor='nw', image=imagetk)
        self.c.lower(self.imageid)  # set it into background
        self.c.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

        #self.goldImage = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, new_size)))
        #self.label_image.configure(image=self.goldImage)

    def apply_modification(self):
        image_saved = self.image1.copy()
        image_saved1 = cv2.cvtColor(np.array(image_saved), cv2.COLOR_BGR2GRAY)

        self.mostra(image_saved1)
        self.mostra(self.imageInMermory)

        # image_saved1

        self.last_modifications = [None] * number_last_images

        ret, thresh = cv2.threshold(image_saved1, 128, 255, 0)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        try:
            for i in range(len(contours)):
                cv2.drawContours(image_saved1, contours, i, 255, -1)
        except:
            messagebox.showerror("Error", "Fechar a area delimitada!")

        # transformar goldImage em imageInMermory + image_saved1

        imgteste = cv2.add(self.imageInMermory, image_saved1)
        self.mostra(imgteste)


        self.imageCV = self.individualregioncolor(imgteste)
        self.mostra(self.imageCV)
        self.imageInMermory = imgteste

        #img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        #self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        #self.label_image.configure(image=self.goldImage)
        self.remove_area(None)

        self.c.delete(ALL)
        #imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        #self.imgLeft = ImageTk.PhotoImage(imageCV600)
        #self.c.create_image(0, 0, image=self.imgLeft, anchor='nw')

        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        self.show_image()
        self.timeline.enqueue(self.image1.copy())

    def translatePortuguese(self):
        self.pen_button.config(text="Caneta")
        self.eraser_button.config(text="Borracha")
        self.btn_apply.config(text="Aplicar")
        self.last_original.config(text="Imagem Original")
        self.btn_redo.config(text="Refazer")
        self.btn_undo.config(text="Desfazer")
        self.btn_move.config(text="Mover")

    def save(self):
        existeOuro = str(self.root.filename)

        for i in range(len(existeOuro) - 1, 0, -1):
            if existeOuro[i] == '.':
                existeOuro = existeOuro[:i]
                break

        existeOuro += nomeArquivoPadraoOuro

        cv2.imwrite(existeOuro, self.remove_area(None))
        messagebox.showinfo("Concluido", "Imagem salva com sucesso")

    # abre a imagem
    def open_file(self):
        self.root.filename = filedialog.askopenfilename(initialdir=str(self.root.filename), title="Select file",
                                                   filetypes=(("Images files", "*.png"), ("Images files", "*.jpg"),
                                                              ("All files", "*.*")))
        self.c.delete(ALL)
        self.timeline.clear_all()
        self.choose_area.set(0)

        self.imgOriginalCV = cv2.imread(self.root.filename)
        self.imgright = self.imgOriginalCV.copy
        self.lin, self.col, _ = self.imgOriginalCV.shape

        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        #imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        #self.imgLeft = ImageTk.PhotoImage(imageCV600)
        self.show_image()

        self.last_modifications = [None] * number_last_images

        #self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

        existeOuro = str(self.root.filename)

        for i in range(len(existeOuro)-1, 0, -1):
            if existeOuro[i] == '.':
                existeOuro = existeOuro[:i]
                break

        existeOuro += nomeArquivoPadraoOuro

        messagebox.showinfo("Espere", "Clique em OK e espere o algoritmo de processamento terminar de executar")

        if os.path.exists(existeOuro):
            self.imageCV = cv2.imread(existeOuro)

        else:
            #imageCV = Image.open('Images/load.gif').resize((guiX, guiY), Image.ANTIALIAS)
            self.imageCV = CellDetectionImage(self.imgOriginalCV)

        #img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        #self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        #self.label_image.configure(image=self.goldImage)

        self.remove_area(None)

        self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        self.imageInMermory[self.imageInMermory > 0] = 255

        self.timeline.enqueue(self.image1.copy())

    # cria a area na imagem da direita para ser editada
    def select_area(self, event):
        img = self.imageCV.copy()

        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        try:
            _, _ = img.shape
            im2 = img
        except:
            im2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        x = event.x
        y = event.y
        y2, x2 = im2.shape
        areay = int((y2 * y) / (guiY * 1.0))
        areax = int((x2 * x) / (guiX * 1.0))

        if im2[areay][areax] < 10:
            self.c.delete(ALL)
            self.imgright = self.imgOriginalCV.copy()

            self.imgright = cv2.cvtColor(self.imgright, cv2.COLOR_BGR2RGB)

            #self.imgLeft = ImageTk.PhotoImage(Image.fromarray(self.imgright).resize((guiX, guiY), Image.ANTIALIAS))
            #self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

            self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
            self.imageInMermory[self.imageInMermory > 0] = 255

            self.show_image()
            print("nao tem nada")

            return

        im2 = cv2.threshold(im2, 10, 255, cv2.THRESH_BINARY)[1]  # ensure binary
        ret, labels = cv2.connectedComponents(im2)

        area = labels[areay, areax]

        labels[labels != area] = 0
        labels[labels == area] = 1

        # Colore cada área
        # Map component labels to hue val
        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        # set bg label to black
        labeled_img[label_hue == 0] = 0

        # Transforma em escala de cinza
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2GRAY)

        # get the contour
        ret, thresh = cv2.threshold(labeled_img, 10, 255, 0)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # separates only the region of interest
        lin, col = im2.shape
        im3 = np.zeros([lin, col], dtype=np.uint8)

        cv2.drawContours(im3, contours, -1, 255, -1)

        self.imageInMermory = im2 - im3

        im3 = np.zeros([lin, col], dtype=np.uint8)

        cv2.drawContours(im3, contours, -1, 255)

        self.image1 = Image.fromarray(cv2.cvtColor(im3, cv2.COLOR_GRAY2BGR))

        self.draw = ImageDraw.Draw(self.image1)

        self.show_image()

        self.timeline.enqueue(self.image1.copy())

    def mostra(self, img, name='Name'):
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def original_img(self):
        self.c.delete(ALL)
        #imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        #self.imgLeft = ImageTk.PhotoImage(imageCV600)
        #self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)
        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        self.timeline.enqueue(self.image1.copy())

        self.show_image()

        self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        self.imageInMermory[self.imageInMermory > 0] = 255

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.c.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.c.scan_dragto(event.x, event.y, gain=1)

    def use_move(self):
        self.c.config(cursor="fleur")
        self.move_on = True
        self.activate_button(self.btn_move)

    def use_pen(self):
        self.c.config(cursor="pencil")
        self.choose_size_button.set(1)
        self.move_on = False
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.move_on = False
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.c.config(cursor="dotbox")
        self.choose_size_button.set(5)
        self.move_on = False
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        if self.move_on:
            self.move_to(event)
            return
        paint_color = 'black' if self.eraser_on else 'white'

        # convert from window coordinates to canvas coordinates
        x = self.c.canvasx(event.x)
        y = self.c.canvasy(event.y)

        colRight, linRight, _ = self.imgright.shape

        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, x, y, width=self.line_width*(linRight/self.lin), fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            #print((self.old_x, self.old_y))
            #print((event.x, event.y))
            self.draw.line((self.lin*self.old_x/linRight, self.col*self.old_y/colRight, self.lin*x/linRight, self.col*y//colRight), fill=paint_color, width=self.line_width)
        self.old_x = x
        self.old_y = y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.c.delete(ALL)
        self.last_modifications[cont_images] = self.image1.copy()
        self.show_image()
        self.timeline.enqueue(self.image1.copy())

    def undo(self):
        self.image1 = self.timeline.last().copy()
        self.draw = ImageDraw.Draw(self.image1)

        self.c.delete(ALL)
        self.show_image()

    def redo(self):
        self.image1 = self.timeline.next().copy()
        self.draw = ImageDraw.Draw(self.image1)

        self.c.delete(ALL)
        self.show_image()

    def resetImage(self):
        self.c.delete(ALL)
        self.timeline.clear_all()

        self.last_modifications = [None] * number_last_images

        #imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        #self.imgLeft = ImageTk.PhotoImage(imageCV600)
        #self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

        self.image1 = Image.new("RGB", (self.col, self.lin), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        self.show_image()

        messagebox.showinfo("Espere", "Clique em OK e espere o algoritmo de processamento terminar de executar")

        self.imageCV = CellDetectionImage(self.imgOriginalCV)

        self.lin, self.col, _ = self.imageCV.shape
        #img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        #self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        #self.label_image.configure(image=self.goldImage)

        self.remove_area(None)

        self.timeline.enqueue(self.image1.copy())

    def individualregioncolor(self, im1):
        try:
            _, _ = im1.shape
            im2 = im1
        except:
            im2 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

            # identifies each area separately
        ret, thresh = cv2.threshold(im2, 127, 255, 0)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # creates an array of the same size
        lin, col = im2.shape
        im3 = np.zeros([lin, col], dtype=np.uint8)
        im3 = cv2.cvtColor(im3, cv2.COLOR_GRAY2RGB)

        # color each area with a randomly generated RGB color
        for i in range(1, len(contours)):
            cv2.drawContours(im3, contours, i,
                             ((random.randint(100, 255)), random.randint(20, 255), random.randint(20, 255)), -1)

        return im3

    def remove_area(self, event):
        im1 = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(im1, 1, 255, 0)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # separates only the region of interest
        lin, col = im1.shape
        im3 = np.zeros([lin, col], dtype=np.uint8)

        small = self.choose_area.get()

        for i in range(1, len(contours)):
            if small <= len(contours[i]):
                im3 = cv2.drawContours(im3, contours, i, 255, -1)

        im3 = self.individualregioncolor(im3)

        img1 = cv2.resize(im3, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        self.label_image.configure(image=self.goldImage)

        return im3

if __name__ == '__main__':
    GUI()
