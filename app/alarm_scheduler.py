import threading
import time
from datetime import datetime
import json

import pygame
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

pygame.init()
pygame.mixer.init()

console = Console()

# Shared state
stop_alarm_event = threading.Event()
alarm_active = False
triggered = set()


def deactivate_alarm(alarm):
    try:
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

    except Exception:
        pass


def play_tune(alarm):
    global alarm_active

    pygame.mixer.music.load(
        f"tunes/{alarm['tune_name']}"
    )

    pygame.mixer.music.play(-1)

    start_time = time.time()

    while (
        time.time() - start_time < 60
        and not stop_alarm_event.is_set()
    ):
        time.sleep(0.1)

    pygame.mixer.music.stop()

    alarm_active = False

    deactivate_alarm(alarm)


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
        args=(alarm,),
        daemon=True
    )

    tune_thread.start()

    console.print()

    console.print(
        Panel(
            Align.center(
                f"[bold red]🚨 ALARM 🚨[/bold red]\n\n"
                f"[bold yellow]{alarm['label']}[/bold yellow]\n\n"
                f"[green]Time:[/green] {alarm['time']}\n\n"
                f"[cyan]Menu Option 5 → Stop Active Alarm[/cyan]"
            ),
            title="⏰ CLIClock",
            border_style="bright_red",
            padding=(1, 4)
        )
    )


def alarm_scheduler():
    while True:
        try:
            with open("alarms.json", "r") as f:
                alarms = json.load(f)

            current_time = datetime.now().strftime("%H:%M")

            for alarm in alarms:
                alarm_key = (
                    f"{alarm['time']}-"
                    f"{alarm['label']}"
                )

                if (
                    alarm["active"]
                    and alarm["time"] == current_time
                    and alarm_key not in triggered
                ):
                    triggered.add(alarm_key)
                    trigger_alarm(alarm)

            time.sleep(1)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            time.sleep(1)