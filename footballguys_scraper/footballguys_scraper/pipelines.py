import csv
from pathlib import Path

class CsvPipeline:
    def open_spider(self, spider):
        # Ensure output file path is set correctly
        self.output_file = Path(spider.output_file)
        
        # Create the CSV file and write the header row when the spider opens
        self.output_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        self.file = self.output_file.open(mode="w", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Team', 'Year', 'Week', 'Position', 'Player', 'SnapCount', 'SnapPercent'])

    def close_spider(self, spider):
        # Close the CSV file when the spider closes
        self.file.close()

    def process_item(self, item, spider):
        # Write each item as a row in the CSV file
        self.writer.writerow([
            item['team'],
            item['year'],
            item['week'],
            item['position'],
            item['player'],
            item['snap_count'],
            item['snap_percent']
        ])
        return item
