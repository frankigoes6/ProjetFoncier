# 🏠 ProjetFoncier - Analyse DVF pour Investissement Immobilier

## 📋 Description

**ProjetFoncier** est une solution complète d'analyse des données foncières françaises (DVF) destinée aux investisseurs immobiliers locatifs. Le projet utilise Python et Jupyter Notebooks pour analyser les prix immobiliers, identifier les opportunités d'investissement et générer des recommandations personnalisées.

**Dernière mise à jour :** 16 septembre 2025  
**Volume analysé :** 26,914 transactions immobilières (2019-2023)  
**Zones couvertes :** Départements 91 et 94  

## 🎯 Objectifs

- **Explorer** les données foncières pour comprendre le marché immobilier français
- **Analyser** les prix au m², la typologie des biens et l'évolution temporelle
- **Identifier** les zones attractives pour l'investissement locatif
- **Visualiser** les données avec des graphiques et interfaces interactives
- **Recommander** des stratégies d'investissement basées sur des données réelles

## 📊 Résultats Clés Obtenus

### 🎯 **Indicateurs Principaux**
- **Prix moyen au m² :** 5,482€
- **Rendement locatif moyen :** 5.6% brut/an
- **Surface moyenne :** 75m²
- **Opportunités attractives :** 32% (rendement > 4%)

### 🏆 **Recommandations Principales**
- **Zone prioritaire :** Département 91 (rendement 6.2%)
- **Types recommandés :** Grandes maisons et grands appartements
- **Budget optimal :** 150k-400k€ selon profil investisseur

## 🗂️ Structure du Projet

```
ProjetFoncier/
├── 📁 assets/
│   └── dataset.csv              # Données DVF (2019-2023)
├── 📁 notebooks/
│   ├── 01_preprocessing.ipynb   # ✅ Nettoyage des données
│   ├── 02_analysis.ipynb        # ✅ Analyses statistiques  
│   ├── 03_visualizations.ipynb  # ✅ Tableaux de bord interactifs
│   └── 04_recommendations.ipynb # ✅ Recommandations d'investissement
├── 📁 src/
│   └── dvf_utils.py            # ✅ Modules utilitaires
├── 📁 outputs/
│   ├── 📁 visualizations/       # PNG et tableaux CSV
│   ├── 📁 recommendations/      # Rapports personnalisés
│   ├── 📁 reports/             # Rapports d'analyse complète
│   ├── dvf_cleaned_2019_2023.csv
│   ├── carte_interactive_transactions.html
│   └── heatmap_temporelle.html
├── requirements.txt            # Dépendances Python
├── validate_notebooks.py       # Script de validation
├── rapid_validation.py        # Test rapide d'intégrité
└── README.md                   # Cette documentation
```

## 🚀 Installation et Configuration

### 1. **Prérequis**
- Python 3.11+ (testé avec Python 3.13)
- Jupyter Notebook ou JupyterLab
- 4 Go RAM minimum (8 Go recommandés)

### 2. **Installation Rapide**

```bash
# Cloner le projet
git clone <url-du-repo>
cd ProjetFoncier

# Créer un environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. **Validation de l'Installation**

```bash
# Test rapide d'intégrité
python rapid_validation.py

