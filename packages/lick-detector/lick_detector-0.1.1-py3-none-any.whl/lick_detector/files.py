import datetime
import os
from pathlib import Path

import numpy as np


def find_most_recent_csv() -> Path:
    folder = get_path_to_data()
    contents = folder.iterdir()

    dates = []
    files = []
    for element in contents:
        if element.suffix == ".csv":
            date = element.stem
            dates.append(date)
            files.append(element)
    print(f"{len(files)} calibration files found in {folder}")
    if len(files) < 1:
        raise FileNotFoundError(f"No calibration files in {folder}")
    dates = [datetime.datetime.strptime(x, "%Y-%m-%d").date() for x in dates]
    latest_date = np.max(dates)
    print(f"Latest calibration date: {latest_date}")
    i_latest = np.argmax(dates)
    path_to_csv = files[i_latest]
    return path_to_csv


def get_path_to_data() -> Path:
    path_to_data = Path.home() / "lick_detector_data"
    if not path_to_data.is_dir():
        os.makedirs(path_to_data)
        print(f"{path_to_data} created.")
    return path_to_data


if __name__ == "__main__":
    print(find_most_recent_csv())