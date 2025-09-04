import unittest
import io
import csv
from scraper import generate_kw

class TestKWGenerator(unittest.TestCase):
    def test_calculate_control_digit(self):
        # sprawdzenie kilku numerów zgodnie z danymi z portalu
        numbers = ["00070392", "00070393", "00070394", "00070395"]
        expected_digits = ["3", "0", "7", "4"]
        for num, expected in zip(numbers, expected_digits):
            self.assertEqual(generate_kw.calculate_control_digit(num), expected)

    def test_generate_kw_rows(self):
        start_kw = "WA1G/00070392/3"
        rows = generate_kw.generate_kw(start_kw, 4)
        expected_rows = [
            ["WA1G", "00070392", "3"],
            ["WA1G", "00070393", "0"],
            ["WA1G", "00070394", "7"],
            ["WA1G", "00070395", "4"],
        ]
        self.assertEqual(rows, expected_rows)

    def test_save_to_csv(self):
        # użycie StringIO zamiast pliku
        output = io.StringIO()
        rows = [
            ["WA1G", "00070392", "3"],
            ["WA1G", "00070393", "0"],
        ]
        writer = csv.writer(output)
        writer.writerow(["kod", "number", "control_digit"])
        writer.writerows(rows)
        output.seek(0)
        content = output.read().strip().split("\n")
        expected_content = [
            "kod,number,control_digit",
            "WA1G,00070392,3",
            "WA1G,00070393,0",
        ]
        self.assertEqual(content, expected_content)

if __name__ == "__main__":
    unittest.main()
