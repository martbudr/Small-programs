import pygame
import time
from pygame.locals import *

# posprawdzac wi i he - ktore powinno byc ktorym gdzie !

WI, HE = 400, 400
ELEMENT_SIZE = 10
ELS_IN_1D = WI//ELEMENT_SIZE # how many in one direction
AMT_NEIGH = [[0 for i in range(ELS_IN_1D)] for j in range(ELS_IN_1D)]

class App:    
    def __init__(self):
        self._running = True
        self._displaySurf = None
        
        self.ALIVE = set()
        self.CANDIDATES = set()  
    
    def _onInit(self):
        pygame.init()
        self._displaySurf = pygame.display.set_mode((WI, HE), pygame.HWSURFACE)
        self._running = True
        self._initialSetup()
    
    def _initialSetup(self):
        self._updateNeighs((0,2), 1)
        self._updateNeighs((1, 2), 1)
        self._updateNeighs((2, 2), 1)
        self._updateNeighs((1, 0), 1)
        self._updateNeighs((2, 1), 1)
        self._onRender()

    def _onEvent(self, event):
        if event.type == QUIT:
            self._running = False
           
    # main logic of the game: 
    def _onLoop(self):     
        for live in self.ALIVE:
            self._checkIfShouldBeAlive(live)
        
        TO_DELETE = set()
        for live in self.ALIVE:
            wi, he = live[0], live[1]     
            if AMT_NEIGH[wi][he] != 2 and AMT_NEIGH[wi][he] != 3:
                TO_DELETE.add(live) 
                
        for live in TO_DELETE:
            self._updateNeighs(live, -1)
            
        for cand in self.CANDIDATES:
            self._updateNeighs(cand, 1)
        self.ALIVE.union(self.CANDIDATES)
        self.CANDIDATES.clear()                
    
    # just rendering graphics:
    def _onRender(self):
        for live in self.ALIVE:
            x, y = live[0], live[1]
            pygame.draw.rect(self._displaySurf, (255, 255, 255), ((y*ELEMENT_SIZE, x*ELEMENT_SIZE), (ELEMENT_SIZE, ELEMENT_SIZE)))
            
        pygame.display.flip()
        time.sleep(0.2)
        self._displaySurf.fill((0,0,0))
    
    def _onCleanup(self):
        self._running = False
        pygame.quit()
        
    def onExecute(self):
        if self._onInit() == False:
            self._running = False
            
        while(self._running):
            for event in pygame.event.get():
                self._onEvent(event)
            self._onLoop()
            self._onRender()
        
        self._onCleanup()
        
    def _checkAmtNeighs(self, wi, he):
        if (wi, he) in self.ALIVE:
            return
        
        if AMT_NEIGH[wi][he] == 3:
            self.CANDIDATES.add((wi, he))
        elif (wi, he) in self.CANDIDATES:
            self.CANDIDATES.remove((wi, he))
    
    def _checkIfShouldBeAlive(self, toSet):
        wi, he = toSet[0], toSet[1]
        
        if(he-1 >= 0):
            self._checkAmtNeighs(wi, he-1)
        if(he+1 < ELS_IN_1D):
            self._checkAmtNeighs(wi, he+1)
        if(wi-1 >= 0):
            self._checkAmtNeighs(wi-1, he)
            if(he-1 >= 0):
                self._checkAmtNeighs(wi-1, he-1)
            if(he+1 < ELS_IN_1D):
                self._checkAmtNeighs(wi-1, he+1)
        if(wi+1 < ELS_IN_1D):
            self._checkAmtNeighs(wi+1, he)
            if(he-1 >= 0):
                self._checkAmtNeighs(wi+1, he-1)
            if(he+1 < ELS_IN_1D):
                self._checkAmtNeighs(wi+1, he+1)
    
    def _updateNeighs(self, toSet, amt): # mozna dodac dodatkowa funkcje, ktora robilaby dla jednego wymiaru, powtorzyc ja 3 razy i usunac dla srodkowej wartosci w kwadracie 3x3
        wi, he = toSet[0], toSet[1]
            
        if(amt == 1):
            self.ALIVE.add(toSet)    
        elif(amt == -1):
            self.ALIVE.remove(toSet)
            
        if(he-1 >= 0):
            AMT_NEIGH[wi][he-1] += amt
        if(he+1 < ELS_IN_1D):
            AMT_NEIGH[wi][he+1] += amt
        if(wi-1 >= 0):
            AMT_NEIGH[wi-1][he] += amt
            if(he-1 >= 0):
                AMT_NEIGH[wi-1][he-1] += amt
            if(he+1 < ELS_IN_1D):
                AMT_NEIGH[wi-1][he+1] += amt
        if(wi+1 < ELS_IN_1D):
            AMT_NEIGH[wi+1][he] += amt
            if(he-1 >= 0):
                AMT_NEIGH[wi+1][he-1] += amt
            if(he+1 < ELS_IN_1D):
                AMT_NEIGH[wi+1][he+1] += amt
            
        
if __name__ == "__main__":
    theApp = App()
    theApp.onExecute()