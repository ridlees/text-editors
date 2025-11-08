import tkinter as tk
import random
import pygame
import threading
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load your boom sound file (make sure this file exists)
BOOM_SOUND = "boom.mp3"

# Define rainbow colors
RAINBOW_COLORS = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]

class BoomTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("💥 Boom Text Editor 💥")
        self.root.geometry("800x600")

        self.text = tk.Text(root, font=("Consolas", 16), wrap="word")
        self.text.pack(expand=True, fill="both")

        self.text.bind("<KeyPress>", self.on_key_press)

        # Center shaking back to original position
        self.normal_pos = (self.root.winfo_x(), self.root.winfo_y())

    def play_boom(self):
        threading.Thread(target=lambda: pygame.mixer.Sound(BOOM_SOUND).play()).start()

    def shake_window(self):
        def shake():
            x, y = self.root.winfo_x(), self.root.winfo_y()
            for _ in range(10):
                dx = random.randint(-10, 10)
                dy = random.randint(-10, 10)
                self.root.geometry(f"+{x+dx}+{y+dy}")
                time.sleep(0.02)
            self.root.geometry(f"+{x}+{y}")
        threading.Thread(target=shake).start()

    def explode_letter(self, event):
        x, y, _, _ = self.text.bbox("insert") or (0, 0, 0, 0)
        letter = event.char if event.char.strip() else ""
        if not letter:
            return

        label = tk.Label(self.text, text=letter, fg="red", font=("Consolas", 18, "bold"))
        self.text.window_create("insert", window=label)

        def animate():
            for i in range(len(RAINBOW_COLORS)):
                color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
                label.config(fg=color)
                label.place(x=x + random.randint(-10, 10), y=y + random.randint(-10, 10))
                time.sleep(0.05)
            label.destroy()

        threading.Thread(target=animate).start()

    def on_key_press(self, event):
        if event.keysym == "BackSpace":
            return
        self.play_boom()
        self.shake_window()
        self.explode_letter(event)


if __name__ == "__main__":
    root = tk.Tk()
    app = BoomTextEditor(root)
    root.mainloop()
