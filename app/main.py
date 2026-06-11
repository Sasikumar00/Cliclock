import threading
import os
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from alarm import Alarm
from alarm_scheduler import (
    alarm_scheduler,
    stop_alarm
)

console = Console()


def initialize_alarm_store():
    if not os.path.exists("alarms.json"):
        with open("alarms.json", "w") as f:
            json.dump([], f, indent=4)


def load_alarms():
    with open("alarms.json", "r") as f:
        return json.load(f)


def save_alarms(alarms):
    with open("alarms.json", "w") as f:
        json.dump(alarms, f, indent=4)


def display_alarms(alarms):
    if not alarms:
        console.print(
            "[bold yellow]⚠ No alarms found.[/bold yellow]"
        )
        return

    table = Table(title="⏰ Alarms")

    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Time", style="green")
    table.add_column("Label", style="yellow")
    table.add_column("Active", justify="center")
    table.add_column("Tune")

    for i, alarm in enumerate(alarms, 1):
        table.add_row(
            str(i),
            alarm["time"],
            alarm["label"],
            "✅" if alarm["active"] else "❌",
            alarm["tune_name"]
        )

    console.print(table)


def get_main_menu_options():
    console.print(
        Panel.fit(
            "[bold cyan]CLIClock[/bold cyan]\n\n"
            "[green]1.[/green] Set Alarm\n"
            "[green]2.[/green] Update Alarm\n"
            "[green]3.[/green] View Alarms\n"
            "[green]4.[/green] Delete Alarm\n"
            "[green]5.[/green] Stop Active Alarm\n"
            "[red]6.[/red] Exit",
            title="⏰ Main Menu",
            border_style="cyan"
        )
    )


def main():
    initialize_alarm_store()

    scheduler = threading.Thread(
        target=alarm_scheduler,
        daemon=True
    )
    scheduler.start()

    while True:
        get_main_menu_options()

        choice = Prompt.ask(
            "[bold cyan]Choose an option[/bold cyan]"
        )

        # CREATE ALARM
        if choice == "1":
            time = Prompt.ask(
                "[green]Enter alarm time (HH:MM)[/green]"
            )

            label = Prompt.ask(
                "[green]Enter alarm label[/green]"
            )

            alarm = Alarm(time, label)

            tune_option = Prompt.ask(
                "Custom tune? (y/n)",
                choices=["y", "n"],
                default="n"
            )

            if tune_option == "y":
                console.print("\n[bold]Available Tunes:[/bold]")

                for i, tune in enumerate(
                    alarm.get_tunes(),
                    1
                ):
                    console.print(
                        f"[cyan]{i}.[/cyan] {tune}"
                    )

                alarm.tune_name = Prompt.ask(
                    "Enter tune name"
                )

            alarms = load_alarms()

            alarms.append({
                "time": alarm.time,
                "label": alarm.label,
                "active": alarm.active,
                "tune_name": alarm.tune_name
            })

            save_alarms(alarms)

            console.print(
                "[bold green]✓ Alarm created successfully[/bold green]"
            )

        # UPDATE ALARM
        elif choice == "2":
            alarms = load_alarms()

            if not alarms:
                console.print(
                    "[bold yellow]⚠ No alarms to update[/bold yellow]"
                )
                continue

            display_alarms(alarms)

            alarm_id = int(
                Prompt.ask("Alarm ID")
            )

            if not (1 <= alarm_id <= len(alarms)):
                console.print(
                    "[bold red]✗ Invalid alarm ID[/bold red]"
                )
                continue

            selected_alarm = alarms[alarm_id - 1]

            new_time = Prompt.ask(
                "New time",
                default=selected_alarm["time"]
            )

            new_label = Prompt.ask(
                "New label",
                default=selected_alarm["label"]
            )

            tune_option = Prompt.ask(
                "Change tune? (y/n)",
                choices=["y", "n"],
                default="n"
            )

            tune_name = selected_alarm["tune_name"]

            if tune_option == "y":
                for i, tune in enumerate(
                    Alarm("", "").get_tunes(),
                    1
                ):
                    console.print(
                        f"[cyan]{i}.[/cyan] {tune}"
                    )

                tune_name = Prompt.ask(
                    "Enter tune name"
                )

            alarms[alarm_id - 1] = {
                "time": new_time,
                "label": new_label,
                "active": True,
                "tune_name": tune_name
            }

            save_alarms(alarms)

            console.print(
                "[bold green]✓ Alarm updated successfully[/bold green]"
            )

        # VIEW ALARMS
        elif choice == "3":
            alarms = load_alarms()
            display_alarms(alarms)

        # DELETE ALARM
        elif choice == "4":
            alarms = load_alarms()

            if not alarms:
                console.print(
                    "[bold yellow]⚠ No alarms to delete[/bold yellow]"
                )
                continue

            display_alarms(alarms)

            alarm_id = int(
                Prompt.ask("Alarm ID to delete")
            )

            if not (1 <= alarm_id <= len(alarms)):
                console.print(
                    "[bold red]✗ Invalid alarm ID[/bold red]"
                )
                continue

            deleted = alarms.pop(alarm_id - 1)

            save_alarms(alarms)

            console.print(
                f"[bold green]✓ Deleted:[/bold green] "
                f"{deleted['label']}"
            )

        # STOP ALARM
        elif choice == "5":
            if stop_alarm():
                console.print(
                    "[bold green]✓ Alarm stopped[/bold green]"
                )
            else:
                console.print(
                    "[bold yellow]⚠ No active alarm found[/bold yellow]"
                )

        # EXIT
        elif choice == "6":
            console.print(
                "[bold cyan]Goodbye! 👋[/bold cyan]"
            )
            break

        else:
            console.print(
                "[bold red]✗ Invalid choice[/bold red]"
            )


if __name__ == "__main__":
    main()