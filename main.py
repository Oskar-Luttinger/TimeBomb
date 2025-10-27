import time

print("test")
def menu():
    choice = "empty string"
    print("Welcome to TimeBomb")
    print("This game will test your abillity to complete different task in a short amout of time ")
    print("Complete all task before the bomb explodes, GOOD LUCK!")
    choice = input("Enter 1 to start the game: ")
    if choice == "1":
        main()

def taskController():
    print("This is a task")
    pass

def countdown(seconds):
    total_time = float(seconds)
    interval = 0.01  # update every 10 ms

    while total_time > 0:
        secs = int(total_time)
        millis = int((total_time - secs) * 1000)
        timer = f"{secs:02d}.{millis:03d}"
        print(timer, end="\r")
        time.sleep(interval)
        total_time -= interval

    print("00.000\nTime’s up!")

def main():
    countdown(5)


menu()
