# 📊 Financial Dashboard - Market Analyzer

Application Streamlit complète d'analyse de marchés financiers avec visualisation technique, gestion de portefeuille et analyse de sentiment.

![alt text](image.png)

## ✨ Fonctionnalités principales
![alt text](image-1.png)
- **Tableaux de bord individuels** :
  - Analyse technique (MA, RSI, Bollinger Bands)
  - Visualisations interactives (Plotly)
  ![alt text](image-2.png)
  - Alertes personnalisables
  ![alt text](image-3.png)
- **Comparaison multi-actifs** :
  - Analyse comparative entre plusieurs tickers
  ![alt text](image-4.png)
  ![alt text](image-5.png)
  - Téléchargement asynchrone des données
  ![alt text](image-6.png)
- **Portefeuille virtuel** :
  - Simulation de portefeuille multi-actifs
  - Analyse de performance et risque
  ![alt text](image-7.png)
  ![alt text](image-8.png)
  ![alt text](image-9.png)
  - Cartographie géographique des expositions
  ![alt text](image-10.png)
- **Analyse de marché** :
![alt text](image-11.png)
  - Sentiment Reddit (simulé)
  ![alt text](image-12.png)
  - Actualités financières
  ![alt text](image-13.png)
  - Contexte macroéconomique
  ![alt text](image-14.png)
- **Personnalisation** :
  - 7 thèmes visuels différents
  - Système de couleurs global
  ![alt text](image-15.png)
  ![alt text](image-16.png)
  ![alt text](image-17.png)
  ![alt text](image-18.png)
  ![alt text](image-19.png)
  ![alt text](image-20.png)
  ![alt text](image-21.png)

  ## ⚙️ Installation

1. **Cloner le dépôt** :
```bash
git clone https://github.com/BuyukHasan/bourse_dashboard
cd bourse_dashboard

2. **Créer un environnement virtuel** : 
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

3. **Installer les dépendances** :
pip install -r requirements.txt

4. **Lancer l'application** :
streamlit run app.py

🚀 Utilisation
Modes disponibles
Dashboard individuel : Analyse technique d'un actif

Comparaison multi-actifs : Comparaison de plusieurs instruments

Portefeuille virtuel : Simulation de stratégie d'investissement

Tests unitaires : Validation des modules

Commandes utiles
Ctrl+C : Arrêter l'application

Clear cache : Bouton dans la sidebar pour rafraîchir les données

🧩 Structure des fichiers
text
financial-dashboard/
├── app.py                # Point d'entrée principal
├── requirements.txt      # Dépendances
├── .gitignore
├── asset_categories.py   # Classement des actifs par secteur
├── css.py                # Gestion des thèmes visuels
├── dashboard.py          # Module principal du dashboard
├── data_fetcher.py       # Récupération des données (yfinance)
├── geo_data.py           # Données géographiques
├── macro_data.py         # Données macroéconomiques
├── news_fetcher.py       # Collecte d'actualités
├── portfolio_manager.py  # Gestion de portefeuille
├── reddit_analyzer.py    # Analyse de sentiment (simulé)
├── technical_analyzer.py # Calculs d'indicateurs techniques
└── visualizer.py         # Visualisations graphiques

🛠 Dépendances clées
streamlit==1.47.0 - Interface web

yfinance==0.2.65 - Données financières

plotly==6.2.0 - Visualisations interactives

pandas==2.3.0 - Manipulation de données

numpy==2.2.2 - Calculs scientifiques

🤝 Contribution
Les contributions sont bienvenues ! Process recommandé :

Forker le projet

Créer une branche : git checkout -b feature/nouvelle-fonctionnalite

Commiter vos changements : git commit -m 'Ajout d'une super fonction'

Pousser vers la branche : git push origin feature/nouvelle-fonctionnalite

Ouvrir une Pull Request

📜 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.


