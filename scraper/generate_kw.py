import csv
import sys
from typing import List

def calculate_control_digit(number: str) -> str:
    """
    Calculate correct Polish KW control digit for 8-digit number.
    """
    # wagi dla cyfr numeru KW
    weights = [7, 3, 1, 7, 3, 1, 7, 3]
    digits = [int(d) for d in number]
    total = sum(d * w for d, w in zip(digits, weights))
    control_digit = total % 10
    return str(control_digit)

def generate_kw(start_kw: str, count: int) -> List[List[str]]:
    """
    Generate KW numbers [kod, number, control_digit], first KW kept as-is.
    """
    kod, number, control_digit = start_kw.split("/")
    start_int = int(number)
    rows = [[kod, number, control_digit]]  # zachowujemy startowe KW

    for i in range(1, count):
        number_i = str(start_int + i).zfill(8)
        control_digit_i = calculate_control_digit(number_i)
        rows.append([kod, number_i, control_digit_i])

    return rows

def save_to_csv(filename: str, rows: List[List[str]]) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["kod", "number", "control_digit"])
        writer.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_kw.py <start_kw> <count>")
        sys.exit(1)

    start_kw = sys.argv[1]
    count = int(sys.argv[2])
    output_file = "input_kw.csv"

    rows = generate_kw(start_kw, count)
    save_to_csv(output_file, rows)

    print(f"Generated {count} KW numbers starting from {start_kw}")
    print(f"Saved to {output_file}")
