import time
import threading
import curses
import sys
import requests
from random import randint, choice

GAME_ACTIVE = True
POINTS = 0
TASKS_TO_SOLVE = 5
lock = threading.Lock()


# ==============================
#        TIMER FUNKTION
# ==============================
def countdown_curses(stdscr, seconds):
    """Visar en nedräkningstimer i eget curses-fönster."""
    global GAME_ACTIVE
    start_time = time.perf_counter()
    end_time = start_time + seconds

    with lock:
        timer_win = curses.newwin(1, 40, 0, 0)
        timer_win.nodelay(True)

    while GAME_ACTIVE:
        remaining = end_time - time.perf_counter()
        if remaining <= 0:
            break

        secs = int(remaining)
        millis = int((remaining - secs) * 1000)
        timer = f"BOMB TIMER: {secs:02d}.{millis:03d}"

        with lock:
            timer_win.erase()
            timer_win.addstr(0, 0, timer)
            timer_win.refresh()

        time.sleep(0.05)

    GAME_ACTIVE = False
    with lock:
        timer_win.erase()
        timer_win.addstr(0, 0, "00.000 - 💥 BOMB EXPLODED!")
        timer_win.refresh()


# ==============================
#        UPPGIFTER
# ==============================

def compare(correct, answer):
    global POINTS
    if correct == answer:
        POINTS += 1
        return True
    return False


def math_task(win):
    a = randint(1, 9)
    b = randint(1, 9)
    op = choice(["+", "-", "*"])
    correct = str(eval(f"{a}{op}{b}"))

    win.addstr(f"\nVad är {a} {op} {b}?: ")
    win.refresh()
    curses.echo()
    answer = win.getstr().decode("utf-8").strip()
    curses.noecho()

    return compare(correct, answer)


def symbol_task(win):
    symbols = ["×", "&", "^"]
    chosen = choice(symbols)
    symbolString = ""
    size = randint(10, 20)

    for x in range(size):
        symbolString += choice(symbols) + "    "
        if (x + 1) % 5 == 0:
            symbolString += "\n\n"

    correct = str(symbolString.count(chosen))
    win.addstr("\n\n" + symbolString)
    win.addstr(f"\nHur många {chosen} är det?: ")
    win.refresh()

    curses.echo()
    answer = win.getstr().decode("utf-8").strip()
    curses.noecho()

    return compare(correct, answer)


def getWord():
    try:
        url = "https://random-word-api.vercel.app/api?words=1&length=7"
        response = requests.get(url, timeout=3)
        retStr = str(response.json())
        return retStr[2:9]
    except:
        return "example"


def word_task(win):
    chosen = getWord()
    reverse = randint(0, 1)

    if reverse:
        win.addstr(f"\nSkriv ordet '{chosen}': ")
        correct = chosen
    else:
        win.addstr(f"\nSkriv ordet '{chosen}' BAKLÄNGES: ")
        correct = chosen[::-1]

    win.refresh()
    curses.echo()
    answer = win.getstr().decode("utf-8").strip()
    curses.noecho()

    return compare(correct, answer)


def alphabet_task(win):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ")
    letters = [choice(alphabet) for _ in range(3)]
    letters_str = "  ".join(letters)
    correct = min(letters, key=lambda l: alphabet.index(l))

    win.addstr(f"\nVilken av bokstäverna {letters_str} kommer först i alfabetet?: ")
    win.refresh()
    curses.echo()
    answer = win.getstr().decode("utf-8").strip().upper()
    curses.noecho()

    return compare(correct, answer)


TASK_FUNCTIONS = [math_task, word_task, symbol_task, alphabet_task]


# ==============================
#        TASK CONTROLLER
# ==============================
def taskController_curses(stdscr):
    """Visar uppgifter och kontrollerar resultat."""
    global GAME_ACTIVE, POINTS

    time.sleep(0.8)  # vänta lite så timern hinner starta

    with lock:
        task_win = curses.newwin(22, 100, 3, 0)
        task_win.scrollok(True)

    for i in range(TASKS_TO_SOLVE):
        if not GAME_ACTIVE:
            break

        with lock:
            task_win.erase()
            task_win.addstr(0, 0, f"Uppdrag {i + 1} av {TASKS_TO_SOLVE}\n")
            task_win.addstr(f"Poäng: {POINTS}\n")
            task_win.refresh()

        task = choice(TASK_FUNCTIONS)
        result = task(task_win)

        with lock:
            if result:
                task_win.addstr("\n✅ Rätt!\n")
            else:
                task_win.addstr("\n❌ Fel!\n")
            task_win.refresh()

        time.sleep(1)

    with lock:
        if GAME_ACTIVE and POINTS >= TASKS_TO_SOLVE:
            GAME_ACTIVE = False
            task_win.addstr("\n💥 Alla uppdrag klara! Bomben är desarmerad! 💣\n")
        elif GAME_ACTIVE:
            task_win.addstr("\n😬 Du hann inte klart innan bomben exploderade!\n")
        task_win.refresh()

    time.sleep(2)


# ==============================
#        MAIN
# ==============================
def main_curses(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    with lock:
        stdscr.addstr(2, 0, "💣 Välkommen till TimeBomb!")
        stdscr.addstr(3, 0, "Du har 20 sekunder på dig att lösa 5 uppdrag.")
        stdscr.addstr(4, 0, "Tryck Enter efter varje svar.")
        stdscr.refresh()

    time.sleep(1)

    t1 = threading.Thread(target=countdown_curses, args=(stdscr, 20,))
    t2 = threading.Thread(target=taskController_curses, args=(stdscr,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    with lock:
        stdscr.addstr(26, 0, "\nSpelet är slut. Tryck valfri tangent för att avsluta.")
        stdscr.refresh()

    stdscr.nodelay(False)
    stdscr.getch()


# ==============================
#        MENU
# ==============================
def menu():
    global GAME_ACTIVE, POINTS
    choice = input("Tryck 1 för att starta TimeBomb: ")
    if choice == "1":
        try:
            curses.wrapper(main_curses)
        except Exception as e:
            print(f"Ett fel uppstod: {e}", file=sys.stderr)

        GAME_ACTIVE = True
        POINTS = 0


if __name__ == "__main__":
    menu()
