"""Basic computer to lick detector arduino communication."""
import time

import numpy as np
import serial

# constants
LICK_DETECTOR_PORT = "/dev/ttyLick"
BAUDRATE = 115200
TIMEOUT = None

LEFT_CODE = "Z"
RIGHT_CODE = "Y"
CONFIRMATION_CODE = "D"


class BasicLickDetector:
    """Basic class to interact with lick detector arduino through a serial connection."""

    def __init__(self) -> None:
        self.serial_connection: serial.Serial = serial.Serial(
            port=LICK_DETECTOR_PORT,
            baudrate=BAUDRATE,
            timeout=TIMEOUT
        )
        print(f"Serial connection to lick detector {LICK_DETECTOR_PORT} established.")
        time.sleep(1)

    def set_threshold(self, threshold: int) -> None:
        """Set detection threshold (arbitrary value)."""
        message: str = f"IF{threshold}"
        self.send_message_to_arduino(message)

    def open_valve(self, side: str, seconds: float, verbose: bool = False) -> None:
        """Open valve connected to arduino for a some time."""
        short_side: str = "L" if side == "left" else "R"
        milliseconds: int = int(np.rint(seconds * 1000))
        message = f"IP{short_side}{milliseconds}"
        if verbose:
            print(f"Opening {side} valve for {seconds:.3f} seconds.")
        self.send_message_to_arduino(message)

    def send_message_to_arduino(self, message: str) -> None:
        """Send message to arduino."""
        message: bytes = message.encode()
        self.serial_connection.write(message)

    def read_message_from_arduino(self) -> str | None:
        """
        Read a message from arduino (if there is one).
        Clears the serial buffer completely.
        """
        n_bytes: int = self.serial_connection.in_waiting
        if n_bytes > 0:
            message: bytes = self.serial_connection.read(n_bytes)
            message: str = message.decode()
        else:
            message = None
        return message

    def check_lick(self) -> str | None:
        """Read arduino messages and check for lick message inside.

        Checks for Z (left) or Y (right) in message string.
        This is a very basic check.
        It does not take into account that a string might contain multiple messages.
        """
        message: str | None = self.read_message_from_arduino()
        if isinstance(message, str):
            if LEFT_CODE in message:
                lick_side = "left"
            elif RIGHT_CODE in message:
                lick_side = "right"
            else:
                lick_side = None
        else:
            lick_side = None
        return lick_side

    def check_confirmation(self) -> bool:
        """
        Check for 'D' in arduino message.
        Arduino is programmed to send 'D' after it received a command.
        """
        message: str | None = self.read_message_from_arduino()
        if isinstance(message, str):
            return "D" in message
        else:
            return False

    def close(self) -> None:
        self.serial_connection.close()
        print("Serial connection to lick detector closed.")

