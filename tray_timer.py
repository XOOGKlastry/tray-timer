"""Tray Timer - prosty minutnik w zasobniku systemowym Windows."""
import threading
import time
import tkinter as tk
from tkinter import simpledialog

import pystray
from PIL import Image, ImageDraw

try:
    import winsound
except ImportError:  # nie-Windows
    winsound = None

PRESETS = [5, 10, 15, 25, 45]


class TrayTimer:
    def __init__(self):
        self.total = 25 * 60
        self.remaining = self.total
        self.running = False
        self.lock = threading.Lock()
        self.icon = pystray.Icon("tray_timer", self.make_icon(), self.title(), self.build_menu())
        threading.Thread(target=self.tick, daemon=True).start()

    # --- ikona ---
    def make_icon(self, done=False):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        color = (220, 50, 50) if done else ((40, 170, 80) if self.running else (60, 120, 220))
        d.ellipse((4, 4, 60, 60), fill=color, outline="white", width=3)
        frac = self.remaining / self.total if self.total else 0
        d.pieslice((12, 12, 52, 52), -90, -90 + 360 * frac, fill="white")
        return img

    def fmt(self):
        m, s = divmod(int(self.remaining), 60)
        return f"{m:02d}:{s:02d}"

    def title(self):
        state = "" if self.running else " (pauza)"
        return f"Minutnik: {self.fmt()}{state}"

    def refresh(self, done=False):
        self.icon.icon = self.make_icon(done)
        self.icon.title = "Koniec!" if done else self.title()
        self.icon.update_menu()

    # --- logika ---
    def tick(self):
        while True:
            time.sleep(1)
            with self.lock:
                if not self.running:
                    continue
                self.remaining -= 1
                finished = self.remaining <= 0
                if finished:
                    self.remaining = 0
                    self.running = False
            if finished:
                self.finish()
            else:
                self.refresh()

    def finish(self):
        self.refresh(done=True)
        try:
            self.icon.notify("Czas minął!", "Minutnik")
        except Exception:
            pass
        if winsound:
            for _ in range(3):
                winsound.Beep(1000, 300)
                time.sleep(0.15)

    def set_minutes(self, minutes):
        with self.lock:
            self.total = self.remaining = int(minutes * 60)
            self.running = True
        self.refresh()

    def start(self, *_):
        with self.lock:
            if self.remaining <= 0:
                self.remaining = self.total
            self.running = True
        self.refresh()

    def pause(self, *_):
        with self.lock:
            self.running = False
        self.refresh()

    def reset(self, *_):
        with self.lock:
            self.running = False
            self.remaining = self.total
        self.refresh()

    def custom(self, *_):
        def ask():
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            val = simpledialog.askfloat("Minutnik", "Ile minut?", minvalue=0.1, maxvalue=1440, parent=root)
            root.destroy()
            if val:
                self.set_minutes(val)
        threading.Thread(target=ask, daemon=True).start()

    def quit(self, *_):
        self.icon.stop()

    def build_menu(self):
        Item = pystray.MenuItem
        presets = [Item(f"{m} min", (lambda m: lambda *_: self.set_minutes(m))(m)) for m in PRESETS]
        return pystray.Menu(
            Item(lambda _: f"Pozostało: {self.fmt()}", None, enabled=False),
            pystray.Menu.SEPARATOR,
            Item("Start", self.start, default=True, enabled=lambda _: not self.running),
            Item("Pauza", self.pause, enabled=lambda _: self.running),
            Item("Reset", self.reset),
            Item("Ustaw czas", pystray.Menu(*presets, pystray.Menu.SEPARATOR, Item("Własny...", self.custom))),
            pystray.Menu.SEPARATOR,
            Item("Wyjdź", self.quit),
        )

    def run(self):
        self.icon.run()


if __name__ == "__main__":
    TrayTimer().run()
