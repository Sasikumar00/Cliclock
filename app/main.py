from alarm import Alarm
from alarm_scheduler import (
    alarm_scheduler,
    stop_alarm
)
import threading
import os
import json

def initialize_alarm_store():
    if not os.path.exists("alarms.json"):
        with open("alarms.json", "w") as f:
            json.dump([], f)

def get_main_menu_options():
    print("Menu Options:")
    print("1. Set Alarm")
    print("2. Update Alarm")
    print("3. View Alarms")
    print("4. Delete Alarm")
    print("5. Stop Active Alarm")
    print("6. Exit")

def main():

    initialize_alarm_store()

    scheduler = threading.Thread(
    target=alarm_scheduler,
    daemon=True
    )

    scheduler.start()
    while True:
        get_main_menu_options()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            time = input("Enter alarm time (HH:MM): ")
            label = input("Enter alarm label: ")
            alarm = Alarm(time, label)
            tune_option = input("Do you want to set a custom tune? (y/n): ")
            tune = None
            if tune_option.lower() == 'y':
                tunes = alarm.get_tunes()
                print("Available tunes:")
                for i, t in enumerate(tunes, 1):
                    print(f"{i}. {t}")
                tune = input("Enter alarm tune (e.g., miku.mp3): ")

            # Save the alarm to the JSON file, creating the file if it doesn't exist
            with open(alarm.alarm_store, 'r') as f:
                alarms = json.load(f)
            alarms.append({
                "time": alarm.time,
                "label": alarm.label,
                "active": alarm.active,
                "tune_name": alarm.tune_name
            })
            with open(alarm.alarm_store, 'w') as f:
                json.dump(alarms, f, indent=4)

        elif choice == '2':
            # Load existing alarms
            with open("alarms.json", 'r') as f:
                alarms = json.load(f)
            if not alarms:
                print("---------- No alarms to update. ----------")
                continue
            print("Existing Alarms:")
            for i, a in enumerate(alarms, 1):
                print(f"{i}. {a['time']} - {a['label']} (Active: {a['active']}, Tune: {a['tune_name']})")

            alarm_id = int(input("Enter alarm ID to update: "))
            new_time = input("Enter new alarm time, press Enter to keep current (HH:MM): ")
            new_label = input("Enter new alarm label, press Enter to keep current: ")
            if new_label == "":
                new_label = alarms[alarm_id - 1]['label']
            if new_time == "":
                new_time = alarms[alarm_id - 1]['time']
            tune_option = input("Do you want to set a custom tune? (y/n): ")
            tune = None
            if tune_option.lower() == 'y':
                tunes = alarm.get_tunes()
                print("Available tunes:")
                for i, t in enumerate(tunes, 1):
                    print(f"{i}. {t}")
                new_tune = input("Enter alarm tune (e.g., miku.mp3): ")

            # Save the updated alarm to the JSON file
            alarms[alarm_id - 1] = {
                "time": new_time,
                "label": new_label,
                "active": True,
                "tune_name": new_tune if tune_option.lower() == 'y' else alarms[alarm_id - 1]['tune_name']  # Update tune if changed
            }
            with open("alarms.json", 'w') as f:
                json.dump(alarms, f, indent=4)

        elif choice == '3':
            # Load existing alarms            
            with open("alarms.json", 'r') as f:
                alarms = json.load(f)
            if not alarms:
                print("---------- No alarms set. ----------")
            else:
                print("Existing Alarms:")
                for i, a in enumerate(alarms, 1):
                    print(f"{i}. {a['time']} - {a['label']} (Active: {a['active']}, Tune: {a['tune_name']})")
        elif choice == '4':
            # Load existing alarms
            with open("alarms.json", 'r') as f:
                alarms = json.load(f)
            if not alarms:
                print("---------- No alarms set. ----------")
            else:
                print("Existing Alarms:")
                for i, a in enumerate(alarms, 1):
                    print(f"{i}. {a['time']} - {a['label']} (Active: {a['active']}, Tune: {a['tune_name']})")
                alarm_id = int(input("Enter alarm ID to delete: "))
                if 1 <= alarm_id <= len(alarms):
                    del alarms[alarm_id - 1]
                    with open("alarms.json", 'w') as f:
                        json.dump(alarms, f, indent=4)
                    print("---------- Alarm deleted. ----------")
                else:
                    print("---------- Invalid alarm ID. ----------")
        elif choice == '5':
            if stop_alarm():
                print("---------- Alarm stopped. ----------")
            else:
                print("---------- No active alarm found. ----------")
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("---------- Invalid choice. Please try again. ----------")

if __name__ == "__main__":
    main()