import csv

def remove_columns(input_file, output_file, columns_to_remove):
    with open(input_file, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Remove the specified columns
    for row in data:
        for column_index in sorted(columns_to_remove, reverse=True):
            del row[column_index]

    # Write the modified data to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

# Example usage:
input_file_path = 'Voiledencre.csv'
output_file_path = 'VoileDencre.csv'
columns_to_remove = [1, 2, 7, 8]  # Columns are 0-based indexed, so 3 represents the 4th column, and 4 represents the 5th column.

remove_columns(input_file_path, output_file_path, columns_to_remove)