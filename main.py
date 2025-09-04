from scraper.parcel import get_parcel_number
import csv


def scrape_kw_from_csv(input_csv: str, output_csv: str) -> None:
    """
    Read KW numbers from input CSV, scrape parcel numbers, and write results
    to output CSV.
    """
    with open(input_csv, newline="", encoding="utf-8") as infile, open(
        output_csv, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["parcel_number"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            kod = row["kod"]
            number = row["number"]
            control_digit = row["control_digit"]

            parcel_number = get_parcel_number(kod, number, control_digit)
            row["parcel_number"] = parcel_number
            writer.writerow(row)
            print(f"{kod}-{number}-{control_digit} -> {parcel_number}")


if __name__ == "__main__":
    scrape_kw_from_csv("input_kw.csv", "output_parcels.csv")
