# Property Scraper

This project allows you to scrape parcel numbers ("Numer działki") from Polish land registry (KW) for given KW numbers.  
It also contains a separate script to **generate KW numbers** for a specific region.

> ⚠️ This scraper is for **learning purposes only**.

---

## Project Structure

\`\`\`
parcel-scraper/
├── main.py                # Scrapes parcel numbers from input CSV -> output CSV
├── generate_kw.py         # Generates KW numbers to CSV
├── scraper/
│   └── parcel.py          # Function get_parcel_number
├── tests/                 # Unit tests with Playwright mocks
├── input_kw.csv           # Sample input CSV for scraper
├── output_parcels.csv     # Scraper output CSV
├── generated_kw.csv       # Output from generate_kw.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── venv/
\`\`\`

---

## Installation

\`\`\`bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
playwright install
\`\`\`

---

## Usage

### 1. Generate KW numbers

\`\`\`bash
python generate_kw.py
\`\`\`

This will create \`generated_kw.csv\` with the desired number of KW numbers.

---

### 2. Scrape parcel numbers from CSV

\`\`\`bash
python main.py
\`\`\`

Reads KW numbers from \`input_kw.csv\` and writes results to \`output_parcels.csv\`.  
If a parcel number cannot be scraped, the CSV will contain:

\`\`\`
brak Identyfikatora Działki
\`\`\`

---

## Testing & Linting

Run tests:

\`\`\`bash
pytest tests
\`\`\`

Check code formatting with **Black**:

\`\`\`bash
black .
\`\`\`

Check code quality with **Flake8**:

\`\`\`bash
flake8 .
\`\`\`

---

## Notes

- Only for learning purposes.  
- Do **not** use against public services without permission.  
- Headless scraping might be blocked by the website. Use \`headless=False\` if necessary.

---

## License

MIT License © 2025 Piotr Brudny
