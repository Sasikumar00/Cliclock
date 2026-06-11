import json

class Alarm:
    def __init__(self, time, label):
        self.time = time
        self.label = label
        self.active = True
        self.tune_name = "miku.mp3"
        self.alarm_store = "alarms.json"


    def set_time(self, time):
        self.time = time

    def set_label(self, label):
        self.label = label

    def set_active(self, active):
        self.active = active

    def set_tune(self, tune_name):
        self.tune_name = tune_name

    def get_tunes(self):
        return ["rush.mp3", "miku.mp3"]

    def __str__(self):
        return f"Alarm set for {self.time} with label '{self.label}' and tune '{self.tune_name}'"