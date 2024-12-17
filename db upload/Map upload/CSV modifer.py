import csv
import re

def modify_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            modified_row = []
            for cell in row:
                if len(cell) > 1: #safety case
                    # remove 1st, 14th, 26th, and -1st characters
                    modified = ''.join(
                        char for i, char in enumerate(cell) 
                        if i not in {len(cell)}#, 12, 25, len(cell) - 1}
                    )
                else:
                    modified = cell  # keep short strings unchanged
                modified_row.append(modified)
            writer.writerow(modified_row)


def clean_line(line):
    line = line.replace("\\", "") # remove all backslashes
    
    def fix_quotes(match):
        value = match.group(1)
        if value.count("'") == 3:  # Check if there are exactly three '
            parts = value.split("'")  # split by single quotes
            fixed_value = parts[0] + parts[1] + parts[2]  # omit the second quote
            return f"'{fixed_value}'"  # return cleaned str w outer quotes
        return match.group(0)  # else return original string

    line = re.sub(r"'([^']*)'", fix_quotes, line) # regex to find string literals
    
    return line


def modify_csv_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = clean_line(line)
            line = line.strip()  # remove head whitespace
            if len(line) > 1: #safety case
                    # remove 1st, 14th, 26th, and -1st characters
                modified_line = ''.join(
                    char for i, char in enumerate(line)
                    if i not in {0, 13, 25, len(line) - 1}
                )
                outfile.write(modified_line + '\n')
            else:
                outfile.write(line + '\n')  # return unchanged if line is too short

# run as a method for clean code reasons
input_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list.csv"
output_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list_clean.csv"
output_sql = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list_clean.sql"
modify_csv_lines(input_csv, output_csv)
modify_csv_lines(input_csv, output_sql)


