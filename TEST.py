from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')
import copy

def show(self): # het tonen van de SAW 
        plt.figure(figsize=(100, 100))
        # draw points
        plt.scatter(*zip(*self), s=10, c='k')
        # draw lines in red
        plt.plot(*zip(*self), c='r')
        plt.show()

class SAW():
    def __init__(self, path=[(0,0)]):
        SAW.path = path # het pad als koppeltjes, meegegeven als je niks hebt meegegeven
    #2D self-avoiding random walk laten groeien
    def __add__(self, other): #self = length of path and other is how much you grow it by
        self2 = copy.copy(self) #kopiërt de self
        NewMaxLength = other+len(self2.path) #nieuwe maximale lengte berekenen we nu
        CurrentPoint=self2.path[-1]
        x, y = CurrentPoint[0], CurrentPoint[1]
        k=1
        illegal = [] #the one iteration illegal maker, to make sure that backtracking works and the SAW doesn't take the same path twice in a row
        while len(self2.path)<NewMaxLength: 
            options = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)] #all the potential options
            # pick the closest point  without crossing itself
            aoptions = [] # allowed options list
            for i in range(0,len(options)):
                if options[i] not in self2.path and options[i] not in illegal:
                    aoptions.append(options[i]) # stopt ze in de toegestaande opties
            if len(aoptions)==0: #if there are no possible paths left before our SAW got a length of n, we're gonna backtrack as much as necessary
                illegal.append((x,y)) #makes this point illegal for 1 iteration so that it wont literally take this path again
                del self2.path[-1] # deletes your currentpoint from self2.path (your SAW's path)   
            else: # if there are options
                u, v = choice(aoptions) #finds a random path from the possible options
                x, y = u, v #swaps back to our original values
                self2.path.append((x, y)) #new piece of path added
        return self2

    #show plot
    def __pos__(self): # het tonen van de SAW 
        plt.figure(figsize=(100, 100))
        # draw points
        plt.scatter(*zip(*self.path), s=10, c='k')
        # draw lines in red
        plt.plot(*zip(*self.path), c='r')
        plt.show()

#main
    
#if __name__ == '__main__': 
# path = pathing(100000) #decides the length of the saw
# show_path(path)
        
Newsaw = SAW()
Updatedsaw = Newsaw+20
Updatedsaw.__pos__()
#Updatedsaw = Newsaw+10
