# ⏰ Cliclock

A lightweight CLI-based alarm clock built with Python.

Cliclock allows users to create, manage, and trigger alarms directly from the terminal with support for custom labels, custom alarm tunes, and automatic alarm scheduling.

---

## Features

### Functional Requirements

* Create alarms with:

  * Trigger time
  * Custom label/tag
  * Custom ringtone
* View active and inactive alarms
* Update existing alarms
* Delete alarms
* Stop active alarms manually

### Non-Functional Requirements

* Automatically triggers alarms at the scheduled time
* Supports multiple alarms
* Background scheduler runs independently of the CLI menu
* Alarm audio automatically stops after 60 seconds if not dismissed
* Alarm state is persisted across application restarts

---

## Architecture

## Architecture

```text
                    ┌─────────────────┐
                    │     User        │
                    └────────┬────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │       Main Thread       │
                │                         │
                │  • Create Alarm         │
                │  • Update Alarm         │
                │  • View Alarms          │
                │  • Delete Alarm         │
                │  • Stop Active Alarm    │
                └───────────┬─────────────┘
                            │
                            │ Reads/Writes
                            ▼
                    ┌─────────────────┐
                    │   alarms.json   │
                    └────────┬────────┘
                             ▲
                             │
                             │ Reads
                             │
                ┌────────────┴────────────┐
                │    Scheduler Thread     │
                │                         │
                │  • Polls every second   │
                │  • Checks due alarms    │
                │  • Triggers alarms      │
                └────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │      Alarm Player       │
                │                         │
                │  • Plays ringtone       │
                │  • Loops audio          │
                │  • Auto stops (60s)     │
                │  • Manual stop support  │
                └─────────────────────────┘
```

### Components

| Component        | Responsibility                                           |
| ---------------- | -------------------------------------------------------- |
| Main Thread      | Handles user interaction and alarm management            |
| Scheduler Thread | Continuously checks for alarms that need to be triggered |
| Alarm Player     | Plays alarm tunes and manages alarm lifecycle            |
| Alarm Store      | Persists alarms to disk using JSON                       |

---

## Project Structure

```text
app/
├── main.py
├── alarm.py
├── alarm_scheduler.py
├── alarms.json
└── tunes/
    ├── miku.mp3
    └── rush.mp3
```

---

## Alarm Data Model

Each alarm is stored in `alarms.json`:

```json
{
  "time": "09:30",
  "label": "Team Catch-up",
  "active": true,
  "tune_name": "miku.mp3"
}
```

---

## Prerequisites

* Python 3.9+
* pip

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/<username>/cliclock.git
cd cliclock
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

### Activate the Virtual Environment

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```powershell
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install rich pygame
```

---

## Running the Application

```bash
python3 app/main.py
```

---

## Usage

### Create an Alarm

1. Select **Set Alarm**
2. Enter alarm time (`HH:MM`)
3. Enter a label
4. Optionally choose a custom ringtone

### View Alarms

Select **View Alarms** to display all configured alarms.

### Update an Alarm

Select **Update Alarm** and choose the alarm you wish to modify.

### Delete an Alarm

Select **Delete Alarm** and choose the alarm you wish to remove.

### Stop an Active Alarm

Select **Stop Active Alarm** while an alarm is ringing.

---

## Example

### Main Menu

```text
╭────────────── ⏰ Main Menu ──────────────╮
│ 1. Set Alarm                            │
│ 2. Update Alarm                         │
│ 3. View Alarms                          │
│ 4. Delete Alarm                         │
│ 5. Stop Active Alarm                    │
│ 6. Exit                                 │
╰─────────────────────────────────────────╯
```

### Alarm Triggered

```text
╭──────────────── ⏰ CLIClock ────────────────╮
│                                             │
│                 🚨 ALARM 🚨                 │
│                                             │
│               Team Catch-up                 │
│                                             │
│               Time: 09:30                   │
│                                             │
│      Menu Option 5 → Stop Active Alarm      │
│                                             │
╰─────────────────────────────────────────────╯
```