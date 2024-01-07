from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
    
    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def close(self):
        self.__running = False
        

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.p1.x, 
                           self.p1.y, 
                           self.p2.x, 
                           self.p2.y,
                           fill=fill_color,
                           width=2)
        canvas.pack(fill=BOTH, expand=1)
   