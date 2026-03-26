# Ambassy - G20 Embassy Distance Map

Carte interactive montrant la distance entre les ambassades des pays du G20 et les centres de pouvoir (sieges du gouvernement) de chaque pays hote.

## Fonctionnalites

- Carte interactive (Folium/Leaflet) avec les 20 pays du G20
- Marqueurs des centres de pouvoir (Maison Blanche, Elysee, Kremlin...)
- Localisation des ambassades de chaque pays du G20 dans chaque capitale
- Calcul des distances (formule de Haversine) et classement
- Gradient de couleur vert (proche) -> rouge (eloigne)
- Panneau de statistiques et classement par distance moyenne

## Installation

```bash
# Creer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Installer les dependances
pip install -r requirements.txt
```

## Utilisation

```bash
# Activer le venv
source .venv/bin/activate

# Generer la carte
python generate_map.py
```

La carte est generee dans `dist/g20_embassy_map.html`. Ouvrir ce fichier dans un navigateur.

## Visualisation en ligne

La carte est disponible sur [knoel99.github.io/projects/ambassy/](https://knoel99.github.io/projects/ambassy/)

## Structure

```
ambassy/
  generate_map.py      # Script principal de generation
  src/data.py           # Donnees : coordonnees, ambassades, distances
  requirements.txt      # Dependances Python (folium)
  dist/                 # Sortie generee (gitignored)
```
