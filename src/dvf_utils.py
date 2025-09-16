"""
Utilitaires pour l'analyse des données foncières DVF (Version Simplifiée)
"""
import pandas as pd


class DVFDataProcessor:
    """
    Classe pour le traitement des données DVF.
    Encapsule la logique de nettoyage utilisée par 01_preprocessing.ipynb.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_rows = len(df)
        self.cleaned_rows = 0

    def clean_data(self, start_year: int, end_year: int) -> pd.DataFrame:
        """Nettoie les données DVF selon les critères essentiels."""
        df_clean = self.df.copy()

        # Conversion et filtrage temporel
        df_clean['date_mutation'] = pd.to_datetime(df_clean['date_mutation'])
        df_clean['annee_mutation'] = df_clean['date_mutation'].dt.year
        df_clean = df_clean[
            (df_clean['annee_mutation'] >= start_year) & (df_clean['annee_mutation'] <= end_year)
        ]

        # Nettoyage des valeurs critiques pour l'analyse d'investissement
        critical_cols = ['valeur_fonciere', 'surface_reelle_bati']
        df_clean.dropna(subset=critical_cols, inplace=True)
        df_clean = df_clean[(df_clean['valeur_fonciere'] > 1000) & (df_clean['surface_reelle_bati'] > 0)]

        # Création de la variable 'prix_m2'
        df_clean['prix_m2'] = df_clean['valeur_fonciere'] / df_clean['surface_reelle_bati']

        # Suppression des outliers de prix/m² pour la lisibilité des graphiques
        df_clean = df_clean[(df_clean['prix_m2'] >= 100) & (df_clean['prix_m2'] <= 50000)]
        
        self.cleaned_rows = len(df_clean)
        return df_clean

    def get_cleaning_report(self) -> dict:
        """Génère un rapport de nettoyage."""
        removed_rows = self.original_rows - self.cleaned_rows
        removal_percentage = (removed_rows / self.original_rows * 100) if self.original_rows > 0 else 0
        return {
            "original_rows": self.original_rows,
            "cleaned_rows": self.cleaned_rows,
            "removed_rows": removed_rows,
            "removal_percentage": round(removal_percentage, 2),
        }


def load_dvf_data(file_path: str) -> pd.DataFrame:
    """Charge les données DVF en testant plusieurs encodages."""
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, low_memory=False, encoding=encoding, sep=';')
            print(f"✅ Données chargées avec encodage {encoding} : {df.shape[0]} lignes, {df.shape[1]} colonnes")
            
            # Conversion automatique de la date si présente
            if 'date_mutation' in df.columns:
                df['date_mutation'] = pd.to_datetime(df['date_mutation'])
                print(f"📅 Période couverte : {df['date_mutation'].min()} à {df['date_mutation'].max()}")
            
            return df
        except UnicodeDecodeError:
            continue
    
    # Si aucun encodage ne fonctionne, essayer avec errors='ignore'
    try:
        df = pd.read_csv(file_path, low_memory=False, encoding='utf-8', errors='ignore', sep=';')
        print(f"✅ Données chargées avec encodage UTF-8 (errors='ignore') : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        
        if 'date_mutation' in df.columns:
            df['date_mutation'] = pd.to_datetime(df['date_mutation'])
            print(f"📅 Période couverte : {df['date_mutation'].min()} à {df['date_mutation'].max()}")
        
        return df
    except Exception as e:
        raise ValueError(f"Impossible de charger le fichier avec les encodages courants. Erreur: {e}")