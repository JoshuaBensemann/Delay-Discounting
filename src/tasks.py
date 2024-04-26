import random
from typing import List


class DelayDiscountTask:
    def __init__(self, max_value: float, delay_range: List[str], max_trials: int):
        self.max_value = max_value
        self.delay_range = delay_range
        self.max_trials = max_trials

        self.log = []
        self.current_delay = None
        self.current_trial = None
        self._setup_trial_block()

        self.is_running = True

    def _setup_trial_block(self):
        if self.current_delay is None:
            self.current_delay = 0
        else:
            self.current_delay += 1

        if self.current_delay == len(self.delay_range):
            self.is_running = False
            print("Task complete")
            return False

        self.current_trial = 1
        self.current_trial_amount = self.max_value / 2
        self._randomise_display()
        return True

    def _setup_next_trial(self, chose_max):
        self.current_trial += 1
        adjust_amount = self.max_value * 2**-self.current_trial

        if chose_max:
            self.current_trial_amount = self.current_trial_amount + adjust_amount

        else:
            self.current_trial_amount = self.current_trial_amount - adjust_amount

        self._randomise_display()

    def _randomise_display(self):
        self.max_side = random.choice([1, 2])

    def get_trial(self):
        if self.max_side == 1:
            return (
                f"1: ${self.max_value:.2f} in {self.delay_range[self.current_delay]}",
                f"2: ${self.current_trial_amount:.2f} now",
            )

        return (
            f"1: ${self.current_trial_amount:.2f} now",
            f"2: ${self.max_value:.2f} in {self.delay_range[self.current_delay]}",
        )

    def record_response(self, response: int):
        if not self.is_running:
            return False

        valid_responses = [1, 2]
        if response not in valid_responses:
            return False

        chose_max = self.max_side == response
        self.log.append(
            {
                "trial": self.current_trial,
                "delay": self.delay_range[self.current_delay],
                "current_value": self.current_trial_amount,
                "max_value": self.max_value,
                "max_side": self.max_side,
                "response": response,
                "chose_max": chose_max,
            }
        )

        if self.current_trial == self.max_trials:
            self._setup_trial_block()
        else:
            self._setup_next_trial(chose_max)

        return True

    def get_log(self):
        return self.log

    def get_is_running(self):
        return self.is_running
