import scrapy
from weather_crawler.items import WeatherCrawlerItem
from datetime import datetime



class havadurumux_spiders(scrapy.Spider):
    name = 'havadurumux'
    # XPath rules  (city, highest temperature, lowest temperature, date, weather information)
    havadurumux_json = {
        "havadurumux_city": "//div[@class='entry-content clearfix']/h1/text()",
        "havadurumux_up": "./td[3]/text()",
        "havadurumux_low": "./td[4]/text()",
        "havadurumux_date": "./td[1]/text()",
        "havadurumux_obje": "//table[@id='hor-minimalist-a']/tbody/tr"
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
        # Generate URLs of weather pages for cities
        start_urls = []
        for i in range(1, 82):
            domain = "https://www.havadurumux.net/"
            last = "-hava-durumu/"
            url = domain + self.provincial_plate[i] + last
            start_urls.append(url)

        # Create a scrapy.Request for each URL and redirect it to the parse method
        counter = 0
        for url in start_urls:
            counter = counter + 1
            yield scrapy.Request(url=url, callback=self.parse, meta={'plate_codes': counter})

    def parse(self, response):
        # Select objects containing weather data on the sheet
        objects = response.xpath(self.havadurumux_json["havadurumux_obje"])
        # Create a WeatherCrawlerItem instance
        item = WeatherCrawlerItem()
        # Get weather data for each object
        for object in objects[:7]:
            # Get the licence plate code
            item['plate_codes'] = response.meta.get('plate_codes')
            # Edit date information retrieved from the page
            date = object.xpath(self.havadurumux_json["havadurumux_date"]).get()
            turkish_months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz',
                              'Ağustos', 'Eylül','Ekim', 'Kasım', 'Aralık']

            for i, month_name in enumerate(turkish_months, start=1):
                date = date.replace(month_name, f"{i:02}").split(",")[0].strip()

            # Convert date to datetime object and convert to desired format
            parsed_date = datetime.strptime(date, '%d %m %Y')
            formatted_date = parsed_date.strftime('%Y-%m-%d')
            # Pull other weather data and yield by creating the item
            item['date'] = formatted_date
            item['up'] = object.xpath(self.havadurumux_json["havadurumux_up"]).get()
            item['low'] = object.xpath(self.havadurumux_json["havadurumux_low"]).get()
            yield item