# Validation complète des notebooks (optionnel)
python validate_notebooks.py
```

### 4. **Données DVF**
- ✅ **Données fournies :** Le projet inclut un dataset prétraité (26,914 transactions)
- 📁 **Localisation :** `assets/dataset.csv`
- 📊 **Couverture :** Départements 91 et 94 (2019-2023)

## 📖 Guide d'Utilisation

### ⚡ **Démarrage Rapide**

1. **Lancer Jupyter**
   ```bash
   jupyter lab
   # ou
   jupyter notebook
   ```

2. **Navigation recommandée :**
   - 🚀 **Commencer par :** `03_visualizations.ipynb` (interface interactive)
   - 📊 **Puis explorer :** `04_recommendations.ipynb` (recommandations finales)
   - 🔍 **Approfondir :** `02_analysis.ipynb` (analyses détaillées)
   - ⚙️ **Comprendre :** `01_preprocessing.ipynb` (nettoyage des données)

### 📋 **Workflow Détaillé**

#### **Option A : Exploration Interactive (Recommandé)**
```
03_visualizations.ipynb → 04_recommendations.ipynb
```
- ✅ Interface utilisateur intuitive
- ✅ Résultats immédiats
- ✅ Recommandations personnalisées

#### **Option B : Analyse Complète**
```
01_preprocessing.ipynb → 02_analysis.ipynb → 03_visualizations.ipynb → 04_recommendations.ipynb
```
- ✅ Compréhension approfondie
- ✅ Maîtrise de la méthodologie
- ✅ Personnalisation avancée

### 🎛️ **Fonctionnalités par Notebook**

#### **01_preprocessing.ipynb** ⚙️
- ✅ Chargement et validation des données DVF
- ✅ Nettoyage des valeurs aberrantes (98.2% de données conservées)
- ✅ Création de variables dérivées (prix/m², surface habitable, etc.)
- ✅ Export des données nettoyées : `outputs/dvf_cleaned_2019_2023.csv`

#### **02_analysis.ipynb** 📊
- ✅ Analyses géographiques (départements 91 vs 94)
- ✅ Évolution temporelle des prix (2019-2023)
- ✅ Comparaisons par type de bien (maisons, appartements)
- ✅ Identification des opportunités d'investissement

#### **03_visualizations.ipynb** 🎨
- ✅ **Tableau de bord principal** avec filtres interactifs
- ✅ **Simulateur d'investissement** pour calculs de rentabilité
- ✅ **Comparateur de départements** avec recommandations
- ✅ **Recherche avancée** d'opportunités d'investissement
- ✅ **Cartographie interactive** : `outputs/carte_interactive_transactions.html`

#### **04_recommendations.ipynb** 🎯
- ✅ Intégration de données de loyer réelles
- ✅ Calculs de rendement avec scoring multi-critères
- ✅ Recommandations personnalisées par profil (Débutant/Expérimenté/Aguerri)
- ✅ Rapport exécutif complet : `outputs/recommendations/resume_executif_complet.html`

## 💡 Exemples d'Usage

### 🔍 **Trouver les Meilleures Opportunités**
```python
# Dans 03_visualizations.ipynb
# 1. Sélectionner vos critères dans les widgets
# 2. Utiliser la "Recherche Avancée"
# 3. Définir : prix max, surface min, rendement min
# 4. Analyser les résultats par département
```

### 💰 **Simuler un Investissement**
```python
# Dans 03_visualizations.ipynb - Simulateur
# 1. Choisir le département cible
# 2. Définir surface et budget
# 3. Estimer le loyer au m²
# 4. Analyser la rentabilité calculée
```

### 📊 **Comparer des Zones**
```python
# Dans 03_visualizations.ipynb - Comparateur
# 1. Sélectionner 2-3 départements
# 2. Comparer prix, volume, stabilité
# 3. Obtenir une recommandation automatique
```

## � Données et Sources

### **Données DVF (Demandes de Valeurs Foncières)**
- **Source** : data.gouv.fr
- **Période** : 2019-2023
- **Couverture** : France métropolitaine
- **Variables clés** : prix, surface, localisation, date

### **Données de Loyer**
- **Source** : Observatoires locatifs régionaux
- **Couverture** : 80+ départements français
- **Usage** : Calculs de rendement réalistes

## 📈 Résultats et Livrables

### 📊 **Données Générées**
- ✅ `dvf_cleaned_2019_2023.csv` - Dataset nettoyé (26,914 transactions)
- ✅ `transactions_avec_rendements.csv` - Données enrichies avec calculs de rentabilité
- ✅ `recommandations_par_profil.csv` - Suggestions personnalisées par type d'investisseur
- ✅ `zones_attractives_classifiees.csv` - Classement des zones par attractivité

### 🖼️ **Visualisations**
- ✅ `vue_ensemble_marche.png` - Synthèse générale du marché
- ✅ `analyse_geographique.png` - Comparaison départements 91 vs 94
- ✅ `analyse_investissement.png` - Opportunités par segment de prix
- ✅ `carte_interactive_transactions.html` - Cartographie géolocalisée
- ✅ `heatmap_temporelle.html` - Évolution temporelle interactive

### 📑 **Rapports d'Analyse**
- ✅ `resume_executif_complet.html` - Rapport exécutif (version web)
- ✅ `resume_executif_complet.md` - Rapport exécutif (version markdown)
- ✅ `checklist_investisseur.md` - Guide pratique pour investisseurs
- ✅ `rapport_analyse_complete_dvf.html` - Rapport technique complet

### 🎯 **Recommandations Finales**

#### **Top 3 Opportunités Identifiées**
1. **Grand appartement 91** - 102,330€ (62m²) - **Rendement : 12.0%**
2. **Grand appartement 91** - 119,000€ (72m²) - **Rendement : 12.0%**  
3. **Grande maison 91** - 285,000€ (172m²) - **Rendement : 11.9%**

#### **Stratégie par Profil**
- 🌱 **Débutant** : Focus département 91, budget 80k-250k€, rendement > 4.5%
- 📈 **Expérimenté** : Les 2 départements, budget 150k-600k€, rendement > 5.5%
- 🚀 **Aguerri** : Focus département 94, budget 300k€+, rendement > 6.5%

## ⚠️ Limitations et Précautions

### **Données Historiques**
- ✅ Période analysée : 2019-2023 (données récentes)
- ⚠️ Tendances passées ne garantissent pas les performances futures
- 💡 Validation recommandée avec données locales actuelles

### **Calculs de Rendement**
- ✅ Basés sur données de loyer réelles (observatoires locatifs)
- ⚠️ Rendement **brut** uniquement (hors charges, taxes, vacances)
- 💡 Prévoir marge de sécurité de 15-20%

### **Recommandations**
- ✅ Outil d'aide à la décision basé sur 26,914 transactions
- ⚠️ Ne remplace pas un conseil en investissement personnalisé
- 💡 Validation nécessaire avec experts locaux

## 🛠️ Dépendances Techniques

### **Environnement Testé**
- ✅ Python 3.13.3
- ✅ Windows 11 / Linux / macOS
- ✅ Jupyter Lab / Jupyter Notebook

### **Packages Principaux**
```python
# Manipulation de données
pandas>=2.0.0           # DataFrames et analyses
numpy>=1.24.0           # Calculs numériques

