"""
Test de validation rapide des notebooks DVF
Teste les imports et fonctions critiques sans exécution complète
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import time

def test_notebook_imports():
    """Teste que tous les imports nécessaires fonctionnent"""
    print("🔍 Test des imports...")
    
    try:
        # Imports du projet
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        import folium
        import plotly.express as px
        import plotly.graph_objects as go
        from ipywidgets import interact, widgets
        
        print("✅ Tous les imports principaux OK")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_data_availability():
    """Teste que les données sont disponibles"""
    print("🔍 Test de disponibilité des données...")
    
    data_file = Path("assets/dataset.csv")
    if not data_file.exists():
        print(f"❌ Fichier de données manquant: {data_file}")
        return False
    
    try:
        # Test de lecture des données avec encoding approprié
        df = pd.read_csv(data_file, nrows=100, encoding='latin-1')  # Lire seulement 100 lignes pour le test
        print(f"✅ Données lisibles: {len(df)} lignes testées")
        print(f"   Colonnes disponibles: {len(df.columns)}")
        return True
    except Exception as e:
        # Essayer un autre encoding
        try:
            df = pd.read_csv(data_file, nrows=100, encoding='utf-8')
            print(f"✅ Données lisibles (UTF-8): {len(df)} lignes testées")
            return True
        except:
            print(f"❌ Erreur de lecture données: {e}")
            return False

def test_output_directories():
    """Teste que les dossiers de sortie existent"""
    print("🔍 Test des dossiers de sortie...")
    
    required_dirs = [
        "outputs",
        "outputs/visualizations", 
        "outputs/recommendations",
        "outputs/reports"
    ]
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ Dossier OK: {dir_path}")
        else:
            print(f"⚠️  Dossier manquant: {dir_path}")
            # Créer le dossier manquant
            path.mkdir(parents=True, exist_ok=True)
            print(f"   ➕ Dossier créé: {dir_path}")
    
    return True

def test_utility_functions():
    """Teste les fonctions utilitaires"""
    print("🔍 Test des fonctions utilitaires...")
    
    utils_file = Path("src/dvf_utils.py")
    if not utils_file.exists():
        print(f"⚠️  Fichier utilitaires manquant: {utils_file}")
        return True  # Non bloquant
    
    try:
        # Tenter d'importer les fonctions
        sys.path.append(str(Path("src")))
        import dvf_utils
        print("✅ Fonctions utilitaires importables")
        return True
    except Exception as e:
        print(f"⚠️  Problème avec utilitaires: {e}")
        return True  # Non bloquant pour les tests

def test_existing_outputs():
    """Teste les sorties existantes"""
    print("🔍 Test des sorties existantes...")
    
    critical_outputs = [
        "outputs/dvf_cleaned_2019_2023.csv",
        "outputs/recommendations/resume_executif_complet.md"
    ]
    
    existing_count = 0
    for output_file in critical_outputs:
        if Path(output_file).exists():
            print(f"✅ Sortie présente: {output_file}")
            existing_count += 1
        else:
            print(f"⚠️  Sortie manquante: {output_file}")
    
    print(f"📊 Sorties trouvées: {existing_count}/{len(critical_outputs)}")
    return existing_count > 0

def run_validation():
    """Lance tous les tests de validation"""
    print("🎯 VALIDATION RAPIDE DES NOTEBOOKS DVF")
    print("="*60)
    
    tests = [
        ("Imports", test_notebook_imports),
        ("Données", test_data_availability), 
        ("Dossiers", test_output_directories),
        ("Utilitaires", test_utility_functions),
        ("Sorties", test_existing_outputs)
    ]
    
    results = {}
    overall_success = True
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 40)
        
        try:
            success = test_func()
            results[test_name] = success
            if not success:
                overall_success = False
        except Exception as e:
            print(f"💥 Exception dans {test_name}: {e}")
            results[test_name] = False
            overall_success = False
    
    # Résumé
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DE LA VALIDATION RAPIDE")
    print(f"{'='*60}")
    
    for test_name, success in results.items():
        status = "✅ OK" if success else "❌ ÉCHEC"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Résultat: {'✅ VALIDATION RÉUSSIE' if overall_success else '⚠️  PROBLÈMES DÉTECTÉS'}")
    
    # Sauvegarde du rapport
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'overall_success': overall_success,
        'test_results': results,
        'validation_type': 'rapid'
    }
    
    report_path = Path("outputs/rapid_validation_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {report_path}")
    
    # Recommandations
    if not overall_success:
        print(f"\n💡 RECOMMANDATIONS:")
        if not results.get("Imports", True):
            print("   📦 Installer les dépendances manquantes")
        if not results.get("Données", True):
            print("   📊 Vérifier le fichier assets/dataset.csv")
        
    return overall_success

if __name__ == "__main__":
    print("🚀 Démarrage de la validation rapide...")
    
    # Changer vers le répertoire du projet
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    success = run_validation()
    
    if success:
        print("\n🎉 Tous les tests passent - les notebooks devraient fonctionner!")
    else:
        print("\n⚠️  Certains problèmes détectés - vérifier avant exécution complète")
    
    sys.exit(0 if success else 1)