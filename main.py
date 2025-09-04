import csv
import sys
import os
import time
from tqdm import tqdm
from datetime import datetime
from scraper.parcel import get_parcel_data


def main(input_file="input_kw.csv", output_file="output_kw.csv"):
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    os.makedirs("output", exist_ok=True)

    output_path = os.path.join("output", output_file)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "kod",
            "number",
            "control_digit",
            "typ_ksiegi",
            "polozenie",
            "wlasciciel",
            "parcel_number",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # progress bar
        for row in tqdm(rows, desc="Processing KW", unit="KW"):
            kod, number, control_digit = (
                row["kod"],
                row["number"],
                row["control_digit"],
            )
            try:
                data = get_parcel_data(kod, number, control_digit)
            except Exception as e:
                tqdm.write(f"{kod}-{number}-{control_digit} -> ERROR: {e}")
                data = {
                    "typ_ksiegi": None,
                    "polozenie": None,
                    "wlasciciel": None,
                    "parcel_number": None,
                }

            # log live progress line
            tqdm.write(
                f"{kod}-{number}-{control_digit} -> "
                f"{data['typ_ksiegi'] or 'Brak typu'}, "
                f"{data['polozenie'] or 'Brak położenia'}, "
                f"{data['wlasciciel'] or 'Brak właściciela'}, "
                f"{data['parcel_number'] or 'Brak Identyfikatora Działki'}"
            )

            writer.writerow({
                "kod": kod,
                "number": number,
                "control_digit": control_digit,
                **data,
            })

    print(f"\n✅ Zapisano wyniki do {output_file}")


if __name__ == "__main__":
    timestamp_str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    output_file_name = f"output_kw_{timestamp_str}.csv"

    input_file = sys.argv[1] if len(sys.argv) > 1 else "input_kw.csv"
    output_file = sys.argv[2] if len(sys.argv) > 2 else output_file_name
    start = time.time()
    main(input_file, output_file)
    print(f"Czas wykonania: {time.time() - start:.2f} s")
