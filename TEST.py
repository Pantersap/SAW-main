from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')
import copy

class SAW():
    def __init__(self, path=[(0,0)]):
        SAW.path = path # het pad als koppeltjes, meegegeven als je niks hebt meegegeven
    #2D self-avoiding random walk laten groeien
    def __add__(self, other): #self = length of path and other is how much you grow it by
        self2 = copy.copy(self) #kopiërt de self
        CurrentPoint=self2.path[-1]
        x, y = CurrentPoint[0], CurrentPoint[1]
        while len(self2.path)<=other: 
            # pick the closest point  without crossing itself
            u, v = choice([(x+1, y), (x-1, y), (x, y+1), (x, y-1)]) #finds a random path
            if (x+1, y) in self2.path and (x-1, y) in self2.path and (x, y+1) in self2.path and (x, y-1) in self2.path: #if there are no possible paths left
                return self2 
            elif (u, v) not in self2.path: #if the random generated path doesn't cross itself
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

    
#main
    
#if __name__ == '__main__': 
# path = pathing(100000) #decides the length of the saw
# show_path(path)
        
Newsaw = SAW()
Updatedsaw = Newsaw+50000
Updatedsaw.__pos__()
#Updatedsaw = Newsaw+10