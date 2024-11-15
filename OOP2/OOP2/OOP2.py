import xml.etree.ElementTree as ET
import csv
import time
from collections import defaultdict

class DataProcessor:
    def __init__(self):
        self.duplicates = defaultdict(int)
        self.floor_counts = defaultdict(lambda: defaultdict(int))
        self.start_time = time.time()

    def print_results(self):
        print("\nDuplicate entries:")
        for key, count in self.duplicates.items():
            if count > 1:
                print(f"{key} - {count} times")

        print("\nNumber of storey buildings in each city:")
        for city, floors in self.floor_counts.items():
            for floor, count in floors.items():
                print(f"{city}: {floor}-storey buildings - {count}")

        print(f"\nFile processing time: {(time.time() - self.start_time)} s")

class XMLDataProcessor(DataProcessor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def process_file(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for item in root.findall('item'):
            city = item.get('city')
            street = item.get('street')
            house = item.get('house')
            floor = item.get('floor')

            key = f"{city};{street};{house};{floor}"
            self.duplicates[key] += 1
            self.floor_counts[city][floor] += 1

class CSVDataProcessor(DataProcessor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def process_file(self):
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader) 

            for row in reader:
                city = row[0].strip('"')
                street = row[1].strip('"')
                house = row[2].strip('"')
                floor = row[3].strip('"')

                key = f"{city};{street};{house};{floor}"
                self.duplicates[key] += 1
                self.floor_counts[city][floor] += 1

def main():
    while True:
        command = input("Enter the command 1) xml, 2) csv, 0) exit :  ").strip().lower()

        if command == "0":
            break
        elif command == "1":
            processor = XMLDataProcessor("address.xml")
            processor.process_file()
            processor.print_results()
        elif command == "2":
            processor = CSVDataProcessor("address.csv")
            processor.process_file()
            processor.print_results()
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
