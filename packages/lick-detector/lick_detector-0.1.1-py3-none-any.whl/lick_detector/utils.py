import datetime

from lick_detector.reward import RewardLickDetector


class LickReward:
    def __init__(
            self,
            lick_detector: RewardLickDetector,
            reward_size_mg: int,
            fallback_duration_seconds: float = 0.05,
    ) -> None:
        self.reward_size = reward_size_mg
        self.fallback_duration = fallback_duration_seconds
        self.lick_detector = lick_detector
        self.total_reward: float = 0

    def run(self) -> None:
        while True:
            lick_side = self.lick_detector.check_lick()
            if lick_side == "right":
                print(f"{datetime.datetime.now()} - Lick {lick_side}")
                if self.lick_detector.is_calibrated_right:
                    grams = self.reward_size / 1000
                    self.lick_detector.give_reward("right", grams)
                    self.total_reward += grams
                    print(f"{datetime.datetime.now()} - Total reward: {self.total_reward * 1000:.0f} mg")
                else:
                    self.lick_detector.open_valve("right", self.fallback_duration)
