from codecarbon import EmissionsTracker
from time import sleep

tracker = EmissionsTracker(project_name="Test", tracking_mode="machine", save_to_logger=True, output_file="emissions.csv")

tracker.start()
while True:
    sleep(10)
    tracker.flush()

tracker.stop()