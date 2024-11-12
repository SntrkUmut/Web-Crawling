# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from datetime import datetime

# The StatusManager class is used to monitor and update the latest status of the spider.
class StatusManager:
    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Status_Manager']
        self.collection = self.db['status_record']

    # Retrieves Spider's latest status from the database.
    def get_status(self):
        return self.collection.find_one({'spider_name': self.spider_name})

    # Updates Spider's last status or adds it for the first time.
    def update_status(self, plate_codes, last_processed_date, last_weather_up, last_weather_low):
        status = {
            'spider_name': self.spider_name,
            'plate_codes': plate_codes,
            'last_processed_date': last_processed_date,
            'last_weather_up': last_weather_up,
            'last_weather_low': last_weather_low,
            'timestamp': datetime.now()
        }
        self.collection.replace_one({'spider_name': self.spider_name}, status, upsert=True)

class WeatherCrawlerPipeline:
    def process_item(self, item, spider):
        return item

# MongoDBPipeline is used to insert and update data into MongoDB.
class MongoDBPipeline(object):
    def __init__(self):
        # Gets Scrapy settings.
        self.settings = get_project_settings()
        # Starts the Spider state manager.
        self.status_manager = StatusManager('weather_status_record')
        # Initialises the MongoDB connection.
        connection = pymongo.MongoClient(
            self.settings.get('MONGODB_SERVER'),
            self.settings.get('MONGODB_PORT')
        )
        # Selects the database and collection.
        db = connection[self.settings.get('MONGODB_DB')]
        self.collection = db[self.settings.get('MONGODB_COLLECTION')]

    # Checks the item being processed and throws the DropItem exception if there is missing data.
    # It also adds the data to MongoDB and updates the status when the spider finishes its processing.
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not item[data]:
                valid = False
                raise DropItem(f"Missing {data} in {item}")

        if valid:
            # Add the output to MongoDB
            self.insert_to_mongodb(item, spider)
            # Update status when Spider finishes processing
            self.status_manager.update_status(item.get('plate_codes'), item.get('date'), item.get('up'), item.get('low'))
        return item

    # MongoDB'ye veri ekler. Eğer veri zaten varsa günceller.
    def insert_to_mongodb(self, item, spider):
        existing_data = self.collection.find_one({
            'provincial_plate': item.get('plate_codes'),
            'date': item.get('date')
        })

        if existing_data:
            # If data already exists, update existing data
            existing_data['weather'][f'{spider.name}'] = {
                f'{spider.name}_up': item.get('up'),
                f'{spider.name}_low': item.get('low')
            }
            self.collection.update_one(
                {'_id': existing_data['_id']},
                {'$set': {'weather': existing_data['weather']}}
            )
        else:
            # If there is no data, add a new record
            data = {
                'provincial_plate': item.get('plate_codes'),
                'date': item.get('date'),
                'weather': {
                    f'{spider.name}': {
                        f'{spider.name}_up': item.get('up'),
                        f'{spider.name}_low': item.get('low')
                    }
                }
            }
            print("Inserting data to MongoDB:", data)
            self.collection.insert_one(data)



