# ✈️ BLOC 1 : Construire et Manager une Infrastructure de Données

Bienvenue dans le projet **KAYAK**, une aventure autour de la gestion des données pour des voyages optimisés ! 🚀

---

## 🌍 Projet KAYAK

- **🌆 Liste des villes imposées :** 35 destinations à explorer.
- **📅 Date de voyage :** 18/11/2024 - 24/11/2024 (pour 2 personnes)
- **☀️ IMPORTANT METEO :** Utilisation d'une API gratuite.
  - Pour obtenir la météo des dates du séjour, exécuter le Notebook `02_villes_meteo` la veille.  
- **🏨 Scraping de Booking.com :** Focus uniquement sur les logements de type "hôtel".

---

## 🔗 API utilisées

- **🗺️ Coordonnées GPS :** [Nominatim OpenStreetMap](https://nominatim.openstreetmap.org/search)
- **🌦️ Météo :** [OpenWeatherMap API](https://api.openweathermap.org/data/3.0/onecall?)

---

## 📁 Données CSV

| Nom du fichier        | Contenu                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `villes_coordonnees.csv` | ID, destination, longitude, latitude                                 |
| `villes_meteo.csv`       | Date, destination, température, humidité, vent, pluie, nuages, UV   |
| `villes_scoring_meteo.csv` | Date du séjour, destination, scoring météo                          |
| `villes_hotel.csv`       | Informations sur les hôtels sélectionnés                            |

---

## ☀️ Scoring météo & pondération

Les données météo sont évaluées sur une échelle universelle (0 à 1) pour un séjour idéal.

| Critère                | Zone idéale                           | Diminution progressive               | Score nul                              |
|------------------------|--------------------------------------|--------------------------------------|--------------------------------------|
| **Température max**    | 18°C - 30°C                          | <18°C ou >30°C                       | ≥40°C                                  |
| **Température min**    | 10°C - 18°C                          | <10°C ou >18°C                       | ≥25°C                                  |
| **Température ressentie** | 17°C - 25°C                          | <17°C ou >25°C                       | ≤5°C ou ≥35°C                          |
| **Humidité**            | 40% - 60%                            | <40% ou >60%                         | ≤20% ou ≥80%                           |
| **Vent**                | 0 - 5 m/s                            | 5.1 - 8 m/s                           | >8 m/s                                 |
| **Indice UV**           | 1 - 5                                | <1 ou >5                              | ≥10                                    |
| **Probabilité de pluie** | <20%                                 | 20% - 80%                             | >80%                                   |
| **Quantité de pluie**   | <1 mm                                | 1 - 10 mm                             | >10 mm                                 |
| **Couverture nuageuse** | 10% - 40%                            | 40% - 80%                             | >80%                                   |

---

## ⚖️ Pondération du scoring météo

| Critère                | Pondération |
|------------------------|-------------|
| Température ressentie  | 20%         |
| Probabilité de pluie   | 20%         |
| Vitesse du vent        | 15%         |
| Couverture nuageuse    | 15%         |
| Quantité de pluie      | 10%         |
| Température maximale  | 5%          |
| Température minimale  | 5%          |
| Humidité relative     | 5%          |
| Indice UV             | 5%          |

---

Bon voyage à travers les données ! 🚀🌍

