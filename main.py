import time

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


countdown(5)

