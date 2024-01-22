from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')
import copy
import time
import math
start = time.time()
#We still gotta do stuf with the super class that like combines the 2, but idk maybe tuesday
class SAW(): #Square Lattice
    def __init__(self, path=[(0,0)]):
        SAW.path = path # het pad als koppeltjes, meegegeven als je niks hebt meegegeven
    #2D self-avoiding random walk laten groeien
    def __add__(self, other): #self = length of path and other is how much you grow it by
        self2 = copy.copy(self) #kopiërt de self
        NewMaxLength = other+len(self2.path) #nieuwe maximale lengte berekenen we nu
        CurrentPoint=self2.path[-1]
        x, y = CurrentPoint[0], CurrentPoint[1]
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
                x, y = self2.path[-1][0], self2.path[-1][1] #x, y back to your old x, y   
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
        TotalLength=0
        MaxDistancePosX=0 
        MaxDistanceNegX=0  
        MaxDistancePosY=0 
        MaxDistanceNegY=0      
        for i in range(1,len(self.path)):    #go through all points of the saw
            CurrentPoint=self.path[i]        
            Length=abs(CurrentPoint[0])+abs(CurrentPoint[1])    #length of current point in saw from 0,0
            TotalLength +=Length
            if CurrentPoint[0]>MaxDistancePosX:     #keep track of the biggest distance from 0,0 in the saw
                MaxDistancePosX=CurrentPoint[0]
            elif CurrentPoint[0]<MaxDistanceNegX:
                MaxDistanceNegX=CurrentPoint[0]
            if CurrentPoint[1]>MaxDistancePosY:
                MaxDistancePosY=CurrentPoint[1]
            elif CurrentPoint[1]<MaxDistanceNegY:
                MaxDistanceNegY=CurrentPoint[1]
        Xrange=MaxDistancePosX-MaxDistanceNegX          #check which axis has a greater range
        Yrange=MaxDistancePosY-MaxDistanceNegY
        if Xrange>Yrange:                           #set the other axis to the same range so the saw gets plotted in a grid with equal x and y lims
            MaxDistancePosY+=(Xrange-Yrange)/2
            MaxDistanceNegY-=(Xrange-Yrange)/2
        elif Yrange>Xrange:
            MaxDistancePosX+=(Yrange-Xrange)/2
            MaxDistanceNegX-=(Yrange-Xrange)/2

        plt.xlim(MaxDistanceNegX-1,MaxDistancePosX+1)       #update x and y lims
        plt.ylim(MaxDistanceNegY-1,MaxDistancePosY+1)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')  
        #average saw length: total length divided by total points       
        AvgLength=TotalLength/(len(self.path)-1)
        print(AvgLength)  
        plt.show()

class HEX(): #Hexagonal Lattice, work in progress
    def __init__(self, path=[(0,0)]):
        HEX.path = path # het pad als koppeltjes, meegegeven als je niks hebt meegegeven
    #2D self-avoiding random walk laten groeien
    def __add__(self, other): #self = length of path and other is how much you grow it by
        self2 = copy.copy(self) #kopiërt de self
        NewMaxLength = other+len(self2.path) #nieuwe maximale lengte berekenen we nu
        CurrentPoint=self2.path[-1]
        x, y = CurrentPoint[0], CurrentPoint[1]
        illegal = [] #the one iteration illegal maker, to make sure that backtracking works and the SAW doesn't take the same path twice in a row
        hexbool = True #2 different option lists, depending where on the hexagon you are (flipped on the y axis, flips every move)
        while len(self2.path)<NewMaxLength:
            if hexbool == True: #Reason for these options will be added in the report
                options = [(x+1, y), (x-1/2, y+math.sqrt(3)/2), (x-1/2, y-math.sqrt(3)/2)] #all the potential options
            else: #either True or false
                options =  [(x-1, y), (x+1/2, y+math.sqrt(3)/2), (x+1/2, y-math.sqrt(3)/2)]

            # pick the closest point  without crossing itself
            aoptions = [] # allowed options list
            for i in range(0,len(options)):
                if options[i] not in self2.path and options[i] not in illegal:
                    aoptions.append(options[i]) # stopt ze in de toegestaande opties
            print("laatste punt in pad: ", self2.path[-1], "opties: ", aoptions, "hexbool: ", hexbool )
            if len(aoptions)==0: #if there are no possible paths left before our SAW got a length of n, we're gonna backtrack as much as necessary
                illegal.append((x,y)) #makes this point illegal for 1 iteration so that it wont literally take this path again
                del self2.path[-1] # deletes your currentpoint from self2.path (your SAW's path)
                x, y = self2.path[-1][0], self2.path[-1][1] #x,y back to your old x, y
            else: # if there are options
                u, v = choice(aoptions) #finds a random path from the possible options
                x, y = u, v #swaps back to our original values
                self2.path.append((x, y)) #new piece of path added
            hexbool = hexbool*-1# you're moving either by adding a new path or by deleting your last path, so hexbool changes
        return self2

    #show plot
    def __pos__(self): # het tonen van de SAW. MOET NOG COMPLEET AANGEPAST WORDEN VOOR HEX, VOORAL DE AVERAGE!
        plt.figure(figsize=(100, 100))
        # draw points
        plt.scatter(*zip(*self.path), s=10, c='k')
        # draw lines in red
        plt.plot(*zip(*self.path), c='r')
        TotalLength=0
        MaxDistancePosX=0 
        MaxDistanceNegX=0  
        MaxDistancePosY=0 
        MaxDistanceNegY=0      
        for i in range(1,len(self.path)):    #go through all points of the saw
            CurrentPoint=self.path[i]        
            Length=abs(CurrentPoint[0])+abs(CurrentPoint[1])    #length of current point in saw from 0,0
            TotalLength +=Length
            if CurrentPoint[0]>MaxDistancePosX:     #keep track of the biggest distance from 0,0 in the saw
                MaxDistancePosX=CurrentPoint[0]
            elif CurrentPoint[0]<MaxDistanceNegX:
                MaxDistanceNegX=CurrentPoint[0]
            if CurrentPoint[1]>MaxDistancePosY:
                MaxDistancePosY=CurrentPoint[1]
            elif CurrentPoint[1]<MaxDistanceNegY:
                MaxDistanceNegY=CurrentPoint[1]
        Xrange=MaxDistancePosX-MaxDistanceNegX          #check which axis has a greater range
        Yrange=MaxDistancePosY-MaxDistanceNegY
        if Xrange>Yrange:                           #set the other axis to the same range so the saw gets plotted in a grid with equal x and y lims
            MaxDistancePosY+=(Xrange-Yrange)/2
            MaxDistanceNegY-=(Xrange-Yrange)/2
        elif Yrange>Xrange:
            MaxDistancePosX+=(Yrange-Xrange)/2
            MaxDistanceNegX-=(Yrange-Xrange)/2

        plt.xlim(MaxDistanceNegX-1,MaxDistancePosX+1)       #update x and y lims
        plt.ylim(MaxDistanceNegY-1,MaxDistancePosY+1)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')  
        #average saw length: total length divided by total points       
        AvgLength=TotalLength/(len(self.path)-1)
        print(AvgLength)  
        plt.show()

#main
    
#if __name__ == '__main__': 
# path = pathing(100000) #decides the length of the saw
# show_path(path)
Newsaw = SAW()
Newhex = HEX()
Updatedsaw = Newsaw+300
Updatedhex = Newhex+300
Updatedsaw.__pos__()
Updatedhex.__pos__()
end = time.time()
print("time:", end-start)