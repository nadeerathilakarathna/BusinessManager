import os
import pygetwindow as gw
import subprocess

class CurrentProcess:
    def get_current_running_software(self):
        try:
            active_window_title = gw.getActiveWindowTitle()
            return os.path.basename(active_window_title)
        except Exception as e:
            return str(e)

    def tasklist(self):
        running_tasks = []
        try:
            completed_process = subprocess.run(["tasklist"], capture_output=True, text=True, check=True,creationflags=subprocess.CREATE_NO_WINDOW)
            tasklist_output = completed_process.stdout
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            tasklist_output = ""

        # Split the tasklist output into lines and skip the header
        tasklist_lines = tasklist_output.split('\n')[3:]

        # Extract the process names
        running_tasks = []
        for line in tasklist_lines:
            if line.strip():
                process_name = line.split(".exe")[0]
                running_tasks.append(process_name+".exe")
        return running_tasks


    def isRunning(self):
        if not self.tasklist().count("Business Manager.exe") <=1:
            return True
        else:
            return False

