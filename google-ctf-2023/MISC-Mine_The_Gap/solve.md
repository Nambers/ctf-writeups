# MINE THE GAP
## Description
Take a break from the other challenges and play a relxing game of Minesweeper  
I have even solved most of the board for you and marked many of the mines.  
I am completely sure they are correct so you just need to find the remaining ones.  

Instructions:  
The game client requires pygame. Navigate the board with the arrow keys.  
Click an unexplored cell to toggle a flag marking a cell as containing a mine.  
Already placed flags can not be removed. Every cell with a number should have  
that many flags adjacent to it. Press "m" to validate the board.  
The flag will appear in the console.  
## Attachments and official writeup
[https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/misc-mine-the-gap](https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/misc-mine-the-gap)
## Solution
I put all variable(the empty cell), and other constrains into z3 solver to get the flag.  
[solve script](./solve.ipynb)