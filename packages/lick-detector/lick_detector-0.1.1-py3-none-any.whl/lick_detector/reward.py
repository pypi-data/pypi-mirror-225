"""Lick detector with calibrated opening duration -> reward weight relationship."""

import datetime
import socket
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from lick_detector.base import BasicLickDetector
from lick_detector.files import find_most_recent_csv


class RewardLickDetector(BasicLickDetector):
    def __init__(self) -> None:
        super().__init__()

        self.is_calibrated_right = False
        self.is_calibrated_left = False
        self.right_model = None
        self.left_model = None

        self.model_order = 2

    def load_calibration(self, file_path: Path | None = None) -> None:
        if file_path is None:
            file_path = find_most_recent_csv()

        data = pd.read_csv(file_path)
        for side in ["left", "right"]:
            is_side = data["side"] == side
            if np.sum(is_side) > 0:
                list_of_seconds = data.loc[is_side, "duration_seconds"].values
                list_of_grams = data.loc[is_side, "weight_change_per_repeat_grams"].values
                model = self.fit_model(list_of_grams, list_of_seconds)
                print(f"{side.capitalize()} side calibrated.")
                if side == "left":
                    self.is_calibrated_left = True
                    self.left_model = model
                else:
                    self.is_calibrated_right = True
                    self.right_model = model
            else:
                print(f"No calibration for {side}!")

    def fit_model(self, list_of_grams: list, list_of_seconds: list) -> LinearRegression:
        weights = np.asarray(list_of_grams)
        durations = np.asarray(list_of_seconds)

        X = np.zeros((weights.size, self.model_order))
        for i in range(self.model_order):
            X[:, i] = weights ** (i + 1)
        y = durations
        model = LinearRegression()
        model.fit(X, y)
        return model

    def grams2seconds(self, side: str, grams: float) -> float:
        self.assert_calibration(side)

        X_pred = np.zeros((1, self.model_order))
        for i in range(self.model_order):
            X_pred[:, i] = grams ** (i + 1)
        if side == "left":
            seconds = self.left_model.predict(X_pred)
        elif side == "right":
            seconds = self.right_model.predict(X_pred)
        else:
            raise ValueError(f"{side=}")
        seconds = seconds[0]
        return seconds

    def assert_calibration(self, side: str) -> None:
        if side == "left":
            assert self.is_calibrated_left
        elif side == "right":
            assert self.is_calibrated_right
        else:
            raise ValueError(f"{side=}")

    def give_reward(self, side: str, grams: float, verbose: bool = False) -> None:
        self.assert_calibration(side)
        seconds = self.grams2seconds(side, grams)
        if verbose:
            print(f"{side}: {grams * 1000:.0f} mg -> {seconds * 1000:.0f} ms")
        self.open_valve(side, seconds, verbose)

    def collect_data(self, side: str, opening_durations: list, n_repeats: int) -> pd.DataFrame:
        starting_weight = self.ask_user_for_weight()
        print(f"Starting weight: {starting_weight:.1f} g")

        data = []
        last_weight = starting_weight
        for i_duration, duration in enumerate(opening_durations):
            self.ask_user_to_proceed()
            print(f"Duration: {duration * 1000:.0f} ms")

            for i_repeat in range(n_repeats):
                self.open_valve(side, duration)
                self.check_confirmation()
                time.sleep(0.1 + duration)

            new_weight = self.ask_user_for_weight()
            weight_change = new_weight - last_weight
            change_per_repeat = weight_change / n_repeats
            print(f"Change per repeat: {change_per_repeat * 1000:.1f} mg")
            results = {
                "datetime": datetime.datetime.now(),
                "i_duration": i_duration,
                "duration_seconds": duration,
                "weight_grams": new_weight,
                "weight_change_grams": weight_change,
                "weight_change_per_repeat_grams": change_per_repeat,
            }
            data.append(results)
            last_weight = new_weight

        data = pd.DataFrame(data)
        data["n_repeats"] = n_repeats
        data["side"] = side
        data["host"] = socket.gethostname()
        return data

    @staticmethod
    def ask_user_for_weight() -> float:
        while True:
            reply = input("Please input weight in grams: ")
            try:
                grams = float(reply)
                break
            except ValueError as e:
                print(f"Could not convert to float: {e}")
        return grams

    @staticmethod
    def ask_user_to_proceed() -> None:
        input("Press enter to proceed with next duration.")

