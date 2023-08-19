import csv
import pandas


def append_to_csv(data, csv_file='stock_data.csv'):
    if isinstance(data, list):
        try:
            with open(csv_file, 'r') as file:
                is_empty = len(file.readline().strip()) == 0
        except FileNotFoundError:
            is_empty = True

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if is_empty:
                if isinstance(data[0], (list, tuple)):
                    writer.writerows(data)
                else:
                    writer.writerow(data)
            else:
                if isinstance(data[0], (list, tuple)):
                    for item in data:
                        writer.writerow(item)
                else:
                    writer.writerow(data)

    elif isinstance(data, dict):
        fieldnames = list(data.keys())

        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                existing_fieldnames = reader.fieldnames
        except FileNotFoundError:
            existing_fieldnames = []

        if existing_fieldnames:
            ordered_data = [data[field] for field in existing_fieldnames]
        else:
            ordered_data = list(data.values())

        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not existing_fieldnames:
                writer.writeheader()
            writer.writerow({field: value for field, value in zip(existing_fieldnames, ordered_data)})

    elif isinstance(data, pandas.DataFrame):
        data.to_csv(csv_file, mode='a', header=False, index=False)

    else:
        raise ValueError("Unsupported data type. Only lists, dictionaries, and pandas DataFrames are supported.")
