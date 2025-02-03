# VQsX Assembly Program to Draw a Square

.entry START          # Directive to declare entry point.

:START:               # Main program label
    INIT;             # Initialize pen states
    SETORIGIN 0;      # Set origin to top-left
    COLOR 1;          # Set pen color to Bright Green
    BRIGHTNESS 10;    # Set pen brightness to maximum

    CALL DRAW_SQUARE;  # Call subroutine to draw a square

    HALT;              # Halt the execution

# Subroutine to draw a square
:DRAW_SQUARE:          # Subroutine label
    STPUSH             # Save current pen state
    POS 50, 50         # Move to the starting position (50, 50)

    # Draw the four sides of the square
    FORWARD 100       # Move forward 100 units
    ROTATEDEG 90      # Rotate 90 degrees clockwise
    FORWARD 100       # Move forward 100 units
    ROTATEDEG 90      # Rotate 90 degrees clockwise
    FORWARD 100       # Move forward 100 units
    ROTATEDEG 90      # Rotate 90 degrees clockwise
    FORWARD 100       # Move forward 100 units

    STPOP             # Restore pen state
    RETURN            # Return to the main program
