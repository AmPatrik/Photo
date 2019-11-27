from tkinter import * 
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import PIL 
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from ImageHistory import ImageHistory
 

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=40
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()-100))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class application:
    def __init__(self,master):
        self.master = master
        self.width = master.winfo_screenwidth() - 375
        self.height = master.winfo_screenheight() - 180
        self.maxwidth = self.width
        self.maxheight = self.height
        self.blurvalue = IntVar()
        self.brightnessvalue = DoubleVar()
        self.sharpnessvalue = DoubleVar()
        self.contrastvalue = DoubleVar()
        self.history = ImageHistory(10)
        self.extension = StringVar()
        self.setup_gui(self.width, self.height)
        self.img=None
        
        
 
    def setup_gui(self,w, h):
        Label(self.master,text = 'Photo Editor',pady=5,bg='grey',
            font=('Courier new',30)).pack(fill=X)
        
        txt = "No image"
        
        f=Frame(self.master,bg='grey',padx=10,pady=10, bd = 5) #file megnyitás ás effektek frame-je
        f2=Frame(self.master,bg='grey',padx=10,pady=10, bd = 5) #undo-redo frame-je
        f3=Frame(self.master, bg='black', padx=10, pady=10, bd=3) #kép frame-je
        
        
        
        self.canvas = Canvas(f3,height=h ,width=w,
            bg='black',relief='ridge')
        self.wt = self.canvas.create_text(self.width/2, self.height/2 ,text=txt
            ,font=('',30),fill='white')
        self.canvas.pack()
        
        #file megnyitás
        Button(f,text='Open New Image',bd=2,fg='black',bg='gray80',font=('',15) ,command=self.make_image, pady=30).pack(side=TOP, fill=X)
        #effketek
        Button(f,text='Rotate',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.rotate_image).pack(side=TOP, fill=X)
        Button(f,text='Black and white',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.make_blacknwhite).pack(side=TOP, fill=X)
        Button(f,text='Blur',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.make_blur).pack(side=TOP, fill=X)
        Scale(f, sliderlength = 5, orient = HORIZONTAL, resolution=1, from_=0, to_=5, variable = self.blurvalue, label='Blur value').pack(side = TOP, fill=X)
        Button(f,text='Flip',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.flip).pack(side=TOP, fill=X)
        Button(f,text='Change brightness',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.brightness).pack(side=TOP, fill=X)
        scale1 = Scale(f, sliderlength = 5, orient = HORIZONTAL, resolution=0.1, from_=0, to_=5, variable = self.brightnessvalue, label='Brightness value')
        scale1.set(1)
        scale1.pack(side=TOP, fill=X)
        Button(f,text='Change sharpness',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.sharpness).pack(side=TOP, fill=X)
        scale2 = Scale(f, sliderlength = 5, orient = HORIZONTAL, resolution=0.1, from_=0, to_=10, variable = self.sharpnessvalue, label='Sharpness value')
        scale2.set(0)
        scale2.pack(side=TOP, fill=X)
        Button(f,text='Change contrast',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.contrast).pack(side=TOP, fill=X)
        scale3 = Scale(f, sliderlength = 5, orient = HORIZONTAL, resolution=0.1, from_=-10, to_=10, variable = self.contrastvalue, label='Contrast value')
        scale3.set(0)
        scale3.pack(side=TOP, fill=X)

        #mentés
        self.extension.set("jpg")
        OptionMenu(f, self.extension, "jpg", "png").pack(side=BOTTOM, fill=X)
        Label(f, text='Select extension', bg='snow3', font=("Ariel", 15)).pack(side=BOTTOM, fill=X)
        Button(f,text='Save',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.save).pack(side=BOTTOM, fill=X)
        #undo-redo gombok
        Button(f2,text='Undo', bd=2,fg='white',bg='black',font=('',15)
            ,command=self.undo).pack(side=TOP, fill=X)
        Button(f2,text='Redo', bd=2,fg='white',bg='black',font=('',15)
            ,command=self.redo).pack(side=TOP, fill=X)

        #frame-ek elhelyezése
        f.pack(side = LEFT, fill=Y)
        f2.pack(side=LEFT, fill=Y)
        f3.pack(side=RIGHT, expand=1)
 
 
    # Kép betöltése
    def make_image(self):
        try:
            File = fd.askopenfilename(filetypes=[('Pictures', "*.png | *.PNG | *.jpg | *.JPG | *.bmp | *.BMP"), ('All files', '*')])
            self.pilImage = Image.open(File)    # eredeti nagy kép betöltése
            self.resizedImage_to_canvas()       # eredeti -> resizedImage -> img -> canvas
            self.history.AddImageToHistory(self.pilImage)   # eredeti kép -> history
        except:
            ms.showerror('Error!','File type is unsupported.')


    # Elforgatás
    def rotate_image(self):
        try:
            self.pilImage = self.pilImage.transpose(Image.ROTATE_90) # eredeti kép elforgatása
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')


    # Fekete-fehér
    def make_blacknwhite(self):
        try:    
            self.pilImage = self.pilImage.convert('L') # eredeti kép -> fekete-fehér
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')


    # Homályosítás
    def make_blur(self):
        try:
            self.pilImage = self.pilImage.filter(ImageFilter.GaussianBlur(radius = self.blurvalue.get())) # eredeti kép -> homályos
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')

    # Tükrözés
    def flip(self):
        try:
            self.pilImage = self.pilImage.transpose(Image.FLIP_LEFT_RIGHT) # eredeti kép -> tükrözött
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')

    # Fényerő
    def brightness(self):
        try:
            self.pilImage = ImageEnhance.Brightness(self.pilImage).enhance(self.brightnessvalue.get()) # eredeti kép -> fényesebb kép
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')

    # Élesítése
    def sharpness(self):
        try:
            self.pilImage = ImageEnhance.Sharpness(self.pilImage).enhance(self.sharpnessvalue.get()) # eredeti kép -> élesebb kép
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')

    # Kontraszt állítása
    def contrast(self):
        try:
            self.pilImage = ImageEnhance.Contrast(self.pilImage).enhance(self.contrastvalue.get()) # eredeti kép -> módosított kép
            self.resizedImage_to_canvas()
            self.history.AddImageToHistory(self.pilImage)
        except:
            ms.showerror('No photo', 'Select something')

    # resizedImage -> canvas
    def resizedImage_to_canvas(self):
        self.resize_pilImage()  # eredeti(nagy) kép -> resizedImage
        self.img = ImageTk.PhotoImage(self.resizedImage)
        self.canvas.delete(ALL)
        self.canvas.config(width=self.width, height=self.height)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)


    # pilImage átméretezése -> resizedImage
    def resize_pilImage(self):
        w, h = self.pilImage.size
        self.width = w
        self.height = h
        while self.width > self.maxwidth or self.height > self.maxheight -1:
            self.width = int(self.width//1.01)
            self.height = int(self.height//1.01)
        self.resizedImage = self.pilImage.resize((self.width, self.height),Image.NEAREST)


    # Visszavonás
    def undo(self):
        self.pilImage = self.history.Undo() # előző kép betöltése
        self.resizedImage_to_canvas()  # betöltött kép -> kicsinyített kép -> canvas    


    # Újra
    def redo(self):
        self.pilImage = self.history.Redo() # következő kép betöltése
        self.resizedImage_to_canvas()  # betöltött kép -> kicsinyített kép -> canvas    

    # Mentés
    def save(self):
        filename = fd.asksaveasfilename(title='Please select a directory') + "." + self.extension.get() #a file mentésének előkészítése, lekérdezi a kiterjesztést
        self.pilImage.save(filename)


root=Tk()
root.configure(bg='snow3')
root.title('Photo editor')
application(root)
FullScreenApp(root)
root.resizable(0,0)
root.mainloop()
