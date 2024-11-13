# FootballGuys Scraper

This project scrapes football data for a specified year and saves the results as a CSV file. The data is extracted using Scrapy and can be run in a Docker container for easy setup and consistent results.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed on your system.
- Ensure you have `sudo` permissions to run Docker commands, as `sudo` is required for all Docker operations in this project.

## Getting Started

Clone the repository and navigate to the project root:

```bash
git clone https://github.com/yourusername/footballguys-scraper.git
cd footballguys-scraper
```

## Setting Up

### 1. Build the Docker Image

Use Docker Compose to build the Docker image. Run the following command in the project root:

```bash
sudo docker-compose build
```

This will build the image based on the `Dockerfile` in the root directory, installing all necessary dependencies.

## Running the Scraper

To run the scraper for a specific year and save the output to a directory on your host machine, use the following command:

```bash
sudo OUTPUT_DIR=/path/to/host/output YEAR=2024 docker-compose up
```

- **OUTPUT_DIR**: The path on your host machine where you want the output CSV file to be saved.
- **YEAR**: The year you want to scrape data for.

For example:

```bash
sudo OUTPUT_DIR=/home/username/Downloads YEAR=2024 docker-compose up
```

This will:
1. Run the scraper for the year 2024.
2. Save the CSV output to `/home/username/Downloads` on the host machine.

## Output

The output file will be saved in the specified `OUTPUT_DIR` on your host machine with the name `football_snap_counts.csv`.

## Stopping the Scraper

To stop the scraper, press `CTRL + C` in the terminal where the scraper is running. This will shut down the Docker container.