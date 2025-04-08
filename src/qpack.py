#!/usr/bin/env python3
import vqsx

b : vqsx.Builder = vqsx.Builder()

def ren(b : vqsx.Builder, LINELENGTH : int = 100, TOPCORN : tuple = None): # Draw the VQsX QPack Logo
    if TOPCORN == None:
        TOPCORN = (-200, 150)

    def toppos(): ## Position at top (and initialize to be safe)
        b.position(*TOPCORN)
        b.color(vqsx.Colors.BBLUE)

    def dv(): ## Draw the V
        # Render it Red
        b.color(vqsx.Colors.BRED)

        # Draw it
        b.rotaterdeg(45)
        b.drawforward(LINELENGTH)
        b.rotatedeg(90)
        b.drawforward(LINELENGTH)
        # Move on
        b.rotaterdeg(45)
        b.forward(int(LINELENGTH/2))
        b.color(vqsx.Colors.BBLUE)

    def dq():## Draw the Q
        # Draw the box and prepare for the tick
        for i in range(1, 7):
            if i < 5: b.drawforward(LINELENGTH)
            else: b.forward(LINELENGTH)
            b.rotaterdeg(90)
        # Draw the tick
        b.rotatedeg(180) # Rotate 180 for left consistency
        b.rotaterdeg(45) # Rotate for corner tick
        b.backward(int(LINELENGTH/2))
        b.drawforward(LINELENGTH)
        # Move on
        toppos() # Position at top to go down
        b.rotatedeg(45) # Point to the right
        b.backward(30) # Move back for space
        b.rotaterdeg(90) # Point down
        b.forward(int(LINELENGTH*1.35)) # Go for S!

    def ds(): ## Draw an S

        # Prepare by going to right
        b.rotatedeg(90)
        b.backward(30) # Move a bit for X
        b.forward(LINELENGTH)

        # Draw to left
        b.rotaterdeg(180)
        b.drawforward(LINELENGTH)

        # Draw down
        b.rotatedeg(90)
        b.drawforward(int(LINELENGTH/2))

        # Draw to right
        b.rotatedeg(90)
        b.drawforward(LINELENGTH)

        # Draw down
        b.rotaterdeg(90)
        b.drawforward(int(LINELENGTH/2))

        # Draw to left
        b.rotaterdeg(90)
        b.drawforward(LINELENGTH)

        # prepare to move on
        # Go to corner
        b.rotaterdeg(90)
        b.forward(LINELENGTH)
        # Turn right
        b.rotaterdeg(90)
        # Move to other corner
        b.forward(LINELENGTH)
        # Move outside
        b.forward(int(LINELENGTH/2.5))

    def dx(): ## Draw an X
        # Point to left-down
        b.rotaterdeg(90)
        b.rotaterdeg(45)

        # Purple X
        b.color(vqsx.Colors.BPURPLE)

        # Draw a Tick
        b.drawforward(int(LINELENGTH/2.25))
        b.backward(int(LINELENGTH/2.25))
        # Return to normal
        b.rotatedeg(90)
        b.rotatedeg(45)
        
        # Draw the first diagonal
        b.rotaterdeg(45)
        b.drawforward(LINELENGTH)
        b.backward(int(LINELENGTH/2))
        # Draw the second diagonal
        b.rotatedeg(90)
        b.backward(int(LINELENGTH/2))
        b.drawforward(LINELENGTH)

        # Move On
        toppos() # Go to Top
        b.color(vqsx.Colors.BBLUE) # Change Color

    def dbox(): # Draw a box
        # Move back
        b.rotaterdeg(45)
        b.backward(LINELENGTH)
        b.rotaterdeg(90)
        b.forward(10)
        b.rotatedeg(90)

        # Change Color
        b.color(vqsx.Colors.AZURE)
        
        # Draw Box
        # Draw s1
        b.drawforward(int(LINELENGTH*4.25))
        b.rotaterdeg(90)
        # Draw s2
        b.drawforward(int(LINELENGTH*3))
        b.rotaterdeg(90)
        # Draw s3
        b.drawforward(int(LINELENGTH*4.25))
        b.rotaterdeg(90)
        # Draw s4
        b.drawforward(int(LINELENGTH*3))
        b.rotaterdeg(90)

        # Move on
        b.rotaterdeg(90)
        b.color(vqsx.Colors.BBLUE)


    toppos()
    dv()
    dq()
    # b.rotaterdeg(90)
    ds()
    dx()
    dbox()




with open("qpack.vBin", "wb") as f:
    ren(b)
    f.write(b.dump())