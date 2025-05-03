import csv

input_file = "Pilot.csv"
output_file = "Pilot_clean.csv"

# Map IATA code to numeric AID
iata_to_aid = {
    "AAL": 1, "DL": 2, "UAL": 3, "SWA": 4, "ACA": 5,
    "DLH": 6, "BA": 7, "AFR": 8, "UAE": 9, "QTR": 10,
    "SIA": 11, "ANA": 12, "JAL": 13, "CPA": 14, "THY": 15,
    "KLM": 16, "AMX": 17, "CSN": 18, "CES": 19, "EVA": 20,
    "THA": 21, "ASA": 22, "JBU": 23, "ETD": 24, "VIR": 25
}

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    headers = next(reader)
    writer.writerow(headers)  # Write unchanged header row

    for row in reader:
        if row and len(row) == 4:
            old_aid = row[3].strip()
            new_aid = iata_to_aid.get(old_aid, '\\N')  # Default to NULL if not found
            row[3] = new_aid
            writer.writerow(row)
