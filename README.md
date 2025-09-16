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
│   └── dataset.csv                    # Données DVF (2019-2023)
├── 📁 notebooks/
│   ├── 01_preprocessing.ipynb         # ✅ Nettoyage et préparation des données
│   └── 02_application_investisseur.ipynb # ✅ Analyse unifiée + visualisations + recommandations
├── 📁 src/
│   └── dvf_utils.py                  # ✅ Modules utilitaires
├── 📁 outputs/
│   ├── 📁 visualizations/             # PNG et tableaux CSV
│   ├── 📁 recommendations/            # Rapports personnalisés
│   ├── 📁 reports/                   # Rapports d'analyse complète
│   ├── dvf_cleaned_2019_2023.csv     # Dataset nettoyé
│   ├── carte_interactive_transactions.html
│   └── heatmap_temporelle.html
├── requirements.txt                   # Dépendances Python
└── README.md                         # Cette documentation
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
   - 🚀 **Commencer par :** `02_application_investisseur.ipynb` (interface interactive unifiée)
   - 🔍 **Approfondir :** `01_preprocessing.ipynb` (nettoyage des données)

### 📋 **Workflow Simplifié**

#### **Analyse Complète (Recommandé)**
```
01_preprocessing.ipynb → 02_application_investisseur.ipynb
```
- ✅ Interface utilisateur intuitive
- ✅ Analyse, visualisations et recommandations en un seul notebook
- ✅ Dashboard interactif avec widgets ipywidgets

### 🎛️ **Fonctionnalités par Notebook**

#### **01_preprocessing.ipynb** ⚙️
- ✅ Chargement et validation des données DVF
- ✅ Nettoyage des valeurs aberrantes (données conservées)
- ✅ Création de variables dérivées (prix/m², surface habitable, etc.)
- ✅ Export des données nettoyées : `outputs/dvf_cleaned_2019_2023.csv`

#### **02_application_investisseur.ipynb** 📊🎨🎯
- ✅ **Chargement des données nettoyées** du preprocessing
- ✅ **Analyses statistiques** géographiques et temporelles
- ✅ **Tableau de bord principal** avec filtres interactifs (ipywidgets)
- ✅ **Visualisations matplotlib** qui s'actualisent avec les filtres
- ✅ **Recommandations d'investissement** basées sur les données DVF
- ✅ **Conclusions pour investisseurs non-techniques**

## 💡 Exemples d'Usage

### 🔍 **Explorer les Données avec le Dashboard Interactif**
```python
# Dans 02_application_investisseur.ipynb
# 1. Utiliser les widgets pour filtrer par département, année, prix
# 2. Observer les graphiques matplotlib s'actualiser automatiquement
# 3. Analyser les statistiques dynamiques par zone
# 4. Identifier les tendances et opportunités
```

### 💰 **Analyser les Investissements**
```python
# Dans 02_application_investisseur.ipynb - Section Recommandations
# 1. Consulter les analyses par type de bien
# 2. Comprendre les métriques de rentabilité
# 3. Lire les conseils pour investisseurs non-techniques
# 4. Appliquer les recommandations basées sur DVF
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
matplotlib>=3.7.0       # Graphiques statiques (principal)
ipywidgets>=8.0.0       # Widgets interactifs

# Interface interactive
jupyter>=1.0.0          # Environnement notebook

# Utilitaires
pathlib                 # Gestion des chemins
json                   # Traitement JSON
datetime               # Manipulation dates
```

### **Installation Simplifiée**
```bash
# Dépendances essentielles (environnement simplifié)
pip install pandas numpy matplotlib jupyter ipywidgets

# Installation complète avec requirements.txt
pip install -r requirements.txt
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
1. 📊 Exploration avec le dashboard interactif unifié (`02_application_investisseur.ipynb`)
2. 🎯 Lecture des recommandations d'investissement dans le même notebook
3. � Compréhension du processus de nettoyage (`01_preprocessing.ipynb`)
4. 🏠 Application des stratégies d'investissement identifiées

**🚀 Workflow simplifié : 2 notebooks pour une analyse complète !**