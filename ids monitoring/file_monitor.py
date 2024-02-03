import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
import os
import sys

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        modified_file = event.src_path
        file_name = os.path.basename(modified_file)

        notification_title = "File Modified Alert"
        notification_message = f"File '{file_name}' has been modified.\nPath: {modified_file}"

        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="FileMonitor",
            timeout=10
        )

def monitor_file(file_path):
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file_monitor.py <file_path>")
        sys.exit(1)

    file_to_monitor = sys.argv[1]
    
    if not os.path.isfile(file_to_monitor):
        print(f"Error: The specified file '{file_to_monitor}' does not exist.")
        sys.exit(1)

    monitor_file(file_to_monitor)
