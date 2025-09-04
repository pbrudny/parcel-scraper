from scraper.parcel import get_parcel_number

if __name__ == "__main__":
    kw_number = ("WA6M", "00538393", "0")
    parcel_number = get_parcel_number(*kw_number)
    print(
        f"KW {kw_number[0]}/{kw_number[1]}/{kw_number[2]} → Parcel Number: {parcel_number}"
    )
