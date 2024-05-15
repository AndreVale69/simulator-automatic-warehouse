from unittest import TestCase
from src.sim.__main__ import run_simulator


class TestMain(TestCase):
    def test_main(self):
        self.assertIsNone(run_simulator())