# Running the send_session_reminders task (Windows)

This project includes a small wrapper script `run_send_session_reminders.bat` in the project root to run the Django management command `send_session_reminders` safely from Task Scheduler.

What the batch does
- Changes to the project directory (`D:\P1`).
- If a virtualenv exists at `D:\P1\venv\Scripts\python.exe`, it runs that Python executable.
- Otherwise it falls back to the system `python` found in PATH.

Files added
- `run_send_session_reminders.bat` — wrapper script to run `manage.py send_session_reminders`.

How to use after pulling the repo

1. Ensure Python and dependencies

   - Recommended: create a virtual environment inside the project at `D:\P1\venv` and install requirements.

     PowerShell (from repository root):

     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```

   - Or ensure a global Python is installed and `manage.py` works with it.

2. Test the wrapper manually

   - From an elevated PowerShell or normal PowerShell (depending on your environment), run:

     ```powershell
     cd D:\P1
     .\run_send_session_reminders.bat
     ```

   - You should see console output from Django's management command. Any print() or logging in the command will appear in the console. Fix any errors before scheduling.

3. Create the scheduled task (example)

   - Schedule the wrapper to run daily at 11:00:

     ```powershell
     schtasks /Create /SC DAILY /TN "TutorFinder_Session_Reminders" /TR "D:\P1\run_send_session_reminders.bat" /ST 11:00 /F
     ```

   - To run the task as SYSTEM (no password) instead of your user, use `/RU "SYSTEM"`:

     ```powershell
     schtasks /Create /SC DAILY /TN "TutorFinder_Session_Reminders" /TR "D:\P1\run_send_session_reminders.bat" /ST 11:00 /RU "SYSTEM" /F
     ```

   - If you need to run as a specific user, add `/RU "DOMAIN\User" /RP "Password"` (note: storing passwords on the command line has security implications).

4. Test the scheduled task run

   - Run immediately:

     ```powershell
     schtasks /Run /TN "TutorFinder_Session_Reminders"
     ```

   - Check Task Scheduler History or logs for success/failure. Also check your Django logs or the database (Notification objects) to confirm reminders were sent.

Notes and troubleshooting
- If the scheduled task fails with environment errors, ensure the `venv` exists or the system Python has the required packages installed.
- If running as `SYSTEM`, the environment is very minimal — prefer running as a user that has the virtualenv available or use the absolute venv path.
- If you prefer not to store a venv inside the repo, update the batch to point to an absolute Python path.

If you want, I can also:
- Add logging (append stdout/stderr to a log file).
- Create a PowerShell wrapper instead of a .bat.
- Add a Git-tracked sample Task Scheduler XML export for easy import.
