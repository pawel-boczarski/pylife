# -*- encoding: utf8 -*-

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
        
    def cleanAll(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                self.array[r][c] = NO_LIFE
        self.resetGeneration()
        self.updateDisplay()
        
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
        effective = False
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                if self.isLifeAt(r, c):
                    if self.numberOfNeighbours(r, c) < 2:
                        self.array[r][c] = LIFE_WILL_EXTINCT
                        effective = True
                    elif self.numberOfNeighbours(r, c) > 3:
                        self.array[r][c] = LIFE_WILL_EXTINCT
                        effective = True
                else:
                    if self.numberOfNeighbours(r, c) == 3:
                        self.array[r][c] = NO_LIFE_WILL_BE_BORN
                        effective = True
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                self.array[r][c] = CLEANUP_MAP[self.array[r][c]]
                
        self.generation += 1
 
        if effective == False:
            self.ineffectiveEvolutionHandler()
        else:
            self.updateDisplay()
        
    def ineffectiveEvolutionHandler(self):
        pass
                        
    def updateDisplay(self, row, col):
        pass
        
    def display(self):
        print "Generacja ", self.generation
        for i in range(0,self.rows):
            print " ".join(self.array[i])
    
    def resetGeneration(self):
        self.generation = 0
        self.setGenerationHandler(self.generation)
        
    def setGenerationHandler(self, gen):
        pass
            
    def main(self):
        while(a.population() > 0):
            a.evolve()
            time.sleep(1)
            print
            a.display()
                        
import gtk
import time
import gobject

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
        
class LifeUpperPanel(gtk.VBox):
    def __init__(self):
        super(LifeUpperPanel, self).__init__(None)
        self.label = gtk.Label("Generacja #0")
        self.buttonBox = gtk.HBox(10)
        self.startStopButton = gtk.Button("Start")
        self.singleStepButton = gtk.Button("Jeden krok")
        self.cleanButton = gtk.Button("Wyczyść")
        self.buttonBox.pack_start(self.startStopButton)
        self.buttonBox.pack_start(self.singleStepButton)
        self.buttonBox.pack_start(self.cleanButton)
        self.pack_start(self.label)
        self.pack_start(self.buttonBox)
        self.show_all()
        
        self.generation = 0
        self.gameState = LifeGtkImpl.EVOLUTION_STOPPED
        
    def setGeneration(self, gen):
        self.label.set_text("Generacja #" + str(gen))
        self.generation = gen
        
    def setGameState(self, gameState):
        self.gameState = gameState
        
    def updateDisplay(self):
        if self.gameState == LifeGtkImpl.EVOLUTION_RUNNING:
            self.startStopButton.set_label("Stop")
        else:
            if self.generation == 0:
                self.startStopButton.set_label("Start")
            else:
                self.startStopButton.set_label("Kontynuuj")
            
    def connectStartStopButton(self, signal, callback, data=None):
        self.startStopButton.connect(signal, callback, data)
        
    def connectSingleStepButton(self, signal, callback, data=None):
        self.singleStepButton.connect(signal, callback, data)
        
    def connectCleanButton(self, signal, callback, data=None):
        self.cleanButton.connect(signal, callback, data)
        
class LifeGtkImpl(LifeModel):
    # constants
    EVOLUTION_RUNNING = 1
    EVOLUTION_STOPPED = 0

    def __init__(self, r, c):
        super(LifeGtkImpl, self).__init__(r, c)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Conway's game of Life [PB 2013]")
        self.window.show()
        self.window.connect("destroy", lambda w: gtk.main_quit())
        

        self.upperPanel = LifeUpperPanel()
        self.upperPanel.show_all()
        
        self.lifeButtonTable = gtk.Table(r+2, c, True)
        
        self.lifeButtonTable.attach(self.upperPanel, 0, c, 0, 2, gtk.FILL | gtk.SHRINK, gtk.FILL | gtk.SHRINK, 0, 0)
            
        self.upperPanel.connectStartStopButton("clicked", self.startButtonCallback)
        self.upperPanel.connectSingleStepButton("clicked", self.singleStepButtonCallback)
        self.upperPanel.connectCleanButton("clicked", self.cleanButtonCallback)
        
                
        self.lifeButtons = list()
        for i in range(0, self.rows):
            self.lifeButtons.append(list())
            for j in range(0, self.cols):
                self.lifeButtons[i].append(LifeButton())
                self.lifeButtonTable.attach(self.lifeButtons[i][j],
                                        j, j+1, i+2, i+3, gtk.FILL,
                                        gtk.FILL, 0, 0)
                self.lifeButtons[i][j].show()
                self.lifeButtons[i][j].connect("clicked", self.otherButtonCallback, tuple((i,j)))

        #self.window.add(self.upperPanel)        
        self.window.add(self.lifeButtonTable)
        self.lifeButtonTable.show()       
        self.window.show()
                
        self.state = self.EVOLUTION_STOPPED
        
    def setEvolutionState(self, evolutionState):
        if self.state <> evolutionState:
            if evolutionState == self.EVOLUTION_RUNNING:
                self.tsourceId = gobject.timeout_add(1000, self.evolutionTimer)                
            else:
                gobject.source_remove(self.tsourceId)                
            self.state = evolutionState
            self.upperPanel.setGameState(self.state)
    
    def ineffectiveEvolutionHandler(self):
        if self.state == self.EVOLUTION_RUNNING:
            self.setEvolutionState(self.EVOLUTION_STOPPED)
                
    def updateDisplay(self, row=None, col=None):
        if row == None:
            for i in range(0, self.rows):
                for j in range(0, self.cols):
                    if self.isLifeAt(i, j) == 1:
                         self.lifeButtons[i][j].setLife()
                    else:
                         self.lifeButtons[i][j].setNoLife()
        else:
             if self.isLifeAt(row, col) == 1:
                  self.lifeButtons[row][col].setLife()
             else:
                  self.lifeButtons[row][col].setNoLife()
        
        self.upperPanel.setGameState(self.state)
        self.upperPanel.setGeneration(self.generation)
        self.upperPanel.updateDisplay()
                                   
    def display(self):
        self.updateDisplay()
    
    def startButtonCallback(self, widget, data=None):
        if self.state == self.EVOLUTION_STOPPED:
           a.evolve()
           self.setEvolutionState(self.EVOLUTION_RUNNING)
           self.upperPanel.updateDisplay()
        else:
            self.setEvolutionState(self.EVOLUTION_STOPPED)
            self.updateDisplay()
            
    def singleStepButtonCallback(self, widget, data=None):
        if self.state == self.EVOLUTION_STOPPED:
            a.evolve()
            
    def cleanButtonCallback(self, widget, data=None):
        self.setEvolutionState(self.EVOLUTION_STOPPED)
        a.cleanAll()
        
    def evolutionTimer(self):
        a.evolve()
        return True
        
    def otherButtonCallback(self, widget, data=None):
        if self.state == self.EVOLUTION_STOPPED:
            row = data[0]
            col = data[1]
            self.switchBeingAt(row, col)
            self.resetGeneration()
            
    def setGenerationHandler(self, gen):
        self.upperPanel.setGeneration(gen)
        #self.upperPanel.updateDisplay()
        
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