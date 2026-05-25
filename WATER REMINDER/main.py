import time
from plyer import notification

while True:
    notification.notify(
        title="water reminder",
        message="DRINK WATER!!!!",
        timeout=10,
        app_icon = "water-glass-color-icon.ico"
    )
    time.sleep(3600) # 1 hour