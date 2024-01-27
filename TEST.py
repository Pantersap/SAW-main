from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')
import copy
import time
import math
""" We still gotta do stuf with the super class that like combines the 2, but idk maybe tuesday
 dingen die we in de recursieve formule van Z_N moeten berekenen:
1: aantal walks, gwn de recursieve formule, er steeds 1 bij optrekken aan het einde van de walk
2: lattice constant, doe je aan het hele einde, door gwn z_n^(1/n_max) te doen
3: average distance from endpoint to origin for a set the set of walks:
    naast dat we aan het einde van iedere walk een 1 optellen voor het aantal paden, berekenen we ook distance van endpoint to origin.
    Dit is gwn abs(x)+abs(y) voor square en het is de hexdistance() functie voor hexagonal.
    Dan aan het einde delen we de totale lengte door Z_N en we hebben average distance (we kunnen dus zowel total als average distance printen)
4: rauwe average distance (als in pythagoras):
    Simpelweg sqrt(x^2+y^2) per walk en tellen we hetzelfde op als de echte average distance (weer kunnen we beide printen)
We printen dus 6 dingenn:
Z_N; 
lattice constant approximatie voor die N;
average distance eindpunt-oorsprong voor die N
total distance eindpunt-oorsprong voor die N
rauwe average distance eindpunt-oorsprong voor die N
rauwe total distance eindpunt-oorsprong voor die N
"""
def hexdistance(endpoint): #calculates the average distance from endpoint to origin in a hex lattice
        x = endpoint[0]
        y = endpoint[1]
        y_offset = 2*abs(y)/math.sqrt(3) #1 move is sqrt(3)/2, amount of times you have to move down/up in 1 
        x_offset = abs(x)/1.5 #amount you move in the x direction after 2 moves going in the same direction, you go in the y direction ones
        if x_offset-math.floor(x_offset)==0: #checks if x is a multiple of 1.5, hence you need to move an even number of moves to the right/left
            x_offset = 2*math.floor(x_offset) #total amount of moves needed
        else:
            x_offset = 2*math.floor(x_offset)+1 # the extra move
        # combo's van steeds 1 directie in de x, je sneller y is nul bereikt dan x = 0 wil je hier
        if x>=0: #if you moved an odd number of moves in the x direction, your last move will have been one moving directly one to the right  without moving in the y direction
            if x_offset>=2*y_offset: #you reach y=0 before x=0 by going in the x direction the entire time and up/down in the y ones every 2 turns
                distance = x_offset #staircasing works fine here
            else: 
                distance = x_offset+y_offset-math.floor(x_offset/2)
                #you first go to x=0, this is the x_offset. in this you moved floor(x_offset/2) times in the y direction (14->7, 15->7)
                #because you moved that much in the y direction, you have subtract it from the extra y_offset you have to move

        elif x<0: # if you moved an odd number of moves in the x direction, your last move will be a diagonal move
            if (x_offset-1)>=2*(y_offset-1): #takes it into account, works out
                distance = x_offset #staircasing works
            else:
                distance = x_offset+y_offset-math.floor((x_offset+1)/2) #same idea but in x_offset moves you move floor((x_offset+1)/2) times
        return int(round(distance, 1)) #fixes rounding errors

def Walking(n_max, n, point, path, roundedpoint, roundedpath, type, hexbool): #recursief checken, niet super efficiënt maar het werkt.
     #n_max = the length of a path, n = how long your path is right now, point = the point you're on, path = the path of your path (Hugo)
    
    #End of the recursion
    if n == n_max: #1 walk got finished
        if type == "Hex":
            distance = hexdistance(point)
        else:
            distance = abs(point[0])+abs(point[1]) #distance in square grid
        return 1, distance
    
    #Body of the recursion
    Zn = 0 #amount of paths leading away from this point in the path
    distance = 0 # total distance from endpoint to origin of all the paths coming from this point

    path.append(point) # adds our new point to the path: 
    roundedpath.append(roundedpoint) #same thing with the roundedpoint
    x = point[0] 
    y = point[1]

    if type == "Hex": # hex lattice
        if hexbool == True: #Reason for these options will be added in the report
            options = [(x+1, y), (x-1/2, y+math.sqrt(3)/2), (x-1/2, y-math.sqrt(3)/2)] #all the potential options
        else: #either True or false
            options = [(x-1, y), (x+1/2, y+math.sqrt(3)/2), (x+1/2, y-math.sqrt(3)/2)]
    else: #square lattice
        options = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)] #your options

    for i in range(0,len(options)): #checkt elk mogelijke pad vanaf een bepaald punt
        newpoint = options[i] #our new point
        roundednewpoint = (round((2*options[i][0]),0)/2, round((2*options[i][1]),0)/2) #rounded option
        if roundednewpoint not in roundedpath:
            Newvalues = Walking(n_max,n+1,newpoint,path,roundednewpoint,roundedpath,type,hexbool*-1)  #swaps hexbool because the saw moves ones
            Zn += Newvalues[0]
            distance += Newvalues[1]

    #out of the recursion
    path.remove(point) #we've found every walk from our point, so we go back to our previous point in the path
    roundedpath.remove(roundedpoint) #same thing with roundedpath

    return Zn, distance # the amount of walks from our point that we found will be given back

