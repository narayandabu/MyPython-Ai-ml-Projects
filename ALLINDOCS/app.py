import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from miner import PDFMiner
import os
from AI_engine import model
import numpy as np
from tkinter import font

# Chnage The Paths as Per Your Convience
TITLE = 'PDF Viewer'
GEOMETRY = '900x900+440+180'
ICON_IMAGE_PATH = 'ALLINDOCS/Assets/icon.png'
MODEL_PATH = 'ALLINDOCS/Assets/model_6_skimlit.keras'
UPARROW_IMG = 'ALLINDOCS/Assets/up.png'
DOWNARROW_IMG = 'ALLINDOCS/Assets/down.png'

class ALLINDOCS:
    def __init__(self,master) -> None:
        self.pdf = None
        self.path = None
        self.master = master
        self.master.title(TITLE)
        self.master.geometry(GEOMETRY)
        self.master.resizable(width = 0, height = 0)
        self.icon = tk.PhotoImage(file=ICON_IMAGE_PATH)
        self.master.iconphoto(True,self.icon)
        self.fileisopen = 0
        self.data = {
            'string':[],
            'line_num':[], 
        }
        self.isdataready = 0
        self.summary = None
        self.model = model()
        self.windows = []
        self.arranged = None

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

        self.optionsmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Options',menu=self.optionsmenu)
        self.optionsmenu.add_command(label='Arrange',command = self.arrange)
        self.optionsmenu.add_command(label='Arrange all(Only works with page<=10)',command = self.arrangeall)
        self.optionsmenu.add_command(label='Summary',command = self.summarize)

        # creating the top frame
        self.top_frame = ttk.Frame(self.master, width=850, height=800)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)
        self.bottom_frame = ttk.Frame(self.master, width=800, height=65)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)

        
        self.output = tk.Canvas(self.top_frame, bg='#ECE8F3', width=800, height=800)
        # Scroll Bars
        self.scrolly = tk.Scrollbar(self.top_frame, orient='vertical')
        self.scrollx = tk.Scrollbar(self.bottom_frame, orient='horizontal')
        self.scrolly.grid(row=0, column=1, sticky=('N','S'))
        

        self.output.grid(row=0, column=0)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)


        self.scrollx.grid(row=1, column=0, sticky=('W','E'))
        
        # creating the canvas for display the PDF pages
        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

        def on_mouse_wheel(event,canvas):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        self.master.bind("<MouseWheel>", on_mouse_wheel)  # For Windows/Mac
        self.master.bind("<Button-4>", lambda e: self.output.yview_scroll(-1, "units"))  # For Linux
        self.master.bind("<Button-5>", lambda e: self.output.yview_scroll(1, "units"))
        # loading the button icons
        self.uparrow_icon = tk.PhotoImage(file=UPARROW_IMG)
        self.downarrow_icon = tk.PhotoImage(file=DOWNARROW_IMG)
        self.uparrow = self.uparrow_icon.subsample(4, 3)
        self.downarrow = self.downarrow_icon.subsample(4, 3)

        self.upbutton = tk.Button(self.bottom_frame, image=self.uparrow,command=self.previous_page)
        self.upbutton.place(x=400,y=20)
        self.downbutton = tk.Button(self.bottom_frame, image=self.downarrow,command=self.next_page)
        self.downbutton.place(x=450,y=20)
        self.page_label = tk.Label(self.bottom_frame, text='page')
        self.page_label.place(x=500,y=25)
    def open_file(self):
        filepath = fd.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'), ))
        if filepath:
            self.path = filepath
            filename = os.path.basename(self.path)
            self.miner = PDFMiner(self.path)
            data, numPages = self.miner.get_metadata()
            self.current_page = 0
            self.fileisopen = 1
            if numPages:
                self.name = data.get('title', filename[:-4])
                self.author = data.get('author', None)
                self.numPages = numPages
                self.fileisopen = True
                self.display_page()
                self.master.title(self.name)
    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            self.img_file = self.miner.get_page(self.current_page)
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = str(self.stringified_current_page) + ' of ' + str(self.numPages)
            region = self.output.bbox('ALL')
            self.output.configure(scrollregion=region)
    def previous_page(self):
        if self.fileisopen:
            self.ismodelready = 0
            self.current_page = (self.current_page - 1 + self.numPages)%self.numPages
            self.display_page()
    def next_page(self):
        if self.fileisopen:
            self.ismodelready = 0
            self.current_page += 1
            self.current_page %= self.numPages
            self.display_page()
    def get_text(self,page_num):
        if self.fileisopen:
            text = self.miner.get_text(page_num)
            if text:
                self.data['string'] = text.split('.')
                self.data['line_num'] = np.arange(0,len(self.data['string']))
                return text
            else:
                print('NO TEXT FOUND')
    def get_all_text(self):
        if self.fileisopen:
            x = []
            for page_num in range(0,self.miner.total_pages):
                text = self.miner.get_text(page_num)
                if text:
                    x += text.split('.')
                else:
                    print('NO TEXT FOUND')
            self.data['string'] = x
            self.data['line_num'] = np.arange(0,len(self.data['string']))
            return 1
    def make_2nd_window(self):
        top = tk.Toplevel(self.master)
        top.title('....') 
        top.geometry(GEOMETRY)
        frame = ttk.Frame(top)
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame,bg='lightblue')

        h_scrollbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        h_scrollbar.pack(side="bottom", fill='x')
        canvas.configure(xscrollcommand=h_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=v_scrollbar.set)


        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        top.bind("<MouseWheel>", on_mouse_wheel)  # For Windows/Mac
        top.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # For Linux
        top.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        top.grid_rowconfigure(0, weight=1)
        top.grid_columnconfigure(0, weight=1)
        return top,canvas,content_frame
    def delete_all_windows(self):
        for window in self.windows:
            window.destroy()
    def arrange(self):
        self.get_text(self.current_page)
        top,canvas,content_frame = self.make_2nd_window()
        font1 = font.Font(family="Helvetica", size=14, weight="bold",underline=True)
        font2 = font.Font(family="Helvetica", size=12, slant="italic")
        label = tk.Label(content_frame, text='Arranging...',font=font1,foreground='Black')
        label.pack(pady=2)
        self.delete_all_windows()
        self.windows.append(top)
        if len(self.data['string']):
            label.destroy()
            top.title('Arranged Version') 
            if self.isdataready == 0:
                self.isdataready = 1
                self.model.get_data(self.data)
                self.model.refine_data()
            self.arranged = self.model.predict()
            for labels in self.arranged: 
                label = tk.Label(content_frame, text=labels+':',font=font1,foreground='Black')
                label.pack(pady=2)
                for s in self.arranged[labels]:
                    label = tk.Label(content_frame, justify="left",wraplength=500,text=s+'.',font=font2,foreground='Black')
                    label.pack(pady=2)
            content_frame.update_idletasks() 
            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            content_frame.bind("<Configure>", on_frame_configure)
        else:
            label.destroy()
            label = tk.Label(content_frame, text="NO TEXT FOUND TO ARRANGE",font=font1,foreground='Black')
            label.pack(pady=2)
    def arrangeall(self):
        self.get_all_text()
        top,canvas,content_frame = self.make_2nd_window()
        font1 = font.Font(family="Helvetica", size=14, weight="bold",underline=True)
        font2 = font.Font(family="Helvetica", size=12, slant="italic")
        label = tk.Label(content_frame, text='Arranging...',font=font1,foreground='Black')
        label.pack(pady=2)
        self.delete_all_windows()
        self.windows.append(top)
        if self.miner.total_pages <= 10:
            if len(self.data['string']):
                label.destroy()
                top.title('All Arranged Version')
                if self.isdataready == 0:
                    self.isdataready = 1
                    self.model.get_data(self.data)
                    self.model.refine_data()
                self.arranged = self.model.predict()
                for labels in self.arranged: 
                    label = tk.Label(content_frame, text=labels+':',font=font1,foreground='Black')
                    label.pack(pady=2)
                    for s in self.arranged[labels]:
                        label = tk.Label(content_frame, justify="left",wraplength=700,text=s+'.',font=font2,foreground='Black')
                        label.pack(pady=2)
                content_frame.update_idletasks() 
                def on_frame_configure(event):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                content_frame.bind("<Configure>", on_frame_configure)
            else:
                label.destroy()
                label = tk.Label(content_frame, text="NO TEXT FOUND TO ARRANGE",font=font1,foreground='Black')
                label.pack(pady=2)
        else:
            label = tk.Label(content_frame, text='Very Large Set to Arrange...',font=font1,foreground='Black')
    def summarize(self):
        self.delete_all_windows()
        if self.isdataready:
            self.summary = self.model.summarize()
            self.summary = self.summary.split('.')
        else:
            self.isdataready = 1
            self.get_text(self.current_page)
            self.model.get_data(self.data)
            self.summary = self.model.summarize()
            self.summary = self.summary.split('.')
        top,canvas,content_frame = self.make_2nd_window()
        font1 = font.Font(family="Helvetica", size=14, weight="bold",underline=True)
        font2 = font.Font(family="Helvetica", size=12, slant="italic")
        self.windows.append(top)
        if len(self.data['string']):
            top.title('Summarized Version') 
            if self.isdataready == 0:
                self.isdataready = 1
                self.model.get_data(self.data)
            label = tk.Label(content_frame, text='SUMMARY:',font=font1,foreground='Black')
            label.pack(pady=2)
            for labels in self.summary: 
                label = tk.Label(content_frame,justify="left",wraplength=500, text=labels+'.',font=font2,foreground='Black')
                label.pack(pady=2)
            content_frame.update_idletasks() 
            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            content_frame.bind("<Configure>", on_frame_configure)
    
root = tk.Tk()
app = ALLINDOCS(root)
root.mainloop()