from random import choice
from matplotlib import pyplot as plt
plt.style.use('Solarize_Light2')

class SAW():
    def __init__(self,SAW_Length):
        x, y = 0, 0
        path = [(x, y)] # het pad als koppeltjes
    #2D self-avoiding random walk
    def __add__(self, other): #length of path
        while len(path)<=SAW_Length:
            # pick the closest point  without crossing itself
            u, v = choice([(x+1, y), (x-1, y), (x, y+1), (x, y-1)]) #finds a random path
            if (x+1, y) in path and (x-1, y) in path and (x, y+1) in path and (x, y-1) in path: #if there are no possible paths left
                return path 
            elif (u, v) not in path: #if the random generated path doesn't cross itself
                x, y = u, v #swaps back to our original values
                path.append((x, y)) #new piece of path added
        return path

    #show plot
    def show_path(path): 
        plt.figure(figsize=(100, 100))
        # draw points
        plt.scatter(*zip(*path), s=10, c='k')
        # draw lines in red
        plt.plot(*zip(*path), c='r')
        plt.show()

    NewSaw=SAW()
    path=SAW.pathing(100000)
    #main
    
    if __name__ == '__main__': 
        path = pathing(100000) #decides the length of the saw
        show_path(path)