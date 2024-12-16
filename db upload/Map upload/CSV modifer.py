import csv

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
                    modified = cell  # Keep short strings unchanged
                modified_row.append(modified)
            writer.writerow(modified_row)

# run as a method for clean code reasons
input_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list.csv"
output_csv = "C:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/query_list_clean.csv"
modify_csv(input_csv, output_csv)
