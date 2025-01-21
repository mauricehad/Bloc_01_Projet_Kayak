import os
import pandas as pd
import json
import time
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

# Chemins des fichiers
csv_file_path = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/csv_files/villes_hotel.csv"
json_output_path = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/hotels_détails.json"

# Charger les données CSV
data = pd.read_csv(csv_file_path)

class HotelSpider(scrapy.Spider):
    name = "hotel_spider"

    def throttle(self):
        time.sleep(2)

    def start_requests(self):
        for _, row in data.iterrows():
            self.throttle()
            yield scrapy.Request(url=row['url'], callback=self.parse, meta={'id_hotel': row['id_hotel'], 'destination': row.get('destination', 'Unknown')})

    def parse(self, response):
        id_hotel = response.meta['id_hotel']
        destination = response.meta['destination']
        lat, long = response.xpath('//*[@data-atlas-latlng]/@data-atlas-latlng').get().split(',')
        description = response.xpath('//p[@data-testid="property-description"]//text()').getall()
        description = " ".join(description).replace('\xa0', ' ').replace('\n', ' ').strip()
        description = " ".join(description.split())

        # Scrapper le nombre d'expériences et la note moyenne
        review_section = response.xpath('//div[@data-capla-component-boundary="b-property-web-property-page/PropertyReviewScoreRight"]')
        nombre_xp_text = review_section.xpath('.//div[contains(text(), "expériences vécues")]/text()').get()
        nombre_xp = int(nombre_xp_text.split(' ')[0].replace(' ', '')) if nombre_xp_text else 0

        note_moyenne_text = review_section.xpath('.//div[contains(@class, "a3b8729ab1")]/text()').re_first(r'(\d+,\d+)')
        note_moyenne = float(note_moyenne_text.replace(',', '.')) if note_moyenne_text else None

        # Scrapper le nombre de points forts
        nombre_pts_forts = len(response.xpath('//div[@data-capla-component-boundary="b-property-web-property-page/PropertyMostPopularFacilities"]//li').getall())

        yield {
            "id_hotel": id_hotel,
            "lat": lat.strip(),
            "long": long.strip(),
            "description": description,
            "nombre_xp": nombre_xp,
            "note_moyenne": note_moyenne,
            "nombre_pts_forts": nombre_pts_forts
        }
        self.logger.info(f"Scrapping terminé pour : {destination}")

# Supprimer le fichier JSON existant s'il existe
if os.path.exists(json_output_path):
    os.remove(json_output_path)

# Configurer le CrawlerProcess avec les paramètres appropriés
process = CrawlerProcess(settings={
    'USER_AGENT': 'Chrome/130.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        json_output_path: {
            "format": "jsonlines",
            'encoding': 'utf8',
            'ensure_ascii': False,
        },
    }
})

# Démarrer le crawler
process.crawl(HotelSpider)
process.start()

# Lire le fichier JSONLines et l'enregistrer avec une meilleure présentation
with open(json_output_path, 'r', encoding='utf8') as file:
    data = [json.loads(line) for line in file]

with open(json_output_path, 'w', encoding='utf8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Données enregistrées dans {json_output_path}")
