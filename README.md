# SAW
Self-avoiding walk
by Stefan van den Berg and Ilkka Kramer

This program contains an algorithm to generate a random SAW of a chosen length in a square or hexagonal lattice. Furthermore, the program can calculate the total amount of SAWs of length n, as well as some important properties related to these walks.

How to use the program:

Create a new SAW by calling the SAW class, for example: MyNewSaw=SAW([(0,0)],"Hex").
The function requires two inputs. The first input stores information about the current path. If left empty, the code will use [(0,0)]. The second input differentiates between a square or hexagonal grid. If you want a square grid, type "square" and for a hexagonal grid type "Hex". If left empty, the code will use "square".

To grow the SAW, simply use "+", for instance: MyNewSaw += 50 or SAW_1 = MyNewSaw + 2

To plot the SAW, call SAW.__pos__(), for example: MyNewSaw.__pos__()

To calculate the total amount of SAWs of length 1-n and of type "square" or "Hex", call the Pathwalking function:
Pathwalking(15,"square"). 
Actually you don't even have to fill in "square" as your type, since "square" is seen as a default setting. As long as you fill in anything (in parentheses ofcourse) as your 2nd input the Pathwalking function will think you mean a square lattice. If you want to calculate the total amount of SAWs of length 1-n and of type "Hex", then you will have to specify.
In other words: Pathwalking(10,"Nothing") will calculate the total amount of SAWs of length 1 to-10 on a square lattice, while Pathwalking(10, "Hex") will calculate the total amount of SAWs of length 1-10 on a Hexagonal lattice.

This doesn't work that way when creating a new SAW and putting anything other than "square" or "Hex" as your 2nd input will cause issues, because the program doesn't support any other type of grid.

Some sample inputs are given at the bottom of the code.
Keep in mind that this program is sensitive to capital letters. This means that you shouldn't try to input MyNewSaw=SAW([(0,0)],"hex"), because "hex"!="Hex" and "hex"!="square" meaning the program will fail if you try to do anything with MyNewSaw.
Do note that "square" is not capitalized while "Hex" is.