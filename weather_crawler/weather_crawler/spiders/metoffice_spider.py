import scrapy
from weather_crawler.items import WeatherCrawlerItem
from scrapy.http import Request

import re


class metoffice_spider(scrapy.Spider):
    name = 'metoffice'
    metoffice_json = {
        "metoffice_city": "//input/@value",
        "metoffice_up": ".//div/div[2]/div[1]/div/div[2]/span[1]/@data-value",
        "metoffice_low": ".//div/div[2]/div[1]/div/div[2]/span[2]/@data-value",
        "metoffice_date": ".//a/div[2]/div/h3[@class='tab-day']/time/@datetime",
        "metoffice_objects": "//ul[@id='dayNav']/li",
        "metoffice_detail_url_rule": ".//@href",
        "metoffice_cities": "//section[@class='link-group-container link-group-padded double-column']/div/ul/li",
        "metoffice_detail_domain": "https://www.metoffice.gov.uk/",
        "metoffice_city_name": ".//span/text()",
        "metoffice_delete_pattern": "^\s*([^\s]+)"
    }

    # Dictionary corresponding to the licence plate codes of the provinces of Turkey
    provincial_plate = {
        1: 'Adana',
        2: 'Adiyaman',
        3: 'Afyonkarahisar',
        4: 'Agri',
        5: 'Amasya',
        6: 'Ankara',
        7: 'Antalya',
        8: 'Artvin',
        9: 'Aydin',
        10: 'Balikesir',
        11: 'Bilecik',
        12: 'Bingol',
        13: 'Bitlis',
        14: 'Bolu',
        15: 'Burdur',
        16: 'Bursa',
        17: 'Canakkale',
        18: 'Cankiri',
        19: 'Corum',
        20: 'Denizli',
        21: 'Diyarbakir',
        22: 'Edirne',
        23: 'Elazig',
        24: 'Erzincan',
        25: 'Erzurum',
        26: 'Eskisehir',
        27: 'Gaziantep',
        28: 'Giresun',
        29: 'Gumushane',
        30: 'Hakkari',
        31: 'Hatay',
        32: 'Isparta',
        33: 'Mersin',
        34: 'Istanbul',
        35: 'Izmir',
        36: 'Kars',
        37: 'Kastamonu',
        38: 'Kayseri',
        39: 'Kirklareli',
        40: 'Kirsehir',
        41: 'Kocaeli',
        42: 'Konya',
        43: 'Kutahya',
        44: 'Malatya',
        45: 'Manisa',
        46: 'Kahramanmaras',
        47: 'Mardin',
        48: 'Mugla',
        49: 'Mus',
        50: 'Nevsehir',
        51: 'Nigde',
        52: 'Ordu',
        53: 'Rize',
        54: 'Sakarya',
        55: 'Samsun',
        56: 'Siirt',
        57: 'Sinop',
        58: 'Sivas',
        59: 'Tekirdag',
        60: 'Tokat',
        61: 'Trabzon',
        62: 'Tunceli',
        63: 'Sanliurfa',
        64: 'Usak',
        65: 'Van',
        66: 'Yozgat',
        67: 'Zonguldak',
        68: 'Aksaray',
        69: 'Bayburt',
        70: 'Karaman',
        71: 'Kirikkale',
        72: 'Batman',
        73: 'Sirnak',
        74: 'Bartin',
        75: 'Ardahan',
        76: 'Igdir',
        77: 'Yalova',
        78: 'Karabuk',
        79: 'Kilis',
        80: 'Osmaniye',
        81: 'Duzce'
    }

    def start_requests(self):
        start_urls = ['https://www.metoffice.gov.uk/weather/world/turkey/list']

        for url in start_urls:
            yield Request(url=url, callback=self.city_list_parse)

    def parse(self, response):
        # Parse the weather information for each day and yield WeatherCrawlerItem
        objects = response.xpath(self.metoffice_json["metoffice_objects"])
        item = WeatherCrawlerItem()
        for object in objects[:8]:
            # Extract the city name from the response
            city_full_name = response.xpath(self.metoffice_json["metoffice_city"]).get()
            city_name = re.search(self.metoffice_json["metoffice_delete_pattern"], city_full_name).group(1)

            # Set item fields with information from the response
            item['date'] = object.xpath(self.metoffice_json["metoffice_date"]).get()
            item['up'] = object.xpath(self.metoffice_json["metoffice_up"]).get()
            item['low'] = object.xpath(self.metoffice_json["metoffice_low"]).get()
            # Find and set the plate codes for the city
            item['plate_codes'] = self.find_plate_codes(city_name)
            #print(len(item))
            yield item

    def city_list_parse(self, response):
        # Parse the list of cities and extract detail URLs for each city
        objects = response.xpath(self.metoffice_json["metoffice_cities"])
        detail_urls = []
        for object in objects:
            # Extract the detail URL and city name
            detail_url = object.xpath(self.metoffice_json["metoffice_detail_url_rule"]).get()
            city_name = object.xpath(self.metoffice_json["metoffice_city_name"]).get()
            # Find the plate codes for the city and construct the detail URL
            for i in range(1, 82):
                if self.provincial_plate[i] == city_name:
                    if detail_url is None:
                        continue
                    detail_url = self.metoffice_json["metoffice_detail_domain"] + detail_url
                    detail_urls.append(detail_url)
        # Send requests for each city's detail URL
        for url in detail_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def find_plate_codes(self, city_name):
        # Find the plate codes for a given city name
        for i in range(1, 82):
            if self.provincial_plate[i] == city_name:
                return i
