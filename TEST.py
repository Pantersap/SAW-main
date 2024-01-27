from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')
import copy
import time
import math
""" 
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

def Walking(n_max, n, point, roundedpoint, roundedpath, type, hexbool): #recursive checking, not super efficient but it works
     #n_max = the length of a path, n = how long your path is right now, point = the point you're on, path = the path of your path (Hugo)
    

    if n == n_max:                                  #End of the recursion
        if type == "Hex":                           #1 walk got finished
            distance = hexdistance(point)
        else:
            distance = abs(point[0])+abs(point[1])  #distance in square grid, needed for calculating avg distance
        return 1, distance

    Zn = 0                 #amount of paths leading away from this point in the path
    distance = 0           #total distance from endpoint to origin of all the paths coming from this point 
    #body of the recursion   
    roundedpath.append(roundedpoint) #adds our new point to the path 
    x = point[0] 
    y = point[1]

    if type == "Hex": 
        if hexbool == True: 
            options = [(x+1, y), (x-1/2, y+math.sqrt(3)/2), (x-1/2, y-math.sqrt(3)/2)] #available path options for hex
        else: 
            options = [(x-1, y), (x+1/2, y+math.sqrt(3)/2), (x+1/2, y-math.sqrt(3)/2)]
    else: 
        options = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  #available path options for square

    for i in range(0,len(options)):                    #checks every possible path from a certain point 
        newpoint = options[i]                          #our new point  
        roundednewpoint = (round((2*options[i][0]),0)/2, round((2*options[i][1]),0)/2) 
        if roundednewpoint not in roundedpath:
            Newvalues = Walking(n_max,n+1,newpoint,roundednewpoint,roundedpath,type,hexbool*-1) 
            Zn += Newvalues[0]
            distance += Newvalues[1]
    #out of the recursion
    roundedpath.remove(roundedpoint)#we found every walk from our point, so we go back to our previous point in the path

    return Zn, distance             #the amount of walks from our point that we found will be returned 

def Pathwalking(k, type):  #our actual path calculator
    oldμ = 69              #nonsensical value so n=1 does not cause issues at calculating the lattice constant approximation decrease
    for n in range(1,k+1): #k+1 because range does not include the last element
        start = time.time() 
        roundedpath = [] 
        hexbool = True 
        Zn, distance = Walking(n, 0, (0,0), (0,0), roundedpath, type, hexbool) #starts in (0,0) on an empty saw (length 0)
        μ = Zn**(1/n)                   #lattice constant approximation
        averagedistance = distance/Zn   #averagedistance = total distance divided by the 
        
        print(n)                        #print all important information                        
        print("amount of paths:", Zn)
        print("lattice constant approximation:", μ)
        print("lattice constant approximation decrease:", oldμ-μ) 
        print("average distance endpoint to origin:", averagedistance)
        end = time.time()
        print("time taken:", end-start)
        print("")
        oldμ = μ      #keeps track of the previous lattice constant

class SAW(): #main class for generating SAWs
    def __init__(self, path=[(0,0)],type="square"): #default path is square
        SAW.path = path                             #path stores the SAW itself in x, y coordinates
        SAW.type = type                             #the SAW can be generated on a square or hexagonal lattice
    #2D self-avoiding random walk laten groeien
    def __add__(self, other):                    #self stores the SAW and other is how much you grow it by
        if SAW.type=="square":
            self2 = copy.copy(self)              #copies the SAW
            NewMaxLength = other+len(self2.path) #calculate end saw length
            CurrentPoint=self2.path[-1]
            x, y = CurrentPoint[0], CurrentPoint[1]
            illegal = [] #this array stores points the SAW cannot visit, as it would block itself
            while len(self2.path)<NewMaxLength: 
                options = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)] #all the potential options
                aoptions = []                                      #allowed options list so it doesnt cross itself
                for i in range(0,len(options)):
                    if options[i] not in self2.path and options[i] not in illegal:
                        aoptions.append(options[i])             #add current option to allowed options
                if len(aoptions)==0:                            #if there are no 'legal moves' the SAW will start backtracking
                    illegal.append((x,y))                       #makes this point illegal so it doesnt take this path again
                    del self2.path[-1]                          #deletes your currentpoint from self2.path (the SAW's path)
                    x, y = self2.path[-1][0], self2.path[-1][1] #x, y back to  old x, y   
                else: # if there are allowed options
                    u, v = choice(aoptions)   #finds a random direction from the possible options
                    x, y = u, v               #swaps back to our original values
                    self2.path.append((x, y)) #new piece of path added
            return self2
        elif SAW.type=="Hex":       #if the SAW is on a hexagonal grid
            self2 = copy.copy(self) #some parts of the code are similar to square grid
            NewMaxLength = other+len(self2.path) 
            CurrentPoint=self2.path[-1]
            x, y = CurrentPoint[0], CurrentPoint[1]
            illegal = [] 
            hexbool = True      #2 different option lists, depending where on the hexagon the saw is (flipped on the y axis, flips every move)
            roundedpath = []    #to fix floating point errors, we will only look at y rounded down to the nearest .5
            for i in range(0,len(self2.path)):
                roundedpath.append((self2.path[i][0], math.floor(2*self2.path[i][1])/2)) #i'th path, you round y down to the nearest .5. x is already a multiple of .5
                
            while len(self2.path)<NewMaxLength:
                if hexbool == True: #reason for these options will be added in the report
                    options = [(x+1, y), (x-1/2, y+math.sqrt(3)/2), (x-1/2, y-math.sqrt(3)/2)] #all the potential options
                else: #either True or false
                    options =  [(x-1, y), (x+1/2, y+math.sqrt(3)/2), (x+1/2, y-math.sqrt(3)/2)]

                #pick the closest point  without crossing itself
                aoptions = [] #allowed options list
                for i in range(0,len(options)):
                    roundedoption = (math.floor(2*options[i][0])/2, math.floor(2*options[i][1])/2) #rounded option
                    if roundedoption not in roundedpath and roundedoption not in illegal:
                        aoptions.append(options[i]) #adds this option to allowed options
                if len(aoptions)==0:                #if there are no possible paths left before our SAW got a length of n, the SAW will start backracking
                    illegal.append((math.floor(2*x)/2, math.floor(2*y)/2)) #makes this point illegal for 1 iteration so that the SAW will not take this path again (it's already rounded for use)
                    del self2.path[-1]                          #deletes your currentpoint from self2.path (the SAW's path)
                    del roundedpath[-1]                         #also has to delete the rounded version of this point
                    x, y = self2.path[-1][0], self2.path[-1][1] #x,y back to old x, y
                else: #if there are options
                    u, v = choice(aoptions)     #finds a random path from the possible options
                    x, y = u, v                 #swaps back to our original values
                    self2.path.append((x, y))   #new piece of path added
                    roundedpath.append((math.floor(2*x)/2, math.floor(2*y)/2))
                hexbool = hexbool*-1# you are moving either by adding a new path or by deleting your last path, so hexbool changes
            return self2
    
    def __pos__(self): #show plot and calculate distance from endpoint to 0, 0
        plt.figure()
        plt.scatter(*zip(*self.path), s=10, c='k')  #draw SAW points
        plt.plot(*zip(*self.path), c='r')           #connect SAW points with black lines
        MaxDistancePosX=0           #keep track of SAW extremities in n,e,s,w direction
        MaxDistanceNegX=0  
        MaxDistancePosY=0 
        MaxDistanceNegY=0      
        for i in range(1,len(self.path)):    #go through all points of the saw
            CurrentPoint=self.path[i]        #whenever a point is further from 0,0 than any point before that, store that information
            if CurrentPoint[0]>MaxDistancePosX:    
                MaxDistancePosX=CurrentPoint[0]
            elif CurrentPoint[0]<MaxDistanceNegX:
                MaxDistanceNegX=CurrentPoint[0]
            if CurrentPoint[1]>MaxDistancePosY:
                MaxDistancePosY=CurrentPoint[1]
            elif CurrentPoint[1]<MaxDistanceNegY:
                MaxDistanceNegY=CurrentPoint[1]
        Xrange=MaxDistancePosX-MaxDistanceNegX          #check which axis has a greater range
        Yrange=MaxDistancePosY-MaxDistanceNegY
        if Xrange>Yrange:                               #set the other axis to the same range so the saw gets plotted in a grid with equal x and y lims
            MaxDistancePosY+=(Xrange-Yrange)/2
            MaxDistanceNegY-=(Xrange-Yrange)/2
        elif Yrange>Xrange:
            MaxDistancePosX+=(Yrange-Xrange)/2
            MaxDistanceNegX-=(Yrange-Xrange)/2

        plt.xlim(MaxDistanceNegX-1,MaxDistancePosX+1)       #update x and y lims
        plt.ylim(MaxDistanceNegY-1,MaxDistancePosY+1)
        ax = plt.gca()
        ax.set_aspect('equal', adjustable='box')  
        if SAW.type=="square":
            Xdistance=self.path[int(len(self.path))-1][0]       #calculate distance between end of SAW and 0, 0
            Ydistance=self.path[int(len(self.path))-1][1] 
            print("SAW distance:",abs(Xdistance)+abs(Ydistance))  
            default_x_ticks=[]
            default_y_ticks=[]
            for i in range(-1+int(MaxDistanceNegX),int(MaxDistancePosX)+2):
                default_x_ticks.append(i)                       #create an array for xticks, to create a proper lattice
            for i in range(-1+int(MaxDistanceNegY),int(MaxDistancePosY+2)):
                default_y_ticks.append(i)                       #same for yticks
            plt.xticks(default_x_ticks)                         
            plt.yticks(default_y_ticks)
            plt.show()
        elif SAW.type=="Hex":     #calculating this distance for a hexagonl SAW is more complicated
            print("Hexdistance:",(hexdistance(self.path[-1])))
            plt.show()
    

Newsaw = SAW([(0,0)],"square")
Updatedsaw = Newsaw+300
Updatedsaw.__pos__()
Pathwalking(12,"Stephan")