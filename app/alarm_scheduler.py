import threading
import time
from datetime import datetime
import json
import pygame

pygame.init()
pygame.mixer.init()

# Shared event used to stop currently playing alarms
stop_alarm_event = threading.Event()
alarm_active = False
triggered = set()

def play_tune(tune_name):
    global alarm_active

    pygame.mixer.music.load(f"tunes/{tune_name}")
    pygame.mixer.music.play(-1)  # loop forever

    start_time = time.time()

    while (
        time.time() - start_time < 60
        and not stop_alarm_event.is_set()
    ):
        time.sleep(0.1)

    pygame.mixer.music.stop()
    alarm_active = False


def stop_alarm():
    global alarm_active

    if not alarm_active:
        return False

    stop_alarm_event.set()
    pygame.mixer.music.stop()
    alarm_active = False

    return True

def trigger_alarm(alarm):
    global alarm_active

    alarm_active = True
    stop_alarm_event.clear()

    tune_thread = threading.Thread(
        target=play_tune,
        args=(alarm["tune_name"],),
        daemon=True
    )
    tune_thread.start()

    print("\n")
    print("=" * 40)
    print("🚨 ALARM 🚨")
    print(f"Label: {alarm['label']}")
    print(f"Time: {alarm['time']}")
    print("Select 'Stop Active Alarm' from the menu to stop it.")
    print("=" * 40)

    # Deactivate alarm after it fires
    with open("alarms.json", "r") as f:
        alarms = json.load(f)

    for a in alarms:
        if (
            a["time"] == alarm["time"]
            and a["label"] == alarm["label"]
        ):
            a["active"] = False
            break

    with open("alarms.json", "w") as f:
        json.dump(alarms, f, indent=4)


def alarm_scheduler():
    while True:
        try:
            with open("alarms.json", "r") as f:
                alarms = json.load(f)

            current_time = datetime.now().strftime("%H:%M")

            for alarm in alarms:
                alarm_key = f"{alarm['time']}-{alarm['label']}"

                if (
                    alarm["active"]
                    and alarm["time"] == current_time
                    and alarm_key not in triggered
                ):
                    triggered.add(alarm_key)
                    trigger_alarm(alarm)

            time.sleep(1)

        except (FileNotFoundError, json.JSONDecodeError):
            time.sleep(1)