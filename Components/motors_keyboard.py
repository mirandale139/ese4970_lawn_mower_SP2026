import curses
from gpiozero import Servo
from time import sleep

# Setup pins
left_wheel = Servo(13, min_pulse_width=1/1000, max_pulse_width=2/1000)
right_wheel = Servo(12, min_pulse_width=1/1000, max_pulse_width=2/1000)

def stop_motors():
    left_wheel.mid()
    right_wheel.mid()

def main(stdscr):
    # Curses setup
    curses.curs_set(0) # Hide the cursor
    stdscr.nodelay(False) # Wait for user input
    stdscr.clear()
    
    # Arming sequence
    stdscr.addstr(0, 0, "Arming Sabertooth... Wait 3s")
    stdscr.refresh()
    stop_motors()
    sleep(3)
    
    stdscr.clear()
    stdscr.addstr(0, 0, "--- ROBOT KEYBOARD CONTROL ---")
    stdscr.addstr(1, 0, "Use Arrow Keys to move. Press 'q' to quit.")
    stdscr.refresh()

    # We define a small power constant (20%)
    p = 0.20 

    while True:
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        
        elif key == curses.KEY_UP:
            stdscr.addstr(3, 0, "Status: FORWARD ")
            left_wheel.value = -2 * p
            right_wheel.value = p
            
        elif key == curses.KEY_DOWN:
            stdscr.addstr(3, 0, "Status: BACKWARD")
            left_wheel.value = p
            right_wheel.value = -2 * p
            
        elif key == curses.KEY_LEFT:
            stdscr.addstr(3, 0, "Status: TURN LEFT")
            left_wheel.value = - 2 * p
            right_wheel.value = - 2 * p
            
        elif key == curses.KEY_RIGHT:
            stdscr.addstr(3, 0, "Status: TURN RIGHT")
            left_wheel.value =  p
            right_wheel.value =  p
            
        elif key == -1: # No key pressed
            pass
        
        else:
            stdscr.addstr(3, 0, "Status: STOPPED ")
            stop_motors()

        stdscr.refresh()
        # Small sleep to prevent CPU hogging
        sleep(0.1)
        # Automatically stop after a short burst if key isn't held (optional)
        stop_motors()

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass
finally:
    stop_motors()
    left_wheel.detach()
    right_wheel.detach()
    print("\nRobot shutdown safely.")
