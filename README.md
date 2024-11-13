# Weather Crawler

This repository contains a **Scrapy**-based web crawling application developed to automatically retrieve daily weather information for cities in Turkey from three different weather websites and save the data in JSON format into a MongoDB database.

## Features

- **Multi-site support**: Ability to scrape data from three different weather websites.
- **Dynamic URL generation**: Automatic URL creation for all cities in Turkey.
- **Data conversion**: Standardization of date and temperature information.
- **MongoDB integration**: Storing the retrieved data in JSON format in a MongoDB database.

## Installation

To set up and run the project, please follow these steps:

### Requirements

- Python 3.x
- MongoDB

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SntrkUmut/Web-Crawling.git
   cd Web-Crawling
   
2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   
3. **MongoDB Setup**:
   
   - Start your MongoDB server. By default, the connection is set to localhost:27017. If using a different configuration, modify the MongoDB connection in the settings.py file.

### Usage

1. **Run the Scrapy Crawler**

   - To run the havadurumux spider, use the following command:
  
     ```bash
       scrapy crawl havadurumux

  - This will start the process of scraping weather information for all cities, and the data will be saved in MongoDB.

### Configurations

  - Data scraping and XPath expressions used for each site are defined in a JSON dictionary named havadurumux_json. XPath rules:
    - City: havadurumux_city
    - Highest Temperature: havadurumux_up
    - Lowest Temperature: havadurumux_low
    - Date: havadurumux_date
    - Data Object: havadurumux_obje

### Code Workflow

 - The crawler generates URLs based on city plate codes for all Turkish cities and navigates to the weather page of each city. Once the data is scraped, the following steps are performed:
  **1. Date Formatting:** The date information is adjusted according to Turkish month names and converted into a specific format (YYYY-MM-DD).
  **2. Saving to MongoDB:** The processed data is stored in the specified collection in MongoDB in JSON format.

**Sample Data Output**

  ```json 
       {
        "plate_codes": 34,
        "city": "Istanbul",
        "date": "2024-11-13",
        "up": "15°C",
        "low": "8°C"
      }
