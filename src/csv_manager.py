import csv
import os
from io import StringIO

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pv


def csv_to_json(csv_string):
    csv_file = StringIO(csv_string)
    reader = csv.DictReader(csv_file)
    json_array = [row for row in reader]
    return json_array


class CsvManager:
    def __init__(self, file: str, target_columns: list[str]):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File {file} does not exist")
        if not target_columns:
            raise ValueError("target_columns must be specified")

        self.table = pv.read_csv(file)
        self.target_columns = target_columns

    def query(self, query: str):
        masks = [
            pc.match_substring(self.table[col], query)  # type: ignore
            for col in self.target_columns
        ]
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask = pc.or_(combined_mask, mask)  # type: ignore
        filtered_table = self.table.filter(combined_mask)
        output_stream = pa.BufferOutputStream()
        with pa.csv.CSVWriter(output_stream, filtered_table.schema) as writer:  # type: ignore
            writer.write_table(filtered_table)
        csv_text = output_stream.getvalue().to_pybytes().decode("utf-8")
        return csv_to_json(csv_text)
