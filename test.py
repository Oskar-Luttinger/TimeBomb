import time
import threading
import curses
import sys
import requests
from random import randint, choice

GAME_ACTIVE = True
POINTS = 0
TASKS_TO_SOLVE = 4
lock = threading.Lock()

def get_input(win, prompt, upper=False):
    win.addstr(prompt)
    win.refresh()
    curses.echo()
    answer = win.getstr().decode().strip()
    curses.noecho()
    return answer.upper() if upper else answer

def compare(correct, answer):
    global POINTS
    if correct == answer:
        POINTS += 1
        return True
    return False

def get_word():
    try:
        return requests.get("https://random-word-api.vercel.app/api?words=1&length=7", timeout=3).json()[0]
    except:
        return "example"

def math_task(win):
    a, b = randint(1, 9), randint(1, 9)
    op = choice(["+", "-", "*"])
    correct = str(eval(f"{a}{op}{b}"))
    answer = get_input(win, f"\nVad är {a} {op} {b}?: ")
    return compare(correct, answer)

def symbol_task(win):
    symbols = ["×", "&", "^"]
    chosen = choice(symbols)
    symbol_str = ""
    size = randint(10, 20)
    for i in range(size):
        symbol_str += choice(symbols) + "    "
        if (i + 1) % 5 == 0:
            symbol_str += "\n\n"
    correct = str(symbol_str.count(chosen))
    answer = get_input(win, f"\n{symbol_str}\nHur många {chosen} är det?: ")
    return compare(correct, answer)

def word_task(win):
    word = get_word()
    reverse = randint(0, 1)
    if reverse:
        correct = word
        prompt = f"\nSkriv ordet '{word}': "
    else:
        correct = word[::-1]
        prompt = f"\nSkriv ordet '{word}' BAKLÄNGES: "
    answer = get_input(win, prompt)
    return compare(correct, answer)

def alphabet_task(win):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ")
    letters = [choice(alphabet) for _ in range(3)]
    letters_str = "  ".join(letters)
    correct = min(letters, key=lambda l: alphabet.index(l))
    answer = get_input(win, f"\nVilken av bokstäverna {letters_str} kommer först i alfabetet?: ", upper=True)
    return compare(correct, answer)

TASK_FUNCTIONS = [math_task, word_task, symbol_task, alphabet_task]

def countdown_curses(stdscr, seconds):
    global GAME_ACTIVE
    start_time = time.perf_counter()
    end_time = start_time + seconds
    timer_win = curses.newwin(1, 40, 0, 0)
    timer_win.nodelay(True)

    while GAME_ACTIVE:
        remaining = end_time - time.perf_counter()
        if remaining <= 0:
            timer_win.erase()
            timer_win.addstr(0, 0, "00.000 - BOMB EXPLODED!")
            timer_win.refresh()
            GAME_ACTIVE = False
            return
        secs = int(remaining)
        millis = int((remaining - secs) * 1000)
        timer = f"BOMB TIMER: {secs:02d}.{millis:03d}"
        timer_win.erase()
        timer_win.addstr(0, 0, timer)
        timer_win.refresh()
        time.sleep(0.05)

def task_controller_curses(stdscr):
    global GAME_ACTIVE, POINTS
    task_win = curses.newwin(22, 100, 3, 0)
    task_win.scrollok(True)
    for i in range(TASKS_TO_SOLVE):
        if not GAME_ACTIVE:
            break
        task_win.erase()
        task_win.addstr(0, 0, f"Uppdrag {i + 1} av {TASKS_TO_SOLVE}\nPoäng: {POINTS}\n")
        task_win.refresh()
        task = choice(TASK_FUNCTIONS)
        result = task(task_win)
        if result:
            task_win.addstr("\nRätt!\n")
        else:
            task_win.addstr("\nFel! Bomben exploderade!\nSpelet är slut. Tryck valfri tangent för att avsluta.\n")
            task_win.refresh()
            GAME_ACTIVE = False
            return
        task_win.refresh()
        time.sleep(1)
    if GAME_ACTIVE and POINTS >= TASKS_TO_SOLVE:
        task_win.addstr("\nAlla uppdrag klara! Bomben är desarmerad!\n")
    elif GAME_ACTIVE:
        task_win.addstr("\nDu hann inte klart innan bomben exploderade!\n")
    task_win.addstr("\nSpelet är slut. Tryck valfri tangent för att avsluta.")
    task_win.refresh()
    time.sleep(2)

def main_curses(stdscr):
    global GAME_ACTIVE, POINTS
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(2, 0, "Välkommen till TimeBomb!")
    stdscr.addstr(3, 0, f"Du har 30 sekunder på dig att lösa {TASKS_TO_SOLVE} uppdrag.")
    stdscr.addstr(4, 0, "Tryck Enter efter varje svar.")
    stdscr.refresh()
    time.sleep(1)
    t1 = threading.Thread(target=countdown_curses, args=(stdscr, 30,))
    t2 = threading.Thread(target=task_controller_curses, args=(stdscr,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    stdscr.nodelay(False)
    stdscr.getch()

def menu():
    global GAME_ACTIVE, POINTS
    if input("Tryck 1 för att starta: ") == "1":
        try:
            GAME_ACTIVE = True
            POINTS = 0
            curses.wrapper(main_curses)
        except Exception as e:
            print(f"Ett fel uppstod: {e}", file=sys.stderr)

if __name__ == "__main__":
    menu()
