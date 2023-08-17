import unittest
import concurrent.futures
from bloonspy import Client, ChallengeFilter


class TestRateLimit(unittest.TestCase):
    def test_rate_limit(self) -> None:
        """
        Tests if the rate limit is handled correctly.
        """
        challenges = []
        challenges += Client.challenges(ChallengeFilter.NEWEST, pages=2)
        challenges += Client.challenges(ChallengeFilter.TRENDING, pages=2)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for challenge in challenges:
                futures.append(executor.submit(challenge.creator))
                futures.append(executor.submit(challenge.load_resource))
            concurrent.futures.wait(futures)

    def test_mics(self) -> None:
        challenges = Client.challenges(ChallengeFilter.NEWEST)
        print(challenges[0].creator())
