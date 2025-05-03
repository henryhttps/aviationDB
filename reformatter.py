import csv

input_file = '/Users/henrywalen/Desktop/CS Projects/databases/Airport.csv'
output_file = '/Users/henrywalen/Desktop/CS Projects/databases/Airport_clean.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Replace empty strings with None (which becomes empty field in CSV)
        cleaned_row = [field if field.strip() != '' else '\\N' for field in row]
        writer.writerow(cleaned_row)
