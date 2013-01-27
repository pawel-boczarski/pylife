NO_LIFE = '.'
LIFE = '*'

NO_LIFE_WILL_BE_BORN = '+'
LIFE_WILL_EXTINCT = '-'

COUNT_MAP = { NO_LIFE : 0, LIFE : 1, NO_LIFE_WILL_BE_BORN : 0, LIFE_WILL_EXTINCT : 1 }

CLEANUP_MAP = { NO_LIFE : NO_LIFE, LIFE : LIFE, NO_LIFE_WILL_BE_BORN : LIFE, LIFE_WILL_EXTINCT : NO_LIFE }

class LifeModel(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.array = []
        self.generation = 0
        for i in range(0, rows):
            row = [NO_LIFE] * self.cols
            self.array.append(row)
                        
    def putBeingAt(self, r, c):
        self.array[r][c] = LIFE
        self.updateDisplay(r, c)
        
    def killBeingAt(self, r, c):
        self.array[r][c] = NO_LIFE
        self.updateDisplay(r, c)
        
    def switchBeingAt(self, r, c):
        if(self.array[r][c] == LIFE):
            self.array[r][c] = NO_LIFE
        else:
            self.array[r][c] = LIFE
        self.updateDisplay(r, c)
            
    def isLifeAt(self, r, c):
        if r < 0:
            return 0
        if r > self.rows - 1:
            return 0
        if c < 0:
            return 0
        if c > self.cols - 1:
            return 0
        return COUNT_MAP[self.array[r][c]]
        
    def population(self):
        count = 0
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                count += COUNT_MAP[self.array[r][c]]
        return count
            
    def numberOfNeighbours(self, r, c):
        return (self.isLifeAt(r-1, c-1) + self.isLifeAt(r-1, c) + self.isLifeAt(r-1, c+1)
                + self.isLifeAt(r, c-1) + self.isLifeAt(r, c+1)
                + self.isLifeAt(r+1, c-1) + self.isLifeAt(r+1, c) + self.isLifeAt(r+1, c+1))
            
    def evolve(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if self.isLifeAt(r, c):
                    if self.numberOfNeighbours(r, c) < 2:
                        self.array[r][c] = LIFE_WILL_EXTINCT
                    elif self.numberOfNeighbours(r, c) > 3:
                        self.array[r][c] = LIFE_WILL_EXTINCT
                else:
                    if self.numberOfNeighbours(r, c) == 3:
                        self.array[r][c] = NO_LIFE_WILL_BE_BORN
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                self.array[r][c] = CLEANUP_MAP[self.array[r][c]]
                
        self.generation += 1
        self.updateDisplay()
                        
    def updateDisplay(self, row, col):
        pass
        
    def display(self):
        print "Generacja ", self.generation
        for i in range(0,self.rows):
            print " ".join(self.array[i])
            
    def main(self):
        while(a.population() > 0):
            a.evolve()
            time.sleep(1)
            print
            a.display()
                        
import gtk
import time

class LifeButton(gtk.Button):
    def __init__(self):
        super(LifeButton, self).__init__(None)
        self.image = gtk.Image()
        self.add(self.image)
        self.setNoLife()
        self.image.show()
    
    def setLife(self):
        self.image.set_from_file("life.xpm")
        
    def setNoLife(self):
        self.image.set_from_file("no_life.xpm")
        

class LifeGtkImpl(LifeModel):
    def __init__(self, r, c):
        super(LifeGtkImpl, self).__init__(r, c)
    #    self.model = LifeModel(r, c)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        self.startButton = gtk.Button("Start")
        self.startButton.show()
        
        self.lifeButtonTable = gtk.Table(r + 1, c, True)
        
        self.lifeButtonTable.attach(self.startButton,
                                        0, c, 0, 1, gtk.FILL|gtk.SHRINK,
                                        gtk.FILL|gtk.SHRINK, 0, 0)
        
        self.startButton.connect("clicked", self.startButtonCallback)
        
                
        self.lifeButtons = list()
        for i in range(0, self.rows):
            self.lifeButtons.append(list())
            for j in range(0, self.cols):
                self.lifeButtons[i].append(LifeButton())
                self.lifeButtonTable.attach(self.lifeButtons[i][j],
                                        j, j+1, i+1, i+2, gtk.FILL,
                                        gtk.FILL, 0, 0)
                self.lifeButtons[i][j].show()
                self.lifeButtons[i][j].connect("clicked", self.otherButtonCallback, tuple((i,j)))
        
        self.window.add(self.lifeButtonTable)
        self.lifeButtonTable.show()       
        self.window.show()
        
    def updateDisplay(self, row=None, col=None):
        if row == None:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    if self.isLifeAt(i, j) == 1:
 #                       self.lifeButtons[i][j].set_image(self.image_life)
                         self.lifeButtons[i][j].setLife()
                    else:
  #                      self.lifeButtons[i][j].set_image(self.image_no_life)
                         self.lifeButtons[i][j].setNoLife()
        else:
             if self.isLifeAt(row, col) == 1:
 #                self.lifeButtons[row][col].set_image(self.image_life)
                  self.lifeButtons[row][col].setLife()
             else:
#                 self.lifeButtons[row][col].set_image(self.image_no_life)
                  self.lifeButtons[row][col].setNoLife()
                 
    def display(self):
        self.updateDisplay()
    
    def startButtonCallback(self, widget, data=None):
        a.evolve()
        
    def otherButtonCallback(self, widget, data=None):
        row = data[0]
        col = data[1]
        self.switchBeingAt(row, col)
        
    def main(self):
        gtk.main()
            
if __name__ == '__main__':
    a = LifeGtkImpl(20, 20)
    a.putBeingAt(1, 1)
    a.putBeingAt(2, 2)
    a.putBeingAt(2, 0)
    a.putBeingAt(2, 3)
    a.putBeingAt(2, 4)
    a.putBeingAt(3, 5)
    a.display()
                
    a.main()