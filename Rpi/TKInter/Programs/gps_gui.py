from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
import tkinter as tk
from tkinter import ttk
import time
import sys

class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker")
        self.root.geometry("400x200")

        # Labels to display GPS data
        self.lat_label = ttk.Label(root, text="Latitude: N/A")
        self.lat_label.pack(pady=10)
        self.lon_label = ttk.Label(root, text="Longitude: N/A")
        self.lon_label.pack(pady=10)
        self.alt_label = ttk.Label(root, text="Altitude: N/A")
        self.alt_label.pack(pady=10)
        self.status_label = ttk.Label(root, text="Status: Connecting to gpsd...")
        self.status_label.pack(pady=10)

        # Connect to gpsd
        try:
            self.session = gps(host="localhost", port="2947", mode=WATCH_ENABLE | WATCH_NEWSTYLE)
            self.status_label.config(text="Status: Connected to gpsd")
        except ConnectionRefusedError:
            self.status_label.config(text="Status: Failed to connect to gpsd")
            sys.exit(1)
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {e}")
            sys.exit(1)

        # Start updating GPS data
        self.update_gps()

    def update_gps(self):
        try:
            report = self.session.next()
            if report.get('class') == 'TPV':
                latitude = getattr(report, 'lat', 'N/A')
                longitude = getattr(report, 'lon', 'N/A')
                altitude = getattr(report, 'alt', 'N/A')
                self.lat_label.config(text=f"Latitude: {latitude}")
                self.lon_label.config(text=f"Longitude: {longitude}")
                self.alt_label.config(text=f"Altitude: {altitude} m")
            elif report.get('class') == 'ERROR':
                self.status_label.config(text=f"Status: GPSD Error - {report.get('message', 'Unknown error')}")
        except StopIteration:
            self.status_label.config(text="Status: GPSD stopped")
            return
        except Exception as e:
            self.status_label.config(text=f"Status: Error - {e}")
        # Schedule next update
        self.root.after(1000, self.update_gps)

if __name__ == "__main__":
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()
