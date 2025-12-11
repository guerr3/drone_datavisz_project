# Drone Proliferation & Impact Analysis

## 📖 Over dit Project

Dit project bevat een uitgebreide data-analyse en visualisatie van de wereldwijde drone-markt, de impact van drone-aanvallen en de effectiviteit van luchtafweersystemen. De analyse is uitgevoerd in een Jupyter Notebook en maakt gebruik van diverse datasets (o.a. CNAS, Drone Wars) om inzicht te geven in moderne oorlogsvoering.

De analyse is opgedeeld in drie kernsecties:

1.  **De Wereldwijde Drone Markt:** Analyse van leveranciers (o.a. VS, Israël, Turkije), exporttrends en geopolitieke relaties.
2.  **Impact van Drone Strikes:** Onderzoek naar slachtoffers, verantwoordelijkheid per president en burgerslachtoffers.
3.  **Casestudy Oekraïne:** Een diepte-analyse van de luchtafweer-effectiviteit tegen drones (zoals de Shahed) versus ballistische raketten.

## 📦 Installatie & Setup

Volg deze stappen om de omgeving op te zetten:

### 1\. Clone de repository

Download de broncode naar je lokale machine via de terminal:

```bash
git clone https://github.com/guerr3/drone_datavisz_project.git
cd drone_datavisz_project
```

## 📂 Data Structuur

Zorg ervoor dat de bronbestanden excel / csv in de juiste map staan of gebruik de kaggle datasets via mijn account. Het script verwacht de data in de root directory of een `data/` submap (controleer de `pd.read_csv` paden in het notebook).

Benodigde datasets/

  * `drone transfer data - excel` (CNAS data) - https://www.cnas.org/publications/reports/drone-proliferation-dataset
  * `DroneWarsData - excel` (Impact data) - https://dronewars.github.io/data/
  * `ukraine_missile_attacks.csv` (Oekraïne conflict data) - https://www.kaggle.com/datasets/piterfm/massive-missile-attacks-on-ukraine?select=missile_attacks_daily.csv

## 📊 Visualisaties

Het notebook genereert o.a. de volgende visualisaties:

  * **Heatmaps:** Geografische spreiding van drone-aanvallen.
  * **Bar & Line Charts:** Historische trends van marktleiders en exportvolumes.
  * **Interactieve Kaarten (Folium):** Detailweergave van succesratio's van luchtafweer in specifieke regio's.

## 👤 Auteur

**Warre Gehre**

  * Student Cyber Security, Cloud & AI
  * Datum: December 2025

## 📄 Licentie

Dit project is uitsluitend bedoeld voor educatieve doeleinden.
