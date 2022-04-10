from tkinter import Canvas, Spinbox
from PositionalPolygon import *


class ShapeCanvas(Canvas):    

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.sides = None
        self.shape_render = None
        self.shape_id = None
        self.shape2_id = None
        self.rot = None

        self.bind('<Button-1>', self.startpos)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<ButtonRelease-1>', self.endpos)
        self.create_text(60, 30, text='No. of Sides:')
        self.shapes =  Spinbox(self, from_=2, to=360, increment=1, width=5)
        self.widg = self.create_window(125, 30, height=25, width = 50, window = self.shapes)
        self.tag_lower(self.widg)


    def endpos(self, event):
        if self.shape2_id is not None:
            self.delete(self.shape2_id)
        

    def drag(self, event):
        #store the new mouse position
        self.buffer_point = Point(event.x, event.y)

        #verify the number of sides
        self.sides = int(self.shapes.get())
        
        #make way for new objects
        if self.shape_id is not None:
            self.delete(self.shape_id)
        if self.shape2_id is not None:
            self.delete(self.shape2_id)

        #find the angle of the mouse position relative to the starting click in radians
        self.rad = getangle(self.start_point, self.buffer_point)
                
        #for non-lines
        if self.sides > 2:
            #draw the angle viewer
            self.shape2_id = draw_line(self.start_point, self.buffer_point, self, dash = (1,6), fill='black')

            #render the polgon
            self.shape_id, self.shape_render = RegularPolygon(self.sides, distance(self.start_point, self.buffer_point)*2, self.start_point).draw(self, fill='red')
            
            #apply mouse-focused rotation to the polygon
            if self.rot != 0.0 and self.shape_render is not None:
                self.shape_id, self.shape_render = self.shape_render(self, self.rad, fill='red')
                self.tag_lower(self.shape_id)
        else:
            self.shape_id = draw_line(self.start_point, self.buffer_point, self, dash = (3,1), fill='red')


    def startpos(self, event):
        self.start_point = Point(event.x, event.y)                

