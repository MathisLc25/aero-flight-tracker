# Airline Operations Control Center (OCC) and ADS-B Telemetry Platform

Plateforme web de surveillance des opérations aériennes inspirée des systèmes OCC (Operations Control Center), assurant le suivi télémétrique en temps réel de liaisons internationales au départ de Paris-CDG, le calcul d'impact énergétique et l'analyse météorologique d'approche.

---

## Fonctionnalités principales

* Trajectoires et suivi radar 2D : Projection cartographique orthodromique interactive (Folium) avec replay temporel dynamique de la position de l'aéronef et calcul du cap vrai (bearing).
* Télémétrie de bord en direct : Altitude barométrique, vitesse sol (GS), nombre de Mach et vitesse verticale (variomètre).
* Analyse énergétique et environnementale : Évaluation du profil de consommation de kérosène selon la phase de vol (montée vs palier) et calcul de l'empreinte carbone (CO2 par passager).
* Météo opérationnelle à destination : Calcul vectoriel du vent de traversier (crosswind) et de face sur la piste en service selon les données d'orientation d'axe.
* Flotte multi-appareils : Intégration de profils de vol réels (Airbus A320, A220-300, A350-900, Boeing 777-300ER).

---

## Architecture technique

* Langage : Python 3
* Interface : Streamlit
* Moteur spatial & géodésique : Geopy (distance géodésique WGS 84), NumPy, Pandas
* Visualisation de données : Folium, Plotly Express

---

## Démarrage rapide

```bash
pip install streamlit streamlit-folium folium geopy pandas plotly
streamlit run src/app.py