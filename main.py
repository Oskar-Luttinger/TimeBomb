import time
import threading
import curses
import sys

GAME_ACTIVE = True

def countdown_curses(stdscr, seconds):
    global GAME_ACTIVE
    start_time = time.perf_counter()
    end_time = start_time + seconds

    timer_win = curses.newwin(1, 30, 0, 0)
    timer_win.nodelay(True)

    while GAME_ACTIVE:
        remaining = end_time - time.perf_counter()
        if remaining <= 0:
            break

        secs = int(remaining)
        millis = int((remaining - secs) * 1000)
        timer = f"BOMB TIMER: {secs:02d}.{millis:03d}"

        timer_win.erase()
        timer_win.addstr(0, 0, timer)
        timer_win.refresh()

        time.sleep(0.01)

    GAME_ACTIVE = False
    timer_win.erase()
    timer_win.addstr(0, 0, "00.000 - BOMB EXPLODED!")
    timer_win.refresh()


def taskController_curses(stdscr):
    global GAME_ACTIVE
    answer = "answer"

    task_win = curses.newwin(5, 80, 2, 0)
    task_win.keypad(True)

    task_win.addstr(0, 0, "This is a task\n")
    task_win.addstr(1, 0, "Skriv 'answer' för att desarmera bomben.\n")
    task_win.addstr(3, 0, "Lösning på uppgiften: ")
    task_win.refresh()

    try:
        curses.echo()
        choice = task_win.getstr().decode('utf-8').strip()
        curses.noecho()
    except:
        choice = ""

    task_win.erase()
    if GAME_ACTIVE:
        if choice == answer:
            task_win.addstr(0, 0, "Correct")
            GAME_ACTIVE = False
        else:
            task_win.addstr(0, 0, "Incorrect! The bomb exploded ")
        task_win.refresh()

    time.sleep(2)


def main_curses(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    stdscr.addstr(6, 0, "Welcome to TimeBomb")
    stdscr.addstr(7, 0, "Complete the tasks so the bomb doesn't explode")
    stdscr.refresh()

    time.sleep(1)

    t1 = threading.Thread(target=countdown_curses, args=(stdscr, 20,))
    t2 = threading.Thread(target=taskController_curses, args=(stdscr,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    stdscr.addstr(10, 0, "\nThe game is over press any key to end the game")
    stdscr.nodelay(False)
    stdscr.getch()


def menu():
    global GAME_ACTIVE
    choice = input("Press 1 to play")
    if choice == "1":
        try:
            curses.wrapper(main_curses)
        except Exception as e:
            print(f"An issue occured {e}", file=sys.stderr)
        GAME_ACTIVE = True


if __name__ == "__main__":
    menu()
