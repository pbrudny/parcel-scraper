import csv
import argparse
import pdb

def calculate_kw_check_digit(court_code, kw_number):
    """
    Calculates the check digit for Polish land registry (księga wieczysta) number.
    
    Args:
        court_code (str): 4-character court code (e.g., "WA1G")
        kw_number (str): 8-digit land registry number (e.g., "00070392")
    
    Returns:
        int: Check digit (0-9)
    """
    # Combine court code and KW number
    full_number = court_code + kw_number
    
    # Polish KW character to number mapping
    char_map = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'X': 10, 'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 
        'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23, 'N': 24, 'O': 25, 
        'P': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'W': 31, 'Y': 32, 'Z': 33
    }
    
    # Weights for each position (12 positions total) - repeating pattern 1,3,7
    weights = [1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]
    
    total = 0
    
    # Calculate control sum
    for i, char in enumerate(full_number):
        char_upper = char.upper()
        if char_upper in char_map:
            value = char_map[char_upper]
        else:
            raise ValueError(f"Invalid character '{char}' in KW number")
        
        total += value * weights[i]
    
    # Check digit is remainder when divided by 10
    check_digit = total % 10
    
    return check_digit


def generate_kw_numbers(court_code, starting_number, count):
    """
    Generates sequential KW numbers starting from a given number.
    
    Args:
        court_code (str): 4-character court code
        starting_number (str): 8-digit starting number
        count (int): Number of KW numbers to generate
    
    Returns:
        list: List of tuples (court_code, number, check_digit)
    """
    kw_numbers = []
    current_number = int(starting_number)
    
    for _ in range(count):
        # Format number back to 8-digit string with leading zeros
        number_str = f"{current_number:08d}"
        
        # Calculate check digit
        check_digit = calculate_kw_check_digit(court_code, number_str)
        
        # Add to results
        kw_numbers.append((court_code, number_str, check_digit))
        
        # Increment for next iteration
        current_number += 1
    
    return kw_numbers


def save_to_csv(kw_numbers, filename="input_kw.csv"):
    """
    Saves KW numbers to CSV file.
    
    Args:
        kw_numbers (list): List of tuples (court_code, number, check_digit)
        filename (str): Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['kod', 'number', 'control_digit'])
        
        # Write data
        for court_code, number, check_digit in kw_numbers:
            writer.writerow([court_code, number, check_digit])
    
    print(f"Generated {len(kw_numbers)} KW numbers and saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate sequential Polish land registry (KW) numbers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_kw.py WA1G 00070392 10
  python generate_kw.py WA1G 00070392 10 -o output.csv
  python generate_kw.py --help
        """
    )
    
    parser.add_argument('court_code', help='4-character court code (e.g., WA1G)')
    parser.add_argument('starting_number', help='8-digit starting KW number (e.g., 00070392)')
    parser.add_argument('count', type=int, help='Number of KW numbers to generate')
    parser.add_argument('-o', '--output', default='input_kw.csv', 
                       help='Output CSV filename (default: input_kw.csv)')
    
    args = parser.parse_args()
    
    # Validate input
    if len(args.court_code) != 4:
        print("Error: Court code must be exactly 4 characters")
        return
    
    if len(args.starting_number) != 8 or not args.starting_number.isdigit():
        print("Error: Starting number must be exactly 8 digits")
        return
    
    if args.count <= 0:
        print("Error: Count must be a positive number")
        return
    
    # Generate KW numbers
    print(f"Generating {args.count} KW numbers starting AFTER {args.court_code}/{args.starting_number}")
    
    kw_numbers = generate_kw_numbers(args.court_code, args.starting_number, args.count)
    
    # Save to CSV
    save_to_csv(kw_numbers, args.output)
    
    # Display first few examples
    print("\nFirst few generated numbers:")
    for i, (code, number, check_digit) in enumerate(kw_numbers[:5]):
        print(f"{i+1:2d}. {code}/{number}/{check_digit}")
    
    if len(kw_numbers) > 5:
        print(f"... and {len(kw_numbers) - 5} more")


if __name__ == "__main__":
    pdb.set_trace()
    main()