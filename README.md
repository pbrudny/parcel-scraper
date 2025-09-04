# property-scraper

Python scraper to extract parcel numbers from the Polish KW portal.  
⚠️ This scraper is **just for learning purposes**.

## Installation

```bash
git clone https://github.com/pbrudny/property-scraper
cd property-scraper
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
playwright install
```

## Usage

```bash
python main.py
```

Example output:

```
KW WA6M/00070392/3 → Parcel Number: 15/13
```

## Running Tests

Basic tests are included in the `tests/` folder. To run them:

```bash
python -m unittest discover tests
```

or if using `pytest`:

```bash
pytest tests
```

## Linting & Formatting

Check code style with Flake8:

```bash
flake8 .
```

Format code automatically with Black:

```bash
black .
```

> Optionally, you can set up pre-commit hooks to run Black and Flake8 automatically on each commit.

## Project Structure

- `scraper/` – main scraper module
- `tests/` – test scripts
- `main.py` – CLI entry point
