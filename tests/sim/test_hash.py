from unittest import TestCase


class TestHash(TestCase):
    # to check the list of prime numbers: https://www.math.uchicago.edu/~luis/allprimes.html
    def setUp(self):
        self.prime_numbers = {
            'Warehouse': 32831,
            'EmptyEntry': 18341,
            'TrayEntry': 17581,
            'TrayContainer': 16963,
            'Column': 15199,
            'Carousel': 14951,
            'Material': 13463,
            'Tray': 12637,
            'Entry': 11497
        }
        self.prime_numbers_values = list(self.prime_numbers.values())

    def test_prime_numbers_hash(self):
        # confirm that there are no duplicates
        self.assertEqual(len(self.prime_numbers), len(set(self.prime_numbers_values)))

        for _, prime_number in self.prime_numbers.items():
            for val in self.prime_numbers_values:
                if (prime_number ^ val) in self.prime_numbers_values:
                    self.assertTrue(
                        False,
                        f"Two bitwise or between two primes gives another prime used: "
                        f"{prime_number} and {val} -> {prime_number ^ val}"
                    )

        self.assertTrue(True)
