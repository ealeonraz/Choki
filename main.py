from functions import gui
from tkinter import Tk


def main():
    with open('./pathway/imagePath.txt', 'w') as o:
        o.seek(0)
        o.truncate
        o.close()
    root = Tk()
    loopme = gui.GUI(root)
    root.mainloop()
  
if __name__ == '__main__':
    main()