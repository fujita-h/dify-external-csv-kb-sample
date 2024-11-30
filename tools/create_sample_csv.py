import csv
import os

from faker import Faker

fake = Faker("ja_JP")
num_records = 100
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, "data")
csv_file = os.path.join(data_dir, "address.csv")

with open(csv_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "address", "company", "email", "phone"])
    for i in range(1, num_records + 1):
        writer.writerow(
            [
                i,
                fake.name(),
                fake.address(),
                fake.company(),
                fake.email(),
                fake.phone_number(),
            ]
        )
