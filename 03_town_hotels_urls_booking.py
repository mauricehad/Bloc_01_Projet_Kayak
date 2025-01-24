import os
import json
import time
import random
import re
from playwright.sync_api import sync_playwright
from scrapy import Selector

class BookingSpider:
    def __init__(self):
        self.filename = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/villes_urls.json"
        self.processed_filename = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/processed_destinations.json"
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self.urls = self.load_json(self.filename)
        self.processed_destinations = set(self.load_json(self.processed_filename, default=[]))

    def load_json(self, filepath, default=None):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf8') as f:
                return json.load(f)
        return default if default is not None else []

    def save_json(self, filepath, data):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def throttle(self):
        time.sleep(random.uniform(1, 3))

    def click_element(self, page, selector, description, timeout=5000):
        try:
            page.wait_for_selector(selector, timeout=timeout)
            page.click(selector)
            self.throttle()
            print(f"{description} effectué.")
        except Exception:
            print(f"{description} introuvable.")

    def scroll_and_collect(self, url):
        with sync_playwright() as p:
            page = p.chromium.launch(headless=False).new_page()
            page.goto(url)

            self.click_element(page, "button:has-text('Accepter')", "Bouton cookies")
            self.click_element(page, 'button:has-text("Tout afficher")', "Clic sur 'Tout afficher'")
            self.click_element(page, 'input[type="checkbox"][aria-label*="Hôtel"]', "Clic sur la case 'Hôtel'")

            click_count = 0
            try:
                start_time = time.time()
                while not page.is_visible('button:has-text("Afficher plus de résultats")'):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    self.throttle()
                    if time.time() - start_time > 10:
                        raise Exception("Timeout atteint en attendant le bouton 'Afficher plus de résultats'.")
                for _ in range(50):
                    if page.is_visible('button:has-text("Afficher plus de résultats")'):
                        page.click('button:has-text("Afficher plus de résultats")')
                        self.throttle()
                        click_count += 1
                    else:
                        break
                print(f"Bouton 'Afficher plus de résultats' cliqué {click_count} fois.")
            except Exception as e:
                print(str(e))
            return page.content()

    def parse_hotels(self, content, destination, id_destination):
        selector = Selector(text=content)
        hotels = selector.css('div[data-testid="property-card"]')

        for hotel in hotels:
            ville_de_lhotel, dans_destination, de_destination_km = self.extract_hotel_info(hotel, destination)
            nom_hotel = hotel.css('div[data-testid="title"]::text').get(default="").strip()
            stars = len(hotel.css('div[data-testid="rating-stars"] > span'))

            yield {
                'id_destination': id_destination,
                'destination': destination,
                'nom_hotel': nom_hotel,
                'ville_de_lhotel': ville_de_lhotel.strip(),
                'price': re.sub(r'[^\d]', '', hotel.css('span[data-testid="price-and-discounted-price"]::text').get(default="")),
                'url': hotel.css('a[data-testid="title-link"]::attr(href)').get(default=""),
                'dans_destination': dans_destination,
                'de_destination_km': de_destination_km,
                'stars': stars if stars else 0
            }

    def extract_hotel_info(self, hotel, destination):
        address_text = hotel.css('span[data-testid="address"]::text').get(default="").strip().lower().replace('-', ' ')
        address_parts = address_text.split(', ')
        ville_de_lhotel = address_parts[-1] if len(address_parts) > 1 else address_text
        distance_text = hotel.css('span[data-testid="distance"]::text').get(default="").lower()
        destination_normalized = destination.lower().replace('-', ' ')

        if destination_normalized in ville_de_lhotel:
            return ville_de_lhotel, 1, 0
        else:
            de_destination_km = (
                float(match.group(1).replace(',', '.'))
                if (match := re.search(r'([\d.,]+)', distance_text))
                else 0
            )
            return ville_de_lhotel, 0, de_destination_km

    def save_hotel_data(self, hotel_data, destination):
        output_filename = f"/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/hotels_url/{destination.lower().replace(' ', '_')}_hotels_urls.json"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        self.save_json(output_filename, hotel_data)
        print(f"Data for {destination} saved.")

spider = BookingSpider()

for entry in spider.urls:
    destination = entry["destination"]
    url = entry["url"]

    if destination in spider.processed_destinations:
        print(f"{destination} déjà traitée, passage à la suivante.")
        continue

    print(f"Recherche pour {destination}")
    content = spider.scroll_and_collect(url)
    hotel_data = list(spider.parse_hotels(content, destination, entry["id_destination"]))
    spider.save_hotel_data(hotel_data, destination)
    spider.processed_destinations.add(destination)
    spider.save_json(spider.processed_filename, list(spider.processed_destinations))

print("Toutes les destinations ont été traitées. Le programme est terminé.")
