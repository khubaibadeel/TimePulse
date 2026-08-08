# Project Instructions: AlarmApp 

This file contains foundational mandates, architectural patterns, and workflows for the AlarmApp project.

## Project Overview
- **Type:** Desktop Alarm Application.
- **Primary Language:** Python 3.
- **Supported Platform:** Windows only.
- **Technology Stack:**
  - GUI: `customtkinter` (Modern UI for Tkinter).
  - System Tray: `pystray` and `Pillow`.
  - Data Storage: JSON (`alarms.json`).
  - System Integration: WinMM MCI audio via `ctypes`, `winsound.Beep` fallback, a per-user Windows named mutex, Startup-folder autostart, and workstation locking.
  - Executable: Windowed one-file `Alarm.exe`, built by PyInstaller using `Alarm.spec`.

## Key Features
- **Modern UI:** Styled with light/dark mode support and custom color palettes.
- **Alarm Management:** Create, update, toggle, and delete alarms with optional labels. Includes integrated **Quick Timers**.
- **Snooze Functionality:** Postpone alarms by 3 minutes without completing them.
- **Repeat Scheduling:** The alarm engine supports daily, weekly, and monthly next-occurrence scheduling.
- **Live Dashboard:** Real-time clock and countdown for the next alarm.
- **Detailed History Log:** Event logging for creation, edits, toggles, triggers, snoozes, dismissals, locks, and missed alarms.
- **Tray Integration:** Minimized-to-tray with time-until-next-alarm tooltip.
- **Security Model:** Optional salted PBKDF2-HMAC-SHA256 password protection for edit, toggle, and delete actions, with automatic migration of verified legacy SHA-256 hashes.
- **Auto-start:** Uses a per-user Windows Startup-folder command file that launches KRONOS normally at sign-in.
- **Automated Actions:** Locks the Windows workstation when an alarm is dismissed or reaches its 30-second auto-lock timeout.
- **Data Persistence:** UTF-8 JSON saved through a temporary file and `os.replace()`, with backup and corruption-recovery behavior.

## Architecture & Logic
- **Main Class:** `AlarmApp` (inherits from `ctk.CTk`).
- **Single Instance:** A per-user, session-local Windows named mutex rejects a second KRONOS process before the UI starts.
- **Concurrency:** The tray and emergency beep fallback use daemon threads; alarm checks run every second through Tk's `after()` loop.
- **Thread Safety:** 
  - Tray-triggered window updates are scheduled through `self.after()`.
  - Shared data (`self.data`) is protected by `threading.Lock`.
- **Alarm Checker:** Polling-based at one-second intervals. Active alarm IDs prevent duplicate popups while an alarm is already being handled.
- **Past Alarms:** During load, enabled past one-time alarms are retained, marked `missed`, disabled, logged, and saved. Repeating alarms are not changed by this cleanup.
- **Data Model:** Alarms are dictionaries in a list, stored in `alarms.json`.

## Ringtone Settings & Customization
- **Ringtone Selection:** Users can choose a specific ringtone for each alarm in both the **Create Alarm** and **Edit Alarm** forms.
- **Ringtone Discovery:** Available ringtones are discovered in this order: an external `ringtones` folder beside `Alarm.exe`, bundled PyInstaller ringtones under `sys._MEIPASS`, then the source `ringtones` folder. Valid ringtone files must be plain `.wav` filenames.
- **Friendly Display Names:** The drop-down displays friendly names for each ringtone by removing the `.wav` extension and replacing underscores with spaces.
- **Hover Preview:** Hovering over a ringtone option in the dropdown initiates a short 4-second preview after a delay. Moving the pointer to a different option stops the previous preview immediately and starts the new one. Previews stop when leaving the dropdown area, closing the form, on alarm trigger, or on Windows session lock.
- **Auto-Cancellation & Delay:** To prevent noise, a 250ms hover delay is applied before starting audio. Outdated preview requests are canceled immediately.
- **Data Persistence:** The chosen ringtone file name is saved in `alarms.json` as the `ringtone` field (e.g., `"Soft_Arrival.wav"`) when alarms are created or edited. Legacy alarms without this field use an in-memory default fallback and are not rewritten merely to add the field.
- **Default Fallback:** Legacy alarms and missing selections fall back in memory to `Soft_Arrival.wav`. If WAV playback fails completely, the alarm falls back to a stoppable `winsound.Beep` sequence.
- **Session-Lock Behavior:** Real-time Windows session lock events are monitored using native APIs (`WTSRegisterSessionNotification` plus a subclassed WndProc). If Windows is locked while an alarm is ringing or a preview is playing, all audio is stopped immediately, and the audio does not resume automatically upon unlocking.
- **Executable Packaging:** The `Alarm.spec` file packages the `ringtones` directory into the final PyInstaller output. Runtime lookup still prefers an external `ringtones` folder beside the executable, allowing users to add or replace WAV files after packaging.

## Conventions & Standards
- **Naming:** Follow PEP 8 (snake_case for functions/variables, PascalCase for classes).
- **UI Consistency:** Use predefined color constants in `Alarm.py`.
- **Validation:** Always validate JSON data on load; provide fallback for corrupt files.

## Known Limitations
- **Windows Only:** The app depends on WinMM MCI audio, `winsound.Beep` fallback, `rundll32.exe`, the Windows Startup folder, WTS session notifications, and Win32 mutex APIs.
- **Sleep Mode:** The app does not wake the computer. An alarm may be delayed until resume; stale one-time alarms found during a later startup are marked missed.
- **Storage Location:** In a frozen build, JSON data and alarm history are stored beside `Alarm.exe`, so that directory must be writable.

## Workflows
- **Install Dependencies:** `python -m pip install -r requirements.txt`
- **Build:** `pyinstaller Alarm.spec`
- **Build Output:** `dist/Alarm.exe` (windowed one-file executable).
- **Local Run:** `python Alarm.py`

`Alarm.spec` resolves project files relative to the spec location, collects CustomTkinter package assets through PyInstaller, and bundles `newico.ico` for both runtime use and the executable icon.
