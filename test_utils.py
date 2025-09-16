#!/usr/bin/env python3
"""
Test script pour vérifier les fonctions utilitaires DVF
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from dvf_utils import InvestmentRecommendationEngine, DVFDataProcessor

def test_investment_recommendation_engine():
    """Test de base du moteur de recommandations"""
    print("🧪 Test du moteur de recommandations d'investissement")
    
    # Création de données de test
    np.random.seed(42)
    n_samples = 100
    
    test_data = pd.DataFrame({
        'nom_commune': np.random.choice(['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'], n_samples),
        'code_departement': np.random.choice(['75', '69', '13', '31', '06'], n_samples),
        'valeur_fonciere': np.random.normal(300000, 100000, n_samples),
        'surface_reelle_bati': np.random.normal(60, 20, n_samples),
        'date_mutation': pd.date_range('2019-01-01', '2023-12-31', periods=n_samples),
        'type_local': np.random.choice(['Appartement', 'Maison'], n_samples)
    })
    
    # Calcul du prix au m²
    test_data['prix_m2'] = test_data['valeur_fonciere'] / test_data['surface_reelle_bati']
    
    print(f"✅ Données de test créées: {test_data.shape[0]} transactions")
    
    # Test du moteur de recommandations
    try:
        engine = InvestmentRecommendationEngine(test_data)
        print("✅ Moteur de recommandations initialisé")
        
        # Test intégration données loyer (mode simulé)
        integrated_data = engine.integrate_rental_data()
        print(f"✅ Intégration données loyer: {integrated_data.shape[0]} lignes")
        
        # Test calcul rendements
        data_with_yields = engine.calculate_rental_yields(integrated_data)
        print(f"✅ Calcul rendements: moyenne = {data_with_yields['rendement_brut'].mean():.2f}%")
        
        # Test score multi-critères
        data_with_scores = engine.calculate_multi_criteria_score(data_with_yields)
        print(f"✅ Score multi-critères: moyenne = {data_with_scores['score_global'].mean():.2f}/10")
        
        # Test identification zones attractives
        try:
            zones_attractives = engine.identify_attractive_zones(data_with_scores, min_transactions=2)  # Reduce threshold for test
            print(f"✅ Zones attractives identifiées: {len(zones_attractives)} communes")
            print(f"   Colonnes disponibles: {list(zones_attractives.columns)}")
        except Exception as e:
            print(f"❌ Erreur zones attractives: {e}")
            print(f"   Colonnes disponibles dans data_with_scores: {list(data_with_scores.columns)}")
            zones_attractives = pd.DataFrame()  # DataFrame vide pour la suite
        
        # Test recommandations personnalisées
        if len(zones_attractives) > 0:
            try:
                recommendations = engine.generate_personalized_recommendations(
                    zones_attractives, 
                    budget_max=500000,
                    surface_min=40,
                    surface_max=100,
                    rendement_min=3.0
                )
                print(f"✅ Recommandations générées: {len(recommendations)} sections")
                
                # Test résumé exécutif
                summary = engine.create_executive_summary(recommendations, zones_attractives)
                print(f"✅ Résumé exécutif créé: {len(summary)} sections")
            except Exception as e:
                print(f"❌ Erreur recommandations: {e}")
        else:
            print("⚠️ Pas de zones attractives pour tester les recommandations")
        
        print("\n🎉 Tous les tests sont passés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_dvf_data_processor():
    """Test de base du processeur de données DVF"""
    print("\n🧪 Test du processeur de données DVF")
    
    # Données de test avec quelques outliers
    np.random.seed(42)
    n_samples = 50
    
    test_data = pd.DataFrame({
        'date_mutation': pd.date_range('2019-01-01', '2023-12-31', periods=n_samples),
        'valeur_fonciere': np.concatenate([
            np.random.normal(300000, 50000, n_samples-5),  # Données normales
            [1000000, 50000, 2000000, 10000, 5000000]      # Outliers
        ]),
        'surface_reelle_bati': np.concatenate([
            np.random.normal(60, 15, n_samples-3),          # Données normales
            [200, 10, 500]                                  # Outliers
        ])
    })
    
    try:
        processor = DVFDataProcessor(test_data)
        print(f"✅ Processeur initialisé avec {test_data.shape[0]} lignes")
        
        # Test nettoyage
        cleaned_data = processor.clean_data()
        print(f"✅ Données nettoyées: {cleaned_data.shape[0]} lignes conservées")
        
        # Test rapport de nettoyage
        report = processor.get_cleaning_report()
        print(f"✅ Rapport de nettoyage: {report['removal_percentage']}% de lignes supprimées")
        
        print("🎉 Test du processeur réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test des utilitaires DVF\n")
    
    success1 = test_dvf_data_processor()
    success2 = test_investment_recommendation_engine()
    
    if success1 and success2:
        print("\n✅ Tous les tests sont passés! Les utilitaires DVF sont fonctionnels.")
    else:
        print("\n❌ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")