# Visualisations
matplotlib>=3.7.0       # Graphiques statiques
seaborn>=0.12.0         # Visualisations statistiques
plotly>=5.15.0          # Graphiques interactifs
folium>=0.14.0          # Cartes géographiques

# Interface interactive
jupyter>=1.0.0          # Environnement notebook
ipywidgets>=8.0.0       # Widgets interactifs
nbconvert>=7.0.0        # Conversion notebooks

# Utilitaires
pathlib                 # Gestion des chemins
json                   # Traitement JSON
datetime               # Manipulation dates
```

### **Installation Complète**
```bash
# Toutes les dépendances (environnement complet)
pip install -r requirements.txt

# Installation minimale (exploration uniquement)
pip install pandas numpy matplotlib jupyter ipywidgets
```

## 🔧 Maintenance et Validation

### **Scripts de Validation Inclus**

#### **Test Rapide (`rapid_validation.py`)**
```bash
python rapid_validation.py
```
- ✅ Vérification des imports
- ✅ Test de lecture des données  
- ✅ Validation de la structure
- ⏱️ Exécution : < 30 secondes

#### **Validation Complète (`validate_notebooks.py`)**
```bash
python validate_notebooks.py
```
- ✅ Exécution complète des notebooks
- ✅ Détection des erreurs
- ✅ Rapport de validation
- ⏱️ Exécution : 10-15 minutes

### **Résolution de Problèmes**

#### **Erreur d'Encoding**
```bash
# Si problème de lecture CSV
# Le script gère automatiquement latin-1 et utf-8
```

#### **Widgets non Affichés**
```bash
# Réinstaller ipywidgets
pip install --upgrade ipywidgets
jupyter nbextension enable --py widgetsnbextension
```

#### **Problème de Mémoire**
```bash
# Réduire la taille d'échantillon dans les notebooks
# Variables sample_size disponibles
```

## 📞 Support et Ressources

### **Documentation Interne**
- 📖 README.md (ce fichier) - Guide complet
- 📝 Notebooks commentés - Documentation inline
- 🐍 `src/dvf_utils.py` - Docstrings détaillées
- 📊 `outputs/reports/` - Rapports d'analyse

### **Fichiers de Référence**
- 🎯 `outputs/recommendations/checklist_investisseur.md` - Guide pratique
- 📈 `outputs/reports/rapport_analyse_complete_dvf.html` - Rapport technique
- ✅ `outputs/rapid_validation_report.json` - Statut de validation

### **Ressources Externes**
- 📊 [Données DVF](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/) - Source officielle
- 📚 [Documentation Jupyter](https://jupyter.readthedocs.io/) - Guide utilisateur
- 🐼 [Documentation Pandas](https://pandas.pydata.org/docs/) - Manipulation données
- 📈 [Plotly Documentation](https://plotly.com/python/) - Visualisations interactives

---

## ✅ Status du Projet

**🎉 PROJET COMPLET ET VALIDÉ**

- ✅ **Données** : 26,914 transactions analysées
- ✅ **Notebooks** : 4 notebooks fonctionnels et documentés  
- ✅ **Visualisations** : 8 graphiques et cartes interactives
- ✅ **Recommandations** : 3 profils d'investisseurs avec suggestions personnalisées
- ✅ **Rapports** : Documentation complète et rapports exécutifs
- ✅ **Validation** : Tests automatisés et validation d'intégrité

### **Prochaines Étapes Suggérées**
1. 📊 Exploration avec le tableau de bord interactif (`03_visualizations.ipynb`)
2. 🎯 Lecture des recommandations personnalisées (`04_recommendations.ipynb`)
3. 📈 Analyse des opportunités identifiées dans les rapports
4. 🏠 Application des stratégies d'investissement recommandées

**🚀 Prêt à identifier vos prochaines opportunités d'investissement immobilier !**