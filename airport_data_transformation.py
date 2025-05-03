import csv

input_file = "raw_airports.csv"
output_file = "Airports.csv"

output_headers = ["code", "name", "city", "country", "timezone"]

def transform_airport_data(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile, \
         open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        writer.writerow(output_headers)

        for row in reader:
            code = row["code"]
            name = row["name"]
            city = row["city"]
            country = row["country"]
            timezone = row["time_zone"]

            writer.writerow([code, name, city, country, timezone])

transform_airport_data(input_file, output_file)

output_file