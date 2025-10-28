import time
import threading
import curses
import sys

GAME_ACTIVE = True 

def countdown_curses(stdscr, seconds):
    """Handles the continuously updating timer in its own window."""
    global GAME_ACTIVE
    total_time = float(seconds)
    interval = 0.01

    timer_win = curses.newwin(1, 20, 0, 0)
    timer_win.nodelay(True) 

    while total_time > 0 and GAME_ACTIVE:
        secs = int(total_time)
        millis = int((total_time - secs) * 1000)
        timer = f"BOMB TIMER: {secs:02d}.{millis:03d}"
        
        timer_win.erase()
        timer_win.addstr(0, 0, timer)
        timer_win.refresh()
        
        time.sleep(interval)
        total_time -= interval

    GAME_ACTIVE = False
    timer_win.erase()
    timer_win.addstr(0, 0, "00.000 - BOMB EXPLODED!")
    timer_win.refresh()

def taskController_curses(stdscr):
    """Handles the task prompt and input in its own window."""
    global GAME_ACTIVE
    answer = "answer"
    
    task_win = curses.newwin(5, 80, 2, 0)
    task_win.keypad(True)

    task_win.addstr(0, 0, "\nThis is a task \n")
    task_win.addstr(2, 0, "\nSolution to the task is?: ")
    task_win.refresh()

    try:
      
        task_win.move(4, 0) 
        task_win.clrtoeol()
        
        curses.echo() 
        choice = task_win.getstr().decode('utf-8') 
        curses.noecho() 

    except:
      
        choice = ""

    task_win.erase()
    if GAME_ACTIVE:
        if choice == answer:
            task_win.addstr(0, 0, "Correct! Bomb Defused")
            GAME_ACTIVE = False 
        else:
            task_win.addstr(0, 0, "Wrong loser! The bomb is still ticking!")
        task_win.refresh()
        
    time.sleep(2)

def main_curses(stdscr):
    
    curses.curs_set(0)
    stdscr.clear() 
    stdscr.refresh()

    t1 = threading.Thread(target=countdown_curses, args=(stdscr, 20,))
    t2 = threading.Thread(target=taskController_curses, args=(stdscr,))

    stdscr.addstr(6, 0, "Welcome to TimeBomb! Complete the task quickly!")
    stdscr.addstr(7, 0, "Task: 'answer'")
    stdscr.addstr(8, 0, "Hit Enter after typing your solution.")
    stdscr.refresh()
    
    time.sleep(1) 

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    stdscr.addstr(10, 0, "Game Over. Press any key to exit.")
    stdscr.nodelay(False)
    stdscr.getch()

def menu():
    global GAME_ACTIVE
    choice = input("Enter 1 to start the TimeBomb game: ")
    if choice == "1":
       
        try:
            curses.wrapper(main_curses)
        except Exception as e:
           
            print(f"An error occurred: {e}", file=sys.stderr)
        
        GAME_ACTIVE = True 

menu()