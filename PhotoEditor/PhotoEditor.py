from tkinter import * 
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import PIL 
from PIL import Image, ImageTk, ImageFilter
from ImageHistory import ImageHistory
 

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class application:
    def __init__(self,master):
        self.master = master
        self.width = 700
        self.height = 500
        self.scale = Scale()
        self.blurvalue = IntVar()
        self.history = ImageHistory(10)
        self.setup_gui(self.width, self.height, self.scale)
        self.img=None
        
        
 
    def setup_gui(self,w, h, s):
        Label(self.master,text = 'Image Editor',pady=5,bg='white',
            font=('Ubuntu',30)).pack()
        self.canvas = Canvas(self.master,height=h ,width=w,
            bg='black',relief='ridge')
        self.canvas.pack()
        txt = '''
                  !
            No Image
        '''
        self.wt = self.canvas.create_text(self.width/2-40, self.height/2 ,text=txt
            ,font=('',30),fill='white')
        f=Frame(self.master,bg='white',padx=10,pady=10)

        Button(f,text='Open New Image',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.make_image).pack(side=LEFT)
        Button(f,text='Rotate',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.rotate_image).pack(side=RIGHT)
        Button(f,text='Black and white',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.make_blacknwhite).pack(side=RIGHT)
        self.scale = Scale(f, sliderlength = 5, orient = HORIZONTAL, resolution=1, from_=0, to_=5, variable = self.blurvalue).pack(side = RIGHT)
        Button(f,text='Blur',bd=2,fg='white',bg='black',font=('',15)
            ,command=self.make_blur).pack(side=RIGHT)
        Button(f,text='Undo', bd=2,fg='white',bg='black',font=('',15)
            ,command=self.undo).pack(side=RIGHT)
        Button(f,text='Redo', bd=2,fg='white',bg='black',font=('',15)
            ,command=self.redo).pack(side=RIGHT)

        f.pack()
 
 
    # Kép betöltése
    def make_image(self):
        try:
            File = fd.askopenfilename(filetypes=[('jpg files', '*.jpg')])
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
        print(w, h)
        self.width = w
        self.height = h
        while self.height > 1700 or self.width > 920 or self.width > 1700 or self.height > 920:
            self.width = int(self.width//1.2)
            self.height = int(self.height//1.2)
        print(self.width, self.height)
        self.resizedImage = self.pilImage.resize((self.width, self.height),Image.NEAREST)


    # Visszavonás
    def undo(self):
        self.pilImage = self.history.Undo() # előző kép betöltése
        self.resizedImage_to_canvas()  # betöltött kép -> kicsinyített kép -> canvas    


    # Újra
    def redo(self):
        self.pilImage = self.history.Redo() # következő kép betöltése
        self.resizedImage_to_canvas()  # betöltött kép -> kicsinyített kép -> canvas    

root=Tk()
root.configure(bg='white')
root.title('Image Viewer')
application(root)
FullScreenApp(root)
root.resizable(0,0)
root.mainloop()
