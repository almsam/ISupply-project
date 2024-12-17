import csv
import re

def clean_line(line):
    line = line.replace("\\", "") # remove all backslashes
    
    def fix_quotes(match):
        value = match.group(1)
        if value.count("'") == 3:  # check if there are exactly three '
            parts = value.split("'")  # split by single quotes
            fixed_value = parts[0] + parts[1] + parts[2]  # omit the second quote
            return f"'{fixed_value}'"  # return cleaned str w outer quotes
        return match.group(0)  # else return original string

    line = re.sub(r"'([^']*)'", fix_quotes, line) # regex to find string literals
    
    return line

def test_clean_line():
    # test case : Line with backslashes and three single quotes
    input_line = "(156, 'Children\'s Clothing');"
    expected_output = "(156, 'Children's Clothing');"
    assert clean_line(input_line) == expected_output, "test case 1 failed"
    
    
    print("All test cases passed!")

# run the tests
test_clean_line()