def Pathwalking(k, type): #our actual path calculator, that calculates the red stuff 
    oldμ = 69 #nonsensical value so n=1 doesn't cause issues at calculating the lattice constant approximation decrease
    for n in range(1,k+1): #k+1 cause range doesn't pick the last element
        start = time.time()
        path = []
        roundedpath = [] #alleen voor hex
        hexbool = True #alleen voor hex
        Zn, distance = Walking(n, 0, (0,0), path, (0,0), roundedpath, type, hexbool) #starts in (0,0) on an empty saw (length 0)
        μ = Zn**(1/n) #lattice constant approximation
        averagedistance = distance/Zn # averagedistance = total distance divided by the amount
        print(n)
        print("amount of paths:", Zn)
        print("lattice constant approximation:", μ)
        print("lattice constant approximation decrease:", oldμ-μ) #at n=1 this is nonsense as it's the first μ
        print("average distance endpoint to origin:", averagedistance)
        end = time.time()
        print("time taken:", end-start)
        print("")
        oldμ = μ #houdt de vorige lattice constant approximation bij 

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
        roundedpath = [] #To fix floating point errors, we will only look at y rounded down to the nearest .5
        for i in range(0,len(self2.path)):
            roundedpath.append((self2.path[i][0], math.floor(2*self2.path[i][1])/2)) #i'th path, you round y down to the nearest .5. x is already a multiple of .5
            
        while len(self2.path)<NewMaxLength:
            if hexbool == True: #Reason for these options will be added in the report
                options = [(x+1, y), (x-1/2, y+math.sqrt(3)/2), (x-1/2, y-math.sqrt(3)/2)] #all the potential options
            else: #either True or false
                options =  [(x-1, y), (x+1/2, y+math.sqrt(3)/2), (x+1/2, y-math.sqrt(3)/2)]

            # pick the closest point  without crossing itself
            aoptions = [] # allowed options list
            for i in range(0,len(options)):
                roundedoption = (math.floor(2*options[i][0])/2, math.floor(2*options[i][1])/2) #rounded option
                if roundedoption not in roundedpath and roundedoption not in illegal:
                    aoptions.append(options[i]) # stopt ze in de toegestaande opties
            if len(aoptions)==0: #if there are no possible paths left before our SAW got a length of n, we're gonna backtrack as much as necessary
                illegal.append((math.floor(2*x)/2, math.floor(2*y)/2)) #makes this point illegal for 1 iteration so that it wont literally take this path again (it's already rounded for use)
                del self2.path[-1] # deletes your currentpoint from self2.path (your SAW's path)
                del roundedpath[-1] #obviously also has to delete the rounded version of this point
                x, y = self2.path[-1][0], self2.path[-1][1] #x,y back to your old x, y
            else: # if there are options
                u, v = choice(aoptions) #finds a random path from the possible options
                x, y = u, v #swaps back to our original values
                self2.path.append((x, y)) #new piece of path added
                roundedpath.append((math.floor(2*x)/2, math.floor(2*y)/2))
            hexbool = hexbool*-1# you're moving either by adding a new path or by deleting your last path, so hexbool changes
        return self2

    #show plot
    def __pos__(self):
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
        # print(AvgLength) not important appearently this wasn't even what was asked
        print("Hexdistance:", (hexdistance(self.path[-1]))) # prints distance endpoint to origin
        plt.show()
    





#main
    
#if __name__ == '__main__': 
# path = pathing(100000) #decides the length of the saw
# show_path(path)
Newsaw = SAW()
Newhex = HEX()
Updatedsaw = Newsaw+30
Updatedhex = Newhex+30
Updatedsaw.__pos__()
Updatedhex.__pos__()
Pathwalking(25, "Hex")