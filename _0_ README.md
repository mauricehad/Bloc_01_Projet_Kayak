
# BLOC 1



## Projet KAYAK :

- Liste de 35 villes imposées.
- Dâte de voyage du projet  : 18/11/2024 au 24/11/2024 pour 2 personnes
- IMPORTANT METEO : utilisation de l'API gratuite. Pour avoir la météo du 18/11/2024 au 24/11/2024, le NoteBook 02_villes_meteo doit être lancé la veille. (API gratuite)
- Scraping de Booking.com : sélection uniquement des logements de type "hôtel"

## API utilisées :
- coordonnées GPS : https://nominatim.openstreetmap.org/search
- météo : https://api.openweathermap.org/data/3.0/onecall?


## CSV : 
- villes_coordonnees.csv : id_destination, destination, longitude, latitude
- villes_meteo.csv : date, id_destination, destination, description, min_temp_C, max_temp_C, temp_ressentie_C, humidite_pourcent, vent_ms, indice_uv, pluie_probabilite, pluie_mm, nuageux_pourcent
- villes_scoring_meteo.csv : date_sejour, id_destination, destination, scoring_sejour
- villes_hotel.csv : 


## Scoring météo et pondération :

Les éléments récupérés sont scorés à l'échelle universelle (0 à 1).

- #### Température maximale :
Idéal : entre 18°C et 30°C.
En dessous de 18°C ou au-dessus de 30°C, le score diminue progressivement.
À partir de 40°C, le score est nul.

- #### Température minimale :
Idéal : entre 10°C et 18°C.
En dessous de 10°C ou au-dessus de 18°C, le score diminue progressivement.
À partir de 25°C, le score est nul.

- ####  Température ressentie :
Idéal : entre 17°C et 25°C.
En dessous de 17°C ou au-dessus de 25°C, le score diminue progressivement.
À partir de 5°C (froid) ou 35°C (chaud), le score est nul.

- ####  Humidité relative :
Idéal : entre 40% et 60%.
En dessous de 40% ou au-dessus de 60%, le score diminue progressivement.
À partir de 20% (trop sec) ou 80% (trop humide), le score est nul.

- ####  Vitesse du vent :
Idéal : entre 0 et 5 m/s (vent calme).
Entre 5.1 et 8 m/s, le score diminue progressivement.
Au-delà de 8 m/s, le score est nul (vent trop fort).

- ####  Indice UV :
Idéal : entre 1 et 5.
En dessous de 1, le score diminue proportionnellement.
Au-delà de 5, le score diminue progressivement.
À partir de 10, le score est nul.

- ####  Probabilité de pluie :
Idéal : moins de 20%.
Entre 20% et 80%, le score diminue progressivement.
Au-delà de 80%, le score est nul.

- ####  Quantité de pluie :
Idéal : moins de 1 mm.
Entre 1 mm et 10 mm, le score diminue progressivement.
Au-delà de 10 mm, le score est nul.

- ####  Couverture nuageuse :
Idéal : entre 10% et 40%.
Entre 40% et 80%, le score diminue progressivement.
Au-delà de 80%, le score est nul.


Pondération sur le calcul du scoring :

- Température ressentie : 20%
- Probabilité de pluie : 20%
- Vitesse du vent : 15%
- Couverture nuageuse : 15%
- Quantité de pluie : 10%
- Température maximale : 5%
- Température minimale : 5%
- Humidité relative : 5%
- Indice UV : 5%