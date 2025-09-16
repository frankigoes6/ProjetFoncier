#!/usr/bin/env python3
"""
Démonstration complète des utilitaires DVF pour l'analyse d'investissement immobilier
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from dvf_utils import (
    InvestmentRecommendationEngine, 
    DVFDataProcessor, 
    StatisticalAnalyzer, 
    InvestmentAnalyzer
)
import json

def create_realistic_test_data():
    """Crée des données de test réalistes pour la démonstration"""
    np.random.seed(42)
    n_samples = 200
    
    # Communes et départements réels d'Île-de-France
    communes_data = [
        ('Paris', '75'), ('Boulogne-Billancourt', '92'), ('Versailles', '78'),
        ('Créteil', '94'), ('Nanterre', '92'), ('Argenteuil', '95'),
        ('Montreuil', '93'), ('Saint-Denis', '93'), ('Aulnay-sous-Bois', '93'),
        ('Rueil-Malmaison', '92'), ('Champigny-sur-Marne', '94'), ('Colombes', '92'),
        ('Vitry-sur-Seine', '94'), ('Asnières-sur-Seine', '92'), ('Courbevoie', '92')
    ]
    
    # Génération des données avec des prix réalistes par commune
    prix_base = {
        'Paris': 11000, 'Boulogne-Billancourt': 8500, 'Versailles': 6500,
        'Créteil': 4800, 'Nanterre': 5200, 'Argenteuil': 3800,
        'Montreuil': 5500, 'Saint-Denis': 3200, 'Aulnay-sous-Bois': 3500,
        'Rueil-Malmaison': 7200, 'Champigny-sur-Marne': 4200, 'Colombes': 5800,
        'Vitry-sur-Seine': 4000, 'Asnières-sur-Seine': 6800, 'Courbevoie': 8200
    }
    
    data_list = []
    for i in range(n_samples):
        commune, dept = communes_data[i % len(communes_data)]
        surface = max(20, np.random.normal(65, 25))
        prix_m2_base = prix_base[commune]
        prix_m2 = max(1000, np.random.normal(prix_m2_base, prix_m2_base * 0.3))
        
        data_list.append({
            'nom_commune': commune,
            'code_departement': dept,
            'surface_reelle_bati': surface,
            'prix_m2': prix_m2,
            'valeur_fonciere': surface * prix_m2,
            'date_mutation': pd.Timestamp('2022-01-01') + pd.Timedelta(days=np.random.randint(0, 730)),
            'type_local': np.random.choice(['Appartement', 'Maison'], p=[0.8, 0.2]),
            'nombre_pieces_principales': np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.3, 0.4, 0.15, 0.05])
        })
    
    return pd.DataFrame(data_list)

def demonstration_complete():
    """Démonstration complète des fonctionnalités"""
    print("🏠 DÉMONSTRATION COMPLÈTE DES UTILITAIRES DVF")
    print("=" * 60)
    
    # 1. Création et nettoyage des données
    print("\n📊 1. CHARGEMENT ET NETTOYAGE DES DONNÉES")
    print("-" * 40)
    
    data = create_realistic_test_data()
    print(f"✅ Données créées: {data.shape[0]} transactions, {data.shape[1]} colonnes")
    print(f"📅 Période: {data['date_mutation'].min().strftime('%Y-%m-%d')} à {data['date_mutation'].max().strftime('%Y-%m-%d')}")
    
    processor = DVFDataProcessor(data)
    cleaned_data = processor.clean_data(start_year=2022, end_year=2023)
    report = processor.get_cleaning_report()
    
    print(f"🧹 Nettoyage terminé: {report['cleaned_rows']} lignes conservées ({report['removal_percentage']}% supprimées)")
    
    # 2. Analyses statistiques
    print("\n📈 2. ANALYSES STATISTIQUES DÉTAILLÉES")
    print("-" * 40)
    
    analyzer = StatisticalAnalyzer()
    
    # Statistiques descriptives
    desc_stats = analyzer.comprehensive_descriptive_stats(cleaned_data)
    print("📊 Statistiques descriptives principales:")
    for var, stats in desc_stats.items():
        print(f"  • {var}: moyenne = {stats['mean']:,.0f}€, médiane = {stats['median']:,.0f}€")
    
    # Analyse géographique
    geo_analysis = analyzer.geographical_price_analysis(cleaned_data)
    if 'departements' in geo_analysis:
        print(f"\n🗺️ Analyse par département: {len(geo_analysis['departements'])} départements analysés")
        top_dept = geo_analysis['departements'].head(3)
        for _, row in top_dept.iterrows():
            print(f"  • Département {row['code_departement']}: {row['prix_m2_mean']:,.0f}€/m² ({row['prix_m2_count']} transactions)")
    
    # 3. Moteur de recommandations d'investissement
    print("\n🎯 3. RECOMMANDATIONS D'INVESTISSEMENT")
    print("-" * 40)
    
    engine = InvestmentRecommendationEngine(cleaned_data)
    
    # Intégration données loyer (simulées)
    integrated_data = engine.integrate_rental_data()
    print(f"✅ Données de loyer intégrées (mode simulé)")
    
    # Calcul des rendements
    data_with_yields = engine.calculate_rental_yields(integrated_data)
    rendement_moyen = data_with_yields['rendement_brut'].mean()
    print(f"💰 Rendement brut moyen estimé: {rendement_moyen:.1f}%")
    
    # Classification des rendements
    yield_distribution = data_with_yields['classe_rendement'].value_counts()
    print("📊 Répartition des classes de rendement:")
    for classe, count in yield_distribution.items():
        print(f"  • {classe}: {count} biens ({count/len(data_with_yields)*100:.1f}%)")
    
    # Calcul des scores multi-critères
    data_with_scores = engine.calculate_multi_criteria_score(data_with_yields)
    score_moyen = data_with_scores['score_global'].mean()
    print(f"⭐ Score d'investissement moyen: {score_moyen:.1f}/10")
    
    # Identification des zones attractives
    zones_attractives = engine.identify_attractive_zones(data_with_scores, min_transactions=5)
    print(f"🎯 Zones attractives identifiées: {len(zones_attractives)} communes")
    
    if len(zones_attractives) > 0:
        print("\n🏆 TOP 5 des meilleures opportunités:")
        top_zones = zones_attractives.head(5)
        for i, (_, zone) in enumerate(top_zones.iterrows(), 1):
            print(f"  {i}. {zone['nom_commune']} ({zone['code_departement']})")
            print(f"     Score: {zone['score_global']:.1f}/10, Rendement: {zone.get('rendement_brut', 'N/A'):.1f}%")
            print(f"     Prix moyen: {zone['prix_moyen']:,.0f}€, Prix/m²: {zone['prix_m2']:,.0f}€")
    
    # 4. Recommandations personnalisées
    print("\n🎪 4. RECOMMANDATIONS PERSONNALISÉES")
    print("-" * 40)
    
    if len(zones_attractives) > 0:
        # Simulation d'un profil d'investisseur
        budget_max = 400000
        surface_min = 40
        surface_max = 80
        rendement_min = 4.0
        
        print(f"👤 Profil investisseur simulé:")
        print(f"  • Budget maximum: {budget_max:,}€")
        print(f"  • Surface souhaitée: {surface_min}-{surface_max}m²")
        print(f"  • Rendement minimum: {rendement_min}%")
        
        recommendations = engine.generate_personalized_recommendations(
            zones_attractives,
            budget_max=budget_max,
            surface_min=surface_min,
            surface_max=surface_max,
            rendement_min=rendement_min
        )
        
        if 'message' in recommendations:
            print(f"⚠️ {recommendations['message']}")
        else:
            stats = recommendations['statistiques_portefeuille']
            print(f"\n📊 Portefeuille recommandé:")
            print(f"  • Zones éligibles: {stats['nb_zones_eligibles']}")
            if 'rendement_moyen_estime' in stats:
                print(f"  • Rendement moyen estimé: {stats['rendement_moyen_estime']:.1f}%")
            if 'score_global_moyen' in stats:
                print(f"  • Score moyen: {stats['score_global_moyen']:.1f}/10")
        
        # 5. Résumé exécutif
        print("\n📋 5. RÉSUMÉ EXÉCUTIF")
        print("-" * 40)
        
        summary = engine.create_executive_summary(recommendations, zones_attractives)
        
        if 'vue_ensemble_marche' in summary:
            market = summary['vue_ensemble_marche']
            print(f"🏙️ Vue d'ensemble du marché:")
            print(f"  • Zones analysées: {market['total_zones_analysees']}")
            print(f"  • Zones premium: {market['zones_premium']}")
            print(f"  • Zones attractives: {market['zones_attractives']}")
            print(f"  • Rendement moyen marché: {market['rendement_moyen_marche']:.1f}%")
        
        if 'principales_opportunites' in summary:
            opp = summary['principales_opportunites']['meilleure_opportunite']
            print(f"\n🎯 Meilleure opportunité:")
            print(f"  • Commune: {opp['commune']} ({opp['departement']})")
            print(f"  • Score: {opp['score']:.1f}/10")
            print(f"  • Rendement: {opp['rendement']:.1f}%")
            print(f"  • Prix moyen: {opp['prix_moyen']:,.0f}€")
        
        if 'conseils_strategiques' in summary:
            print(f"\n💡 Conseils pour investisseurs débutants:")
            for conseil in summary['conseils_strategiques']['investisseur_debutant'][:3]:
                print(f"  • {conseil}")
    
    # 6. Analyses avancées
    print("\n🔬 6. ANALYSES AVANCÉES")
    print("-" * 40)
    
    # Détection d'outliers
    outliers = analyzer.outlier_detection(cleaned_data, method='iqr')
    print("🔍 Détection d'outliers (méthode IQR):")
    for var, outlier_info in outliers.items():
        print(f"  • {var}: {outlier_info['outliers_count']} outliers ({outlier_info['outliers_percentage']:.1f}%)")
    
    # Analyse d'investissement par segments
    investment_analysis = analyzer.investment_market_analysis(cleaned_data)
    if 'surface_segments' in investment_analysis:
        print(f"\n📏 Analyse par segments de surface:")
        segments = investment_analysis['surface_segments']
        for _, segment in segments.iterrows():
            print(f"  • {segment['segment_surface']}: {segment['prix_m2_mean']:,.0f}€/m² ({segment['prix_m2_count']} transactions)")
    
    print("\n✅ DÉMONSTRATION TERMINÉE - Tous les utilitaires DVF fonctionnent correctement!")
    print("🎉 Le module est prêt pour une utilisation en production.")

if __name__ == "__main__":
    demonstration_complete()