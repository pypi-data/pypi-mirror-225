"""A GUI to control the lick detector."""
import datetime
import tkinter as tk
from functools import partialmethod

from lick_detector.reward import RewardLickDetector


OPENING_TIME = 0.25
WAITING_TIME = 0.15


class LickDetectorGui:
    """GUI to control lick detector directly."""
    def __init__(self, lick_detector: RewardLickDetector, detect_licks: bool = True) -> None:
        self.lick_detector = lick_detector
        self.detect_licks = detect_licks

        self.window: tk.Tk = tk.Tk()
        self.window.title("Lick Detector")

        self.variables = {}
        self.gui_elements = {}

        self.continue_loop = True

    def run(self) -> None:
        """Main method to call."""
        self.set_up()
        self.window.after(ms=10, func=self.update)
        self.window.mainloop()

    def set_up(self) -> None:
        """Prepare various gui elements."""
        self.set_up_threshold()
        self.set_up_single()
        self.set_up_continuous()
        self.set_up_reward()
        if self.detect_licks:
            self.set_up_licks()

    def set_up_threshold(self) -> None:
        frame = tk.LabelFrame(self.window, text="Threshold")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=1, uniform="a")

        label = tk.Label(frame, text="Threshold (a.u.)")
        label.grid(row=0, column=0, sticky="NEWS")
        variable = tk.IntVar()
        variable.set(100)
        self.variables["threshold"] = variable
        entry = tk.Entry(frame, textvariable=variable)
        entry.grid(row=0, column=1, sticky="NEWS")

        button = tk.Button(frame, text="Set threshold", command=self.set_threshold)
        button.grid(row=1, column=0, columnspan=2, sticky="NEWS")

    def set_threshold(self) -> None:
        threshold = self.variables["threshold"].get()
        print(f"{datetime.datetime.now()}: Setting threshold: {threshold}")
        self.lick_detector.set_threshold(threshold)

    def set_up_single(self) -> None:
        """Set up GUI elements for single valve openings"""
        frame = tk.LabelFrame(self.window, text="Single")
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=1, uniform="a")

        label = tk.Label(frame, text="Duration (s)")
        label.grid(row=0, column=0, sticky="NEWS")

        variable = tk.DoubleVar()
        variable.set(0.5)
        self.variables["duration"] = variable
        entry = tk.Entry(frame, textvariable=variable)
        entry.grid(row=0, column=1, sticky="NEWS")

        button = tk.Button(frame, text="Left", command=self.open_left_valve)
        button.grid(row=1, column=0, sticky="NEWS")
        self.gui_elements["single_left"] = button

        button = tk.Button(frame, text="Right", command=self.open_right_valve)
        button.grid(row=1, column=1, sticky="NEWS")
        self.gui_elements["single_right"] = button

    def set_up_continuous(self) -> None:
        """Set up GUI elements for continuous valve opening"""
        frame = tk.LabelFrame(self.window, text="Continuous")
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=1, uniform="a")

        button = tk.Button(frame, text="Open left", command=self.initiate_left)
        button.grid(row=0, column=0, sticky="NEWS")
        self.gui_elements["continuous_left"] = button

        button = tk.Button(frame, text="Open right", command=self.initiate_right)
        button.grid(row=0, column=1, sticky="NEWS")
        self.gui_elements["continuous_right"] = button

        button = tk.Button(frame, text="Close", command=self.close_valves)
        button.grid(row=1, column=0, columnspan=2, sticky="NEWS")
        button.config(state="disabled")
        self.gui_elements["continuous_close"] = button

    def set_up_licks(self) -> None:
        """Set up GUI elements for logging licks."""
        frame = tk.LabelFrame(self.window, text="Licks")
        frame.pack(fill="both", expand=True)

        text = tk.Text(frame, height=10)
        text.pack(fill="both", expand=True)
        text.config(state="disabled")
        self.gui_elements["lick"] = text

    def set_up_reward(self) -> None:
        """Set up GUI elements for giving rewards."""
        frame = tk.LabelFrame(self.window, text="Reward")
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=1, uniform="a")
        frame.columnconfigure(1, weight=1, uniform="a")

        label = tk.Label(frame, text="Amount (mg)")
        label.grid(row=0, column=0, sticky="NEWS")

        variable = tk.IntVar()
        variable.set(10)
        self.variables["amount"] = variable
        entry = tk.Entry(frame, textvariable=variable)
        entry.grid(row=0, column=1, sticky="NEWS")

        button = tk.Button(frame, text="Left", command=self.give_left_reward)
        button.grid(row=1, column=0, sticky="NEWS")
        self.gui_elements["reward_left"] = button
        if not self.lick_detector.is_calibrated_left:
            button.config(state=tk.DISABLED)

        button = tk.Button(frame, text="Right", command=self.give_right_reward)
        button.grid(row=1, column=1, sticky="NEWS")
        self.gui_elements["reward_right"] = button
        if not self.lick_detector.is_calibrated_right:
            button.config(state=tk.DISABLED)

    def give_reward(self, side: str) -> None:
        milligrams = self.variables["amount"].get()
        grams = milligrams / 1000
        print(f"{datetime.datetime.now()}: {side} -> {milligrams:.0f} mg")
        self.lick_detector.give_reward(side, grams, verbose=True)

    def open_valve(self, side: str) -> None:
        duration = self.variables["duration"].get()
        print(f"{datetime.datetime.now()}: {side} -> {duration:.3f}s")
        self.lick_detector.open_valve(side, duration)

    def initiate_continuous_opening(self, side: str) -> None:
        self.continue_loop = True
        self.gui_elements["continuous_close"].config(state="normal")
        for name in ["continuous_right", "continuous_left", "single_right", "single_left"]:
            self.gui_elements[name].config(state="disabled")
        print(f"{datetime.datetime.now()}: {side} opened.")
        self.open_continuously(side)

    def open_continuously(self, side: str) -> None:
        if self.continue_loop:
            self.lick_detector.open_valve(side, OPENING_TIME)
            self.window.after(int(OPENING_TIME * 1000), self.open_continuously, side)
        else:
            print(f"{datetime.datetime.now()}: {side} closed.")

    def close_valves(self) -> None:
        self.continue_loop = False
        self.gui_elements["continuous_close"].config(state="disabled")
        for name in ["continuous_right", "continuous_left", "single_right", "single_left"]:
            self.gui_elements[name].config(state="normal")

    def update(self) -> None:
        if self.detect_licks:
            lick_side = self.lick_detector.check_lick()
            if lick_side:
                time_string = datetime.datetime.now().strftime("%H:%M:%S,%f")
                line = f"{time_string} - {lick_side}"
                self.gui_elements["lick"].config(state="normal")
                self.gui_elements["lick"].insert("1.0", f"{line}\n")
                self.gui_elements["lick"].config(state="disabled")
            self.window.after(10, self.update)

    # partialmethods
    initiate_right = partialmethod(initiate_continuous_opening, "right")
    initiate_left = partialmethod(initiate_continuous_opening, "left")
    open_right_valve = partialmethod(open_valve, "right")
    open_left_valve = partialmethod(open_valve, "left")
    give_right_reward = partialmethod(give_reward, "right")
    give_left_reward = partialmethod(give_reward, "left")
