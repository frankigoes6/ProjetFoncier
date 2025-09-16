# 🏠 ProjetFoncier - Analyse DVF pour Investissement Immobilier

**Analyse des données foncières françaises (DVF) pour l'inves---

## 📚 Ressources

**Documentation** : [data.gouv.fr - DVF](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)  
**Support** : Consultez les commentaires dans les notebooks pour plus de détails

---

> Interface interactive simple et efficace pour analyser le marché immobilier français

📊 **26,914 transactions analysées** • 🗓️ **Année 2024** • 📍 **Départements 91 & 94**

## 🎯 Objectif

Fournir aux investisseurs immobiliers une **analyse claire et interactive** des données DVF pour identifier les meilleures opportunités d'investissement locatif.

## 🚀 Démarrage Rapide

### 1. **Installation**
```bash
# Cloner le projet
git clone https://github.com/frankigoes6/ProjetFoncier.git
cd ProjetFoncier

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. **Utilisation**
```bash
# Lancer Jupyter
jupyter lab

# Ouvrir les notebooks dans l'ordre :
# 1. notebooks/01_preprocessing.ipynb     → Préparer les données
# 2. notebooks/02_application_investisseur.ipynb → Analyser et explorer
```

### 3. **Ce que vous obtenez**
- ✅ **Dashboard interactif** avec filtres temps réel
- ✅ **Analyses géographiques** par département et commune  
- ✅ **Recommandations d'investissement** personnalisées
- ✅ **Visualisations claires** des tendances de marché

## � Structure du Projet

```
ProjetFoncier/
├── 📁 assets/
│   └── dataset.csv                           # Données DVF brutes (26,914 transactions)
├── 📁 notebooks/
│   ├── 01_preprocessing.ipynb                # Nettoyage des données
│   └── 02_application_investisseur.ipynb     # Interface d'analyse complète
├── 📁 src/
│   └── dvf_utils.py                         # Fonctions utilitaires
├── 📁 outputs/
│   └── dvf_cleaned_2024.csv            # Données nettoyées (générées)
└── requirements.txt                          # Dépendances Python
```

### **Workflow Simple**
```
01_preprocessing.ipynb → 02_application_investisseur.ipynb
      (une fois)              (exploration interactive)
```

## 🎮 Interface Interactive

### **Dashboard Principal** (`02_application_investisseur.ipynb`)
- 🎛️ **Filtres interactifs** : Département, année, prix, surface
- 📊 **Graphiques dynamiques** : Mise à jour automatique avec les filtres
- 📈 **Analyses statistiques** : Prix médian, évolution temporelle, distribution
- 🎯 **Recommandations** : Suggestions basées sur votre profil d'investisseur

### **Fonctionnalités Clés**
```python
# Filtrage en temps réel
Département: [91, 94, Tous]
Années: [2024]
Prix: [50k€ - 1M€+]
Surface: [20m² - 200m²+]
Type: [Appartement, Maison]

# Résultats instantanés
→ 📊 Graphiques actualisés
→ � Statistiques par zone  
→ 🎯 Recommandations personnalisées
```

## � Exemples de Résultats

### **Indicateurs Clés du Marché**
- � **Prix médian** : 4,800€/m² (appartements) | 3,200€/m² (maisons)
- � **Zones attractives** : Évry, Créteil, Villeneuve-Saint-Georges  
- 📈 **Évolution** : +8% sur la période 2024
- 🏠 **Opportunités** : Maisons 100-200m² dans le 91

### **Recommandations Types**
```
🌱 Investisseur Débutant
└── Budget: 80k-250k€ | Dept: 91 | Type: Appartement 60-80m²

📈 Investisseur Expérimenté  
└── Budget: 150k-400k€ | Les 2 depts | Type: Maison 100-150m²

🚀 Investisseur Aguerri
└── Budget: 300k€+ | Dept: 94 | Type: Tous types selon opportunités
```

## � Prérequis Techniques

### **Environnement**
- **Python** : 3.11+ (testé avec 3.13)
- **Mémoire** : 4GB RAM minimum
- **OS** : Windows, macOS, Linux

### **Dépendances Principales**
```python
pandas>=2.0.0        # Manipulation des données
numpy>=1.24.0        # Calculs numériques  
matplotlib>=3.7.0    # Visualisations
jupyter>=1.0.0       # Environnement notebook
ipywidgets>=8.0.0    # Interface interactive
```

## ⚠️ Points d'Attention

- 📊 **Données historiques** : Période 2024, tendances passées ≠ performances futures
- 🏠 **Scope géographique** : Départements 91 & 94 uniquement
- 💡 **Usage recommandé** : Outil d'aide à la décision, validation locale conseillée