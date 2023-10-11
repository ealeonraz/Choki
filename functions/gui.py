import tkinter as tk
from PIL import ImageTk, Image
import os
from tkinter import END, filedialog
from tkinter.filedialog import askopenfile, askopenfilename
import re
import shutil
from functions import white_noise_cropping as wnc
#Creates the GUI for the app
class GUI:
    def __init__(self, master):
        self.master = master
        master.resizable(False, False)
        master.geometry('750x525')
        master.title("Choki")
        self.width_screen = master.winfo_screenwidth()
        self.height_screen = master.winfo_screenheight()
        self.x = (self.width_screen/2) - (750/2)
        self.y = (self.height_screen/2) - (525/2)
        self.functions_frame = tk.LabelFrame(master, text="Funcions", height = 500, width = 200, fg="black", relief=tk.SUNKEN)
        self.functions_frame.place(x=520, y=10)
        self.images_frame = tk.LabelFrame(master, height = 500, width = 500, fg = "black", relief = tk.SUNKEN)
        self.images_frame.place(x=15, y=10)
        self.images_frame_label = tk.Label(height = 490, width = 490)
        self.images_frame_label.place(x=520, y=10)
        master.geometry('%dx%d+%d+%d' % (750, 525, self.x, self.y))
        self.note_open = tk.PhotoImage(file='./button_images/open.png')
        self.note_label = tk.Label(image=self.note_open)
        self.folder_button = tk.Button(master, image=self.note_open, borderwidth=0,
                            command=lambda : self.grab_image_path(self.dir_images))  
        self.folder_button.place(x=690, y=50)
        self.import_img_btn = tk.Button(master, text = "Import", command=lambda: self.import_image(self.dir_images))
        self.import_img_btn.place(x=550, y= 90, width = 100)
        self.dir_images = tk.Entry(master, width=5)
        self.dir_label = tk.Label(text="Import Images")
        self.dir_label.place(x=530, y=28)
        self.crop_white_btn = tk.Button(master, text="Crop", command = lambda: wnc.dir_loop('./images'))
        self.crop_white_btn.place(x=550, y=155, width=100)
        self.dir_images.place(x = 530, y = 50, width = 150)
        self.display_img_btn = tk.Button(master, text = "Display Image", command=lambda: self.display_image('dp'))
        self.display_img_btn.place(x=550, y = 220, width=100)
        self.arrow_fwrd_open = tk.PhotoImage(file='./button_images/forward_btn.png')
        self.arrow_fwrd_label = tk.Label(image=self.arrow_fwrd_open)
        self.arrow_foward_button = tk.Button(master, image=self.arrow_fwrd_open, borderwidth=0, command=
                                    lambda:self.display_image('fw'))
        self.arrow_foward_button.place(x=650, y=220)
        self.arrow_bkwrd_open = tk.PhotoImage(file='./button_images/backward_btn.png')
        self.arrow_bkwrd_label = tk.Label(image=self.arrow_bkwrd_open)
        self.arrow_backward_button = tk.Button(master, image=self.arrow_bkwrd_open, borderwidth=0, command=
                                    lambda: self.display_image('bw'))
        self.arrow_backward_button.place(x=522, y=220)
        self.dest_folder = "./images"
        self.dllist = doubly_linked_list()
        for file in os.listdir('./im_output'):
            self.dllist.append(file)
        self.cur_node = self.dllist.head
        #Looks for all image files within a specified path and returns all those image files. Also saves the path to a txt file for later use.
    def grab_image_path(self, path):
        self.filename = filedialog.askdirectory()
        path.insert(0, self.filename)
        with open('./pathway/imagePath.txt', 'w') as o:
            o.write(self.filename)
            o.close()
    #Imports all files ending in jpg or png to the images file in this app from the selected path inside of the text folder.
    def import_image(self, path):
        with open('./pathway/imagePath.txt', 'r') as o:
            self.filename = o.readline()
            o.close()
        for file in os.listdir(self.filename):
            self.filename2 = os.fsdecode(file)
            if (re.search('.(?:jpg|png)$', self.filename2)):
                shutil.copy(f'{self.filename}/{self.filename2}', self.dest_folder)
    #Have display_image reset image area to head node if clicked each time
    def display_image(self, btn):  
        self.path = './im_output'
        self.image_picture = ImagePicture(self.cur_node) #Create a new ImagePicture object with the current node
        #Checks if the theres images in the folder
        if btn == 'dp': #If button hit is display
            self.cur_node = self.dllist.head #Set cur_node as the head node
            if not os.listdir(self.path):
                return #return if path empty
            else:
                self.image_picture = ImagePicture(self.cur_node) #Display the cur_node
        elif btn == 'fw':
            #If the button is forward, return if next node is nonexistent
            if self.cur_node.next == None:
                return 
            else:
                #Set the cur_node to the next node, display the node
                self.cur_node = self.cur_node.next
                self.image_picture = ImagePicture(self.cur_node)
        elif btn == 'bw':
            #If button is back return if the previous node is non existent
            if self.cur_node.prev == None:
                return
            else: 
                #Move back in the doubly linked list and display the image
                self.cur_node = self.cur_node.prev
                self.image_picture = ImagePicture(self.cur_node)

#ImagePicture class, used to create Image object for displaying on the GUI
class ImagePicture:
    def __init__(self, node):
        self.node = node
        self.path = './im_output'
        self.image = Image.open(f'{self.path}/{node.data}')
        self.image = self.image.resize((493, 493), Image.ANTIALIAS) #Apply resampling filter on shorter image
        self.display_image = ImageTk.PhotoImage(image = self.image) #Convert PIL image to tkinter compatible PhotoImage
        self.image_label = tk.Label(image=self.display_image) #Creates a label widget to display the image
        self.image_label.image = self.display_image
        self.image_label.place(x=17, y=12)
#Node Class
class Node:
   def __init__(self, data):
      self.data = data
      self.next = None
      self.prev = None
# Doubly Linked List Class
class doubly_linked_list:
   #Class initialization
   def __init__(self):
      self.head = None
    #Method to add elements at the beginning of the list
   def push(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.next = self.head
      if self.head is not None:
         self.head.prev = NewNode
      self.head = NewNode
#Method to add elements at the end of the list
   def append(self, NewVal):
      NewNode = Node(NewVal)
      NewNode.next = None
      if self.head is None:
         NewNode.prev = None
         self.head = NewNode
         return
      last = self.head
      while (last.next is not None):
         last = last.next
      last.next = NewNode
      NewNode.prev = last
      return
# Define the method to print
   def listprint(self, node):
      while (node is not None):
         print(f'Position is {node.data}')
         last = node
         node = node.next