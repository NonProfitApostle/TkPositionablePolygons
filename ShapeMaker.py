import tkinter as tk
from ShapeCanvas import ShapeCanvas as sc



class ShapeMaker(tk.Tk):

    def __init__(self):
        super().__init__()
        self.canv = sc(self, width=800, height=600)
        self.canv.grid(row= 1, column = 2, sticky = 'nsew')

    def run(self):
        self.mainloop()  


    def Exit(self):
        self.quit()


if __name__ == "__main__":
    sf = ShapeMaker()
    sf.run()
