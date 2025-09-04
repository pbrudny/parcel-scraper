import csv
from scraper.parcel import get_parcel_number
from tqdm import tqdm


def main():
    input_file = "input_kw.csv"
    output_file = "output_kw.csv"

    with open(input_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    results = []
    # tqdm progress bar
    for row in tqdm(rows, desc="Processing KW numbers", unit="kw"):
        kod = row["kod"]
        number = row["number"]
        control_digit = row["control_digit"]

        parcel_number = get_parcel_number(kod, number, control_digit)

        if parcel_number is None:
            parcel_number = "Brak Identyfikatora Działki"

        kw_str = f"{kod}-{number}-{control_digit}"
        print(f"{kw_str} -> {parcel_number}")  # per-line output

        results.append([kw_str, parcel_number])

    # Save results
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["KW", "parcel_number"])
        writer.writerows(results)

    print(f"\n✅ Done! Results saved to {output_file}")


if __name__ == "__main__":
    main()
