# récupération de l'url booking pour chaque ville pour les dates du 3 janvier 2025 au 9 janvier 2025.

import os
import json
import time
import pandas as pd
from playwright.sync_api import sync_playwright

class BookingSpiderHome:
    def __init__(self):
        self.filename = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/json_files/villes_urls.json"
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        csv_path = "/Users/maurice/Documents/certification/bloc_1_Build_and_manage_a_data_infrastructure/csv_files/villes_coordonnees.csv"
        self.destination = pd.read_csv(csv_path)["destination"]
        self.urls = self.load_existing_urls()

    def load_existing_urls(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf8') as f:
                return json.load(f)
        return []

    def search_and_get_url(self, destination):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            try:
                page.goto('https://www.booking.com/', timeout=60000)
                try:
                    page.click('button:has-text("Accepter")', timeout=5000)
                except:
                    print("Pas de bouton 'Accepter' trouvé.")

                time.sleep(2)
                page.fill('input[name="ss"]', destination)
                time.sleep(2)
                page.click('[data-testid="searchbox-dates-container"]')
                page.click('span[data-date="2025-01-13"]')
                page.click('span[data-date="2025-01-19"]')
                page.click('button[type="submit"]')

                # Attente pour que les résultats de recherche se chargent
                page.wait_for_selector('div[data-testid="property-card"]', timeout=60000)

                # Fermer le pop-up de connexion si présent
                try:
                    page.click('button[aria-label="Ignorer les infos relatives à la connexion"]', timeout=5000)
                except:
                    print("Pas de pop-up à ignorer.")

                time.sleep(3)
                return page.url
            except Exception as e:
                print(f"Erreur lors de la recherche pour {destination}: {e}")
                return None
            finally:
                browser.close()

    def save_url(self, url_entry):
        self.urls.append(url_entry)
        with open(self.filename, 'w', encoding='utf8') as f:
            json.dump(self.urls, f, ensure_ascii=False, indent=4)

    def run(self):
        for index, destination in enumerate(self.destination):
            print(f"Recherche pour {destination}")
            result_url = self.search_and_get_url(destination)
            self.save_url({"id_destination": index, "destination": destination, "url": result_url})

if __name__ == "__main__":
    BookingSpiderHome().run()
