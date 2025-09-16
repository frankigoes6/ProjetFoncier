#!/usr/bin/env python3
"""
Script de validation des notebooks DVF
Teste l'exécution de tous les notebooks dans l'ordre correct
"""

import subprocess
import sys
import os
from pathlib import Path
import json
import time

def run_notebook(notebook_path):
    """Exécute un notebook et retourne le status"""
    print(f"\n{'='*60}")
    print(f"🔄 Exécution de {notebook_path.name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Exécuter le notebook avec nbconvert
        result = subprocess.run([
            'C:/Users/vtnde/Documents/Projets/ProjetFoncier/venv/Scripts/jupyter.exe', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--inplace',
            '--ExecutePreprocessor.timeout=300',
            str(notebook_path)
        ], capture_output=True, text=True, timeout=600)
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ SUCCÈS - {notebook_path.name} ({execution_time:.1f}s)")
            return True, None, execution_time
        else:
            print(f"❌ ERREUR - {notebook_path.name}")
            print(f"STDERR: {result.stderr}")
            return False, result.stderr, execution_time
            
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"⏰ TIMEOUT - {notebook_path.name} ({execution_time:.1f}s)")
        return False, "Timeout after 10 minutes", execution_time
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"💥 EXCEPTION - {notebook_path.name}: {str(e)}")
        return False, str(e), execution_time

def validate_notebooks():
    """Valide tous les notebooks dans l'ordre"""
    
    # Définir l'ordre d'exécution
    notebooks_order = [
        '01_preprocessing.ipynb',
        '02_analysis.ipynb', 
        '03_visualizations.ipynb',
        '04_recommendations.ipynb'
    ]
    
    # Chemin vers les notebooks
    notebooks_dir = Path(__file__).parent / 'notebooks'
    
    if not notebooks_dir.exists():
        print(f"❌ Dossier notebooks non trouvé: {notebooks_dir}")
        return False
    
    print("🎯 VALIDATION DES NOTEBOOKS DVF")
    print("="*60)
    print(f"📁 Dossier: {notebooks_dir}")
    print(f"📋 Notebooks à tester: {len(notebooks_order)}")
    
    results = {}
    total_time = 0
    overall_success = True
    
    for notebook_name in notebooks_order:
        notebook_path = notebooks_dir / notebook_name
        
        if not notebook_path.exists():
            print(f"❌ Notebook non trouvé: {notebook_path}")
            results[notebook_name] = {'success': False, 'error': 'File not found', 'time': 0}
            overall_success = False
            continue
        
        success, error, exec_time = run_notebook(notebook_path)
        total_time += exec_time
        
        results[notebook_name] = {
            'success': success,
            'error': error,
            'time': exec_time
        }
        
        if not success:
            overall_success = False
            print(f"⚠️  Arrêt à cause de l'erreur dans {notebook_name}")
            break
    
    # Résumé final
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DE LA VALIDATION")
    print(f"{'='*60}")
    
    for notebook_name, result in results.items():
        status = "✅ SUCCÈS" if result['success'] else "❌ ÉCHEC"
        time_str = f"{result['time']:.1f}s"
        print(f"{status} - {notebook_name:<25} ({time_str})")
        if not result['success'] and result['error']:
            print(f"    🔍 Erreur: {result['error'][:100]}...")
    
    print(f"\n⏱️  Temps total: {total_time:.1f}s")
    print(f"🎯 Résultat global: {'✅ TOUS LES NOTEBOOKS VALIDÉS' if overall_success else '❌ VALIDATION ÉCHOUÉE'}")
    
    # Sauvegarder le rapport
    report_path = Path(__file__).parent / 'outputs' / 'validation_report.json'
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'overall_success': overall_success,
            'total_time': total_time,
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {report_path}")
    
    return overall_success

if __name__ == "__main__":
    print("🚀 Démarrage de la validation des notebooks...")
    
    # Vérifier que jupyter est installé
    try:
        subprocess.run(['C:/Users/vtnde/Documents/Projets/ProjetFoncier/venv/Scripts/jupyter.exe', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Jupyter n'est pas installé ou accessible")
        print("💡 Installez avec: pip install jupyter")
        sys.exit(1)
    
    success = validate_notebooks()
    sys.exit(0 if success else 1)