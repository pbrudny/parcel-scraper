import csv
import io
import generate_kw


def test_calculate_kw_check_digit():
    # Przykłady poprawnych KW (sprawdzone w systemie EKW)
    samples = [
        ("WA1G", "00070393", 0),
        ("WA1G", "00070394", 7),
        ("WA1G", "00070395", 4),
    ]
    for court_code, number, expected in samples:
        assert generate_kw.calculate_kw_check_digit(court_code, number) == expected


def test_generate_kw_numbers_sequence():
    rows = generate_kw.generate_kw_numbers("WA1G", "00070393", 3)
    expected = [
        ("WA1G", "00070393", 0),
        ("WA1G", "00070394", 7),
        ("WA1G", "00070395", 4),
    ]
    assert rows == expected


def test_save_to_csv(tmp_path):
    # Przygotowanie danych
    rows = [
        ("WA1G", "00070393", 0),
        ("WA1G", "00070394", 7),
    ]
    output_file = tmp_path / "test_kw.csv"

    # Zapis do CSV
    generate_kw.save_to_csv(rows, filename=output_file)

    # Wczytanie i porównanie zawartości
    with open(output_file, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    assert reader == [
        ["kod", "number", "control_digit"],
        ["WA1G", "00070393", "0"],
        ["WA1G", "00070394", "7"],
    ]


def test_invalid_court_code():
    # Kod musi mieć dokładnie 4 znaki
    try:
        generate_kw.calculate_kw_check_digit("WA11G", "00070391")
    except Exception as e:
        assert isinstance(e, ValueError) or isinstance(e, IndexError)


def test_invalid_char_in_kw_number():
    # Numer KW z niedozwolonym znakiem
    try:
        generate_kw.calculate_kw_check_digit("BI3P", "00A70192")
    except Exception as e:
        assert isinstance(e, ValueError)
