from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import messagebox
import PIL
from PIL import ImageTk, Image, ImageDraw
import cv2
import numpy as np
from CellDetectionImage import CellDetectionImage
import os

nomeArquivoPadraoOuro = 'PO.png'
guiX = 900
guiY = 900

# TODO open image
# TODO select in result image and show original image

class GUI(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'white'

    def __init__(self):
        self.root = Tk()
        self.root.filename = "C:\\Users\\lucas\\PycharmProjects\\CellDetectionImage\\Images"

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
        self.pen_button = Button(self.root, text='Pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0, columnspan=2)

        # self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        # self.brush_button.grid(row=0, column=1, columnspan=2)

        # self.color_button = Button(self.root, text='Color', command=self.choose_color)
        # self.color_button.grid(row=0, column=2, columnspan=2)

        # eraser button
        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4, columnspan=2)

        # open first image to iterate
        #imageCV = Image.open('Images/result-cell-1.png').resize((guiX, guiY), Image.ANTIALIAS)
        self.imageCV = cv2.imread('Images/first image.png')
        #self.imageCV = CellDetectionImage(self.imageCV)

        # modified image in interface
        imageCV600cell = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(imageCV600cell))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        self.label_image = Label(self.root, image=self.goldImage)
        self.label_image.grid(row=1, column=1, columnspan=2)
        self.label_image.bind("<Button>", self.select_area)

        self.imgright = np.copy(self.imageCV)
        self.lin, self.col, _ = self.imgright.shape
        self.imgOriginalCV = self.imgright.copy()
        imageCV600 = Image.open('Images/first image.png').resize((guiX, guiY), Image.ANTIALIAS)
        self.imgLeft = ImageTk.PhotoImage(imageCV600)

        self.c = Canvas(self.root, bg='white', width=guiX, height=guiY, highlightthickness=0)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)
        self.c.grid(row=1, column=3, columnspan=2)

        self.image1 = Image.new("RGB", (guiX, guiY), (0, 0, 0))
        self.image1.getcolors()
        self.draw = ImageDraw.Draw(self.image1)

        # self.last_image = Button(self.root, text='Last image', command=self.last_img)
        # self.last_image.grid(row=2, column=0, columnspan=2)

        self.last_original = Button(self.root, text='Original image', command=self.original_img)
        self.last_original.grid(row=2, column=0, columnspan=3)

        # self.next_image = Button(self.root, text='Next image', command=self.next_img)
        # self.next_image.grid(row=2, column=4, columnspan=2)

        #TODO ZOOM slider
        # self.zoom_button = Scale(self.root, from_=1, to=100, orient=VERTICAL)
        # self.zoom_button.grid(row=1, column=5)

        self.btn_apply = Button(self.root, text='Apply', command=self.apply_modification)
        self.btn_apply.grid(row=2, column=3, columnspan=3)

        self.label_image1 = np.zeros([guiX, guiY], dtype=np.uint8)

        self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        self.imageInMermory[self.imageInMermory>0] = 255

        self.open_file()

        self.setup()
        self.translatePortuguese()
        self.root.mainloop()

    # TODO change the selection
    def apply_modification(self):
        image_saved = self.image1.copy().resize((self.lin, self.col), PIL.Image.ANTIALIAS)
        image_saved1 = cv2.cvtColor(np.array(image_saved), cv2.COLOR_BGR2GRAY)

        # image_saved1

        ret, thresh = cv2.threshold(image_saved1, 128, 255, 0)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        try:
            for i in range(len(contours)):
                cv2.drawContours(image_saved1, contours, i, 255, -1)
        except:
            messagebox.showerror("Error", "Fechar a area delimitada!")

        # transformar goldImage em imageInMermory + image_saved1

        imgteste = cv2.add(self.imageInMermory, image_saved1)

        self.imageCV = self.individualregioncolor(imgteste)
        self.imageInMermory = imgteste

        img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        self.label_image.configure(image=self.goldImage)

        self.c.delete(ALL)
        imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        self.imgLeft = ImageTk.PhotoImage(imageCV600)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

        self.image1 = Image.new("RGB", (guiX, guiY), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

    def translatePortuguese(self):
        self.pen_button.config(text="Caneta")
        self.eraser_button.config(text="Borracha")
        self.btn_apply.config(text="Aplicar")
        self.last_original.config(text="Imagem Original")

    def save(self):
        existeOuro = str(self.root.filename)

        for i in range(len(existeOuro) - 1, 0, -1):
            if existeOuro[i] == '.':
                existeOuro = existeOuro[:i]
                break

        existeOuro += nomeArquivoPadraoOuro

        cv2.imwrite(existeOuro, self.imageCV)

    # abre a imagem
    def open_file(self):
        self.image1 = Image.new("RGB", (guiX, guiY), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image1)

        self.root.filename = filedialog.askopenfilename(initialdir=str(self.root.filename), title="Select file",
                                                   filetypes=(("Images files", "*.png"), ("Images files", "*.jpg"),
                                                              ("All files", "*.*")))
        self.imgOriginalCV = cv2.imread(self.root.filename)
        imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        self.imgLeft = ImageTk.PhotoImage(imageCV600)

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

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

        self.lin, self.col, _ = self.imageCV.shape
        img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        self.label_image.configure(image=self.goldImage)

        self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
        self.imageInMermory[self.imageInMermory > 0] = 255

    # cria a area na imagem da direita para ser editada
    def select_area(self, event):
        img = self.imageCV.copy()

        self.image1 = Image.new("RGB", (guiX, guiY), (0, 0, 0))
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
            self.imgright = self.imgOriginalCV.copy()

            self.imgright = cv2.cvtColor(self.imgright, cv2.COLOR_BGR2RGB)

            self.imgLeft = ImageTk.PhotoImage(Image.fromarray(self.imgright).resize((guiX, guiY), Image.ANTIALIAS))

            self.imageInMermory = cv2.cvtColor(self.imageCV, cv2.COLOR_BGR2GRAY)
            self.imageInMermory[self.imageInMermory > 0] = 255

            self.c.delete(ALL)
            self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

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

        im3 = im3 - im3
        cv2.drawContours(im3, contours, -1, 255)

        temp = self.imgOriginalCV.copy()

        #self.draw = ImageDraw.Draw(Image.fromarray(im3))

        for y in range(lin):
            for x in range(col):
                if im3[y, x] == 255:
                    temp[y, x] = [255, 255, 255]
                    self.draw.point((int(x * guiX / y2), y * guiY / x2), fill='white')

        self.imgright = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)

        self.imgLeft = ImageTk.PhotoImage(Image.fromarray(self.imgright).resize((guiX, guiY), Image.ANTIALIAS))

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

    def mostra(self, img, name='Name'):
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def original_img(self):
        self.c.delete(ALL)
        imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        self.imgLeft = ImageTk.PhotoImage(imageCV600)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

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

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'black' if self.eraser_on else 'white'
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=paint_color, width=self.choose_size_button.get())
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def resetImage(self):
        imageCV600 = Image.open(self.root.filename).resize((guiX, guiY), Image.ANTIALIAS)
        self.imgLeft = ImageTk.PhotoImage(imageCV600)

        self.c.delete(ALL)
        self.c.create_image(0, 0, image=self.imgLeft, anchor=NW)

        messagebox.showinfo("Espere", "Clique em OK e espere o algoritmo de processamento terminar de executar")

        self.imageCV = CellDetectionImage(self.imgOriginalCV)

        self.lin, self.col, _ = self.imageCV.shape
        img1 = cv2.resize(self.imageCV, (guiX, guiY), interpolation=cv2.INTER_AREA)
        self.goldImage = ImageTk.PhotoImage(Image.fromarray(img1))
        # self.goldImage = ImageTk.PhotoImage(imageCV)

        self.label_image.configure(image=self.goldImage)

    def individualregioncolor(self, im1):
        try:
            _, _ = im1.shape
            im2 = im1
        except:
            im2 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

        im2 = cv2.threshold(im2, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
        ret, labels = cv2.connectedComponents(im2)

        # Map component labels to hue val
        label_hue = np.uint8(179 * labels / (np.max(labels)))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue == 0] = 0

        return labeled_img


if __name__ == '__main__':
    GUI()
