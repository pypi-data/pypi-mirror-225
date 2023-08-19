""" import modules """
import math
import time
DEFAULT_BACKOFF_MAX_RETRIES = 5
BASE_DELAY_MS = 1000

class MaxRetriesExceededError(Exception):
    """ max retry exceeded class """
    def __init__(self, max_retries):
        self.max_retries = max_retries
        super().__init__(f"Max retries ({max_retries}) exceeded.")

class ExponentialBackoff:
    """ exponential backoff class """
    retry_count = 1
    max_retries = DEFAULT_BACKOFF_MAX_RETRIES

    def __init__(self, max_retries = DEFAULT_BACKOFF_MAX_RETRIES):
        self.max_retries = max_retries

    def back_off(self):
        """ back off function """
        if self.retry_count >= self.max_retries:
            raise MaxRetriesExceededError(self.max_retries)

        self.retry_count += 1
        delay_ms = math.pow(2, self.retry_count) * BASE_DELAY_MS / 1000
        return time.sleep(delay_ms)

    def set_num_attempts(self, retry_count: int):
        """ num of attempts """
        self.retry_count = retry_count
