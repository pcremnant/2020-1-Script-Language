from tkinter import *
from tkinter import font


class point:
    def __init__(self, name, x=0, y=0, w=5, h=5, v=0):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.value = v
        self.name = name

    def getRect(self):
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height

class GraphGUI:
    # global mailMarked

    def __init__(self, mailMarked):
        self.window = Tk()

        # window
        self.width = 800
        self.height = 600
        self.widthBorder = 100
        self.heightBorder = 100
        self.window.geometry(str(self.width) + 'x' + str(self.height))
        self.window.resizable(False, False)
        self.window.title('test')

        # canvas
        self.canvas = Canvas(self.window, relief='solid', bd=2, bg='white', width=self.width, height=self.height)
        self.canvas.pack()

        # font
        self.fontValue = font.Font(self.canvas, size=10, weight='bold', family='consolas')
        self.fontName = font.Font(self.canvas, size=20, weight='bold', family='consolas')

        # point
        self.points = [point('기술사'), point('기능장'), point('기사'), point('기능사')]
        self.size = 0
        self.maxValue = 0

        self.setPoint(mailMarked)
        self.drawGraph()

        self.window.mainloop()

    def setPoint(self, mailMarked):
        for mark in mailMarked:
            if mark.seriesCode == '01':
                self.points[0].value += 1
            elif mark.seriesCode == '02':
                self.points[1].value += 1
            elif mark.seriesCode == '03':
                self.points[2].value += 1
            elif mark.seriesCode == '04':
                self.points[3].value += 1

        for p in self.points:
            if p.value > 0:
                self.size += 1
            if p.value > self.maxValue:
                self.maxValue = p.value

    def drawGraph(self):

        idx = 0.5
        w = self.width - self.widthBorder
        h = self.height - self.heightBorder * 2
        for p in self.points:
            if p.value > 0:
                p.x = w / self.size * idx + self.widthBorder
                p.y = (1 - p.value / self.maxValue) * h + self.heightBorder + 50
                self.canvas.create_oval(p.getRect(), fill='red')
                self.canvas.create_text(p.x, p.y - 20, text=p.value, font=self.fontValue)
                self.canvas.create_text(p.x, self.height - self.heightBorder + 50, text=p.name, font=self.fontName)
                idx += 1
        self.canvas.create_rectangle(self.widthBorder, self.heightBorder, self.width,
                                     self.height - self.heightBorder)
        for i in range(self.maxValue):
            self.canvas.create_text(self.widthBorder // 2, i / self.maxValue * h + self.heightBorder + 50,
                                    text=self.maxValue - i, font=self.fontValue)
        self.canvas.create_rectangle(0, 0, self.width, self.heightBorder)
        self.canvas.create_text(self.width//2, self.heightBorder//2, text='북마크 된 정보 그래프', font=self.fontName)