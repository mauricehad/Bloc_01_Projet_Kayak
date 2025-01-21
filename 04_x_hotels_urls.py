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
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.urls = self.load_existing_urls()

    def load_existing_urls(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf8') as f:
                return json.load(f)
        return []

    def throttle(self):
        time.sleep(random.uniform(2, 5))

    def scroll_and_collect(self, url):
        with sync_playwright() as p:
            page = p.chromium.launch(headless=False).new_page()
            page.goto(url)

            # Accepter les cookies
            try:
                page.click("button:has-text('Accepter')", timeout=5000)
                self.throttle()
            except Exception:
                print("Bouton cookies introuvable.")

            # Ignorer les infos relatives à la connexion
            try:
                page.click('button[aria-label="Ignorer les infos relatives à la connexion"]', timeout=5000)
                self.throttle()
            except Exception:
                print("Bouton 'Ignorer les infos relatives à la connexion' introuvable.")

            # Filtrer "Hôtel" si possible
            try:
                if page.is_visible('button:has-text("Tout afficher")'):
                    self.throttle()
                    page.click('button:has-text("Tout afficher")', timeout=5000)
                    print("Clic sur 'Tout afficher' effectué.")

                page.wait_for_selector('input[type="checkbox"][aria-label*="Hôtel"]', timeout=10000)
                self.throttle()
                page.click('input[type="checkbox"][aria-label*="Hôtel"]')
                print("Clic sur la case 'Hôtel' effectué.")
            except Exception as e:
                print(f"Erreur lors de la sélection du filtre 'Hôtel' : {e}")

            # Scroll et chargement des résultats
            for _ in range(100):  
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.throttle()
                try:
                    page.click('button:has-text("Afficher plus de résultats")')
                    self.throttle()
                except Exception:
                    break 

            content = page.content()
            return content

    def parse_hotels(self, content, destination, id_destination):
        selector = Selector(text=content)
        hotels = selector.css('div[data-testid="property-card"]')
        pattern = re.compile(rf'\b{destination.lower().replace(" ", "[-\s]*")}\b')

        for hotel in hotels:
            distance_text = hotel.css('span[data-testid="distance"]::text').get(default="").lower()
            dans_destination = int(not pattern.search(distance_text))
            de_destination_km = (
                float(match.group(1).replace(',', '.'))
                if (match := re.search(r'(\d+,\d+)', distance_text)) and not dans_destination
                else 0
            )

            yield {
                'id_destination': id_destination,
                'destination': destination,
                'price': re.sub(r'[^\d]', '', hotel.css('span[data-testid="price-and-discounted-price"]::text').get(default="")),
                'url': hotel.css('a[data-testid="title-link"]::attr(href)').get(default=""),
                'dans_destination': dans_destination,
                'de_destination_km': de_destination_km
            }

    def save_hotel_data(self, hotel_data, destination):
        output_filename = f"/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/hotels_url/{destination.lower().replace(' ', '_')}_hotels_urls.json"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, 'w', encoding='utf8') as f:
            json.dump(hotel_data, f, ensure_ascii=False, indent=4)
        print(f"Data for {destination} saved.")

# Exécution directe sans structure conditionnelle
spider = BookingSpider()

for entry in spider.urls:
    destination = entry["destination"]
    url = entry["url"]
    print(f"Recherche pour {destination}")

    # Collecte des données de la page
    content = spider.scroll_and_collect(url)
    
    # Extraction des données des hôtels
    hotel_data = list(spider.parse_hotels(content, destination, entry["id_destination"]))

    # Sauvegarde des données des hôtels
    spider.save_hotel_data(hotel_data, destination)

print("Toutes les destinations ont été traitées. Le programme est terminé.")
