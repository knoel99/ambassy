# Ambassy - G20 Embassy Distance Map

Carte interactive des distances entre les ambassades des pays du G20 (+ Israël) et les centres de pouvoir de chaque capitale.

**Live :** [https://knoel99.github.io/ambassy/](https://knoel99.github.io/ambassy/)  
**Portfolio :** [https://knoel99.github.io/](https://knoel99.github.io/)

## Site statique (GitHub Pages)

Servi à la racine du dépôt (`index.html`, `css/`, `js/`, `data/`).

```bash
python3 -m http.server 8080
# http://localhost:8080/
```

Régénérer le manifest front :

```bash
python scripts/generate_manifest.py   # nécessite Node pour parser data/embassies.js
```

## Générateur Python (Folium)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_map.py
# sortie historique : dist/g20_embassy_map.html
```

## Structure

```
ambassy/
  index.html              # Site Pages (carte interactive)
  css/ js/ data/          # Front
  scripts/generate_manifest.py
  generate_map.py         # Générateur Folium
  src/                    # Données Python
  requirements.txt
```
