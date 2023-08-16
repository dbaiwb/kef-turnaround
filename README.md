# Flight Traffic Automation for Keflavik International Airport

The Flight Traffic Analyzer is a Python command-line tool that fetches, processes, and exports flight data from online sources. It focuses on collecting data about flight arrivals and departures at the keflavik international airport, filtering and processing the data, and providing an Excel export for further analysis.

## Features

- Fetches flight data from specified URLs.
- Parses fetched data into usable dictionaries.
- Filters and processes flight data based on specified criteria.
- Exports the merged and formatted flight data to an Excel file.

## Getting Started

### Prerequisites

- Python 3.x
- Required dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/flight-traffic-analyzer.git
   cd kef-turnaround

2. Install required dependencies:

    ```bash
    pip install -r requirements.txt

### Usage

## Run using CLI

Run the main.py script followed by the number of hours before and after the current time to fetch flight data:
    ```bash
    python3 main.py --bf <hours_before> --af <hours_after>

## Run Using Docker

If you prefer using Docker for running the script, follow these steps:

1. Build the Docker image:

   ```bash
   docker build -t kef-turnaround .

2. Run the Docker container:

    ```bash
    docker run -it --rm kef-turnaround python ./app/main.py --bf <hours_before> --af <hours_after>
