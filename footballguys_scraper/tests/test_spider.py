import sys
from pathlib import Path

# Add the project root to the import path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import unittest
from scrapy.http import HtmlResponse, Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from footballguys_scraper.spiders.footballguys_spider import FootballGuysSpider
from footballguys_scraper.items import SnapCountItem
from footballguys_scraper.pipelines import CsvPipeline
import tempfile
import os
import csv

class FootballGuysSpiderTest(unittest.TestCase):

    def setUp(self):
        # Initialize the spider and temporary directory for CSV output
        self.spider = FootballGuysSpider()
        self.process = CrawlerProcess(get_project_settings())
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name).joinpath("test_football_snap_counts.csv")
        
        # Override CSV output file path for testing
        self.spider.output_file = self.csv_path

    def tearDown(self):
        # Clean up temporary directory after tests
        self.temp_dir.cleanup()

    def test_spider_initialization(self):
        # Test if the spider initializes correctly with the expected settings
        self.assertEqual(self.spider.name, "footballguys_spider")
        self.assertTrue(hasattr(self.spider, "teams"))
        self.assertTrue(hasattr(self.spider, "current_year"))
        self.assertEqual(self.spider.current_year, 2024)

    def test_parse_function(self):
        # Define a sample HTML response
        sample_html = """
        <html>
            <table class="table">
                <thead>
                    <tr><th>QB</th><th>Wk 1</th><th>Wk 2</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td><a>Player A</a></td>
                        <td><div>40</div><b>100%</b></td>
                        <td><div>38</div><b>95%</b></td>
                    </tr>
                </tbody>
            </table>
        </html>
        """

        # Create a mock request with meta data and attach it to the response
        request = Request(url="https://www.footballguys.com/stats", meta={'team': 'Test Team'})
        response = HtmlResponse(
            url="https://www.footballguys.com/stats",
            body=sample_html,
            encoding="utf-8",
            request=request  # Attach the request with meta data
        )

        # Run the spider's parse function
        results = list(self.spider.parse(response))

        # Check that the correct number of items is yielded
        self.assertEqual(len(results), 1)

        # Validate the fields of the first item
        item = results[0]
        self.assertIsInstance(item, SnapCountItem)
        self.assertEqual(item["team"], "Test Team")  # Expect 'Test Team' from meta
        self.assertEqual(item["position"], "QB")
        self.assertEqual(item["player"], "Player A")
        self.assertEqual(item["snap_count"], "40")
        self.assertEqual(item["snap_percent"], "100%")
        self.assertEqual(item["week"], "1")

    def test_csv_pipeline(self):
        # Initialize CSV pipeline and open spider
        pipeline = CsvPipeline()
        pipeline.open_spider(self.spider)

        # Mock an item
        item = SnapCountItem(
            team="Test Team",
            year=2024,
            week="1",
            position="QB",
            player="Player A",
            snap_count="40",
            snap_percent="100%"
        )

        # Process the item
        pipeline.process_item(item, self.spider)

        # Close the pipeline (writes to the CSV file)
        pipeline.close_spider(self.spider)

        # Read back the CSV to check if the item was written correctly
        with open(self.csv_path, newline="") as csvfile:
            rows = list(csv.reader(csvfile))
            self.assertEqual(len(rows), 2)  # Header + 1 item
            self.assertEqual(rows[1], ["Test Team", "2024", "1", "QB", "Player A", "40", "100%"])

if __name__ == "__main__":
    unittest.main()
