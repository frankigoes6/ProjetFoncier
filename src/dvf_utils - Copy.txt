"""
Utilitaires pour l'analyse des données foncières DVF
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import stats
import warnings

warnings.filterwarnings("ignore")


class DVFDataProcessor:
    """
    Classe pour le traitement des données DVF
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialise le processeur avec un DataFrame DVF

        Args:
            df: DataFrame contenant les données DVF
        """
        self.df = df.copy()
        self.original_shape = df.shape

    def clean_data(self, start_year: int = 2019, end_year: int = 2023) -> pd.DataFrame:
        """
        Nettoie les données DVF selon les critères définis

        Args:
            start_year: Année de début pour le filtrage
            end_year: Année de fin pour le filtrage

        Returns:
            DataFrame nettoyé
        """
        df_clean = self.df.copy()

        # Conversion de la date
        if "date_mutation" in df_clean.columns:
            df_clean["date_mutation"] = pd.to_datetime(df_clean["date_mutation"])
            df_clean["annee_mutation"] = df_clean["date_mutation"].dt.year

            # Filtrage temporel
            df_clean = df_clean[
                (df_clean["annee_mutation"] >= start_year)
                & (df_clean["annee_mutation"] <= end_year)
            ]

        # Nettoyage des valeurs critiques
        critical_cols = ["valeur_fonciere", "surface_reelle_bati"]
        for col in critical_cols:
            if col in df_clean.columns:
                df_clean = df_clean.dropna(subset=[col])
                df_clean = df_clean[df_clean[col] > 0]

        # Calcul du prix au m²
        if all(col in df_clean.columns for col in critical_cols):
            df_clean["prix_m2"] = (
                df_clean["valeur_fonciere"] / df_clean["surface_reelle_bati"]
            )

            # Suppression des outliers extrêmes (prix au m² > 50000€ ou < 100€)
            df_clean = df_clean[
                (df_clean["prix_m2"] >= 100) & (df_clean["prix_m2"] <= 50000)
            ]

        self.df_clean = df_clean
        return df_clean

    def get_cleaning_report(self) -> Dict:
        """
        Génère un rapport de nettoyage

        Returns:
            Dictionnaire avec les statistiques de nettoyage
        """
        if not hasattr(self, "df_clean"):
            raise ValueError("Veuillez d'abord exécuter clean_data()")

        return {
            "original_rows": self.original_shape[0],
            "cleaned_rows": self.df_clean.shape[0],
            "removed_rows": self.original_shape[0] - self.df_clean.shape[0],
            "removal_percentage": round(
                (self.original_shape[0] - self.df_clean.shape[0])
                / self.original_shape[0]
                * 100,
                2,
            ),
        }


class RentabilityCalculator:
    """
    Classe pour calculer la rentabilité immobilière
    """

    @staticmethod
    def estimate_rental_yield(prix_achat: float, loyer_mensuel_estime: float) -> float:
        """
        Calcule le rendement brut estimé

        Args:
            prix_achat: Prix d'achat du bien
            loyer_mensuel_estime: Loyer mensuel estimé

        Returns:
            Rendement brut en pourcentage
        """
        if prix_achat <= 0 or loyer_mensuel_estime <= 0:
            return np.nan

        loyer_annuel = loyer_mensuel_estime * 12
        return (loyer_annuel / prix_achat) * 100

    @staticmethod
    def estimate_monthly_rent(surface_m2: float, loyer_m2_moyen: float) -> float:
        """
        Estime le loyer mensuel basé sur la surface et le loyer au m² moyen

        Args:
            surface_m2: Surface du bien en m²
            loyer_m2_moyen: Loyer moyen au m² dans la zone

        Returns:
            Loyer mensuel estimé
        """
        if surface_m2 <= 0 or loyer_m2_moyen <= 0:
            return np.nan

        return surface_m2 * loyer_m2_moyen


class GeographicAnalyzer:
    """
    Classe pour les analyses géographiques
    """

    @staticmethod
    def get_top_communes(
        df: pd.DataFrame,
        metric: str = "prix_m2",
        n_top: int = 10,
        ascending: bool = False,
    ) -> pd.DataFrame:
        """
        Obtient le top des communes selon une métrique

        Args:
            df: DataFrame avec les données
            metric: Métrique à utiliser pour le classement
            n_top: Nombre de communes à retourner
            ascending: Ordre croissant ou décroissant

        Returns:
            DataFrame avec le top des communes
        """
        if metric not in df.columns:
            raise ValueError(f"La colonne {metric} n'existe pas")

        result = df.groupby("nom_commune")[metric].agg(["mean", "count"]).reset_index()

        result.columns = ["commune", f"{metric}_moyen", "nb_transactions"]

        # Filtrer les communes avec au moins 5 transactions
        result = result[result["nb_transactions"] >= 5]

        return (
            result.sort_values(f"{metric}_moyen", ascending=ascending)
            .head(n_top)
            .reset_index(drop=True)
        )

    @staticmethod
    def get_market_summary(
        df: pd.DataFrame, group_by: str = "nom_commune"
    ) -> pd.DataFrame:
        """
        Génère un résumé du marché par zone géographique

        Args:
            df: DataFrame avec les données DVF nettoyées
            group_by: Colonne de regroupement ('nom_commune', 'code_departement', etc.)

        Returns:
            DataFrame avec les statistiques par zone
        """
        if group_by not in df.columns:
            raise ValueError(f"La colonne {group_by} n'existe pas")

        summary = (
            df.groupby(group_by)
            .agg(
                {
                    "valeur_fonciere": ["count", "mean", "median"],
                    "prix_m2": ["mean", "median", "std"],
                    "surface_reelle_bati": ["mean", "median"],
                }
            )
            .round(2)
        )

        # Aplatir les colonnes multi-index
        summary.columns = ["_".join(col).strip() for col in summary.columns.values]
        summary = summary.reset_index()

        # Renommer les colonnes pour plus de clarté
        rename_dict = {
            "valeur_fonciere_count": "nb_transactions",
            "valeur_fonciere_mean": "prix_moyen",
            "valeur_fonciere_median": "prix_median",
            "prix_m2_mean": "prix_m2_moyen",
            "prix_m2_median": "prix_m2_median",
            "prix_m2_std": "prix_m2_volatilite",
            "surface_reelle_bati_mean": "surface_moyenne",
            "surface_reelle_bati_median": "surface_mediane",
        }

        summary = summary.rename(columns=rename_dict)

        # Filtrer les zones avec au moins 5 transactions
        summary = summary[summary["nb_transactions"] >= 5]

        return summary.sort_values("nb_transactions", ascending=False)


class InvestmentAnalyzer:
    """
    Classe pour l'analyse d'investissement immobilier
    """

    @staticmethod
    @staticmethod
    def _calculate_price_score(prix_m2: float, prix_m2_moyen_zone: float) -> int:
        """Calcule le score basé sur le prix par rapport à la moyenne de la zone"""
        ratio_prix = prix_m2 / prix_m2_moyen_zone
        if ratio_prix <= 0.8:
            return 5  # Très bon
        elif ratio_prix <= 0.9:
            return 4  # Bon
        elif ratio_prix <= 1.1:
            return 3  # Moyen
        elif ratio_prix <= 1.2:
            return 2  # Cher
        else:
            return 1  # Très cher

    @staticmethod
    def _calculate_liquidity_score(nb_transactions: int) -> int:
        """Calcule le score de liquidité basé sur le nombre de transactions"""
        if nb_transactions >= 50:
            return 5
        elif nb_transactions >= 20:
            return 4
        elif nb_transactions >= 10:
            return 3
        elif nb_transactions >= 5:
            return 2
        else:
            return 1

    @staticmethod
    def _calculate_size_score(surface: float) -> int:
        """Calcule le score basé sur la taille du bien"""
        if 50 <= surface <= 100:
            return 5  # Taille idéale pour location
        elif 40 <= surface <= 120:
            return 4
        elif 30 <= surface <= 140:
            return 3
        else:
            return 2

    @staticmethod
    def _calculate_yield_score(prix_m2: float, loyer_m2_estime: float = None) -> tuple:
        """Calcule le score et le rendement basé sur le loyer estimé"""
        if loyer_m2_estime:
            rendement_brut = (loyer_m2_estime * 12) / prix_m2 * 100

            if rendement_brut >= 8:
                score = 5
            elif rendement_brut >= 6:
                score = 4
            elif rendement_brut >= 4:
                score = 3
            elif rendement_brut >= 3:
                score = 2
            else:
                score = 1

            return score, rendement_brut
        else:
            return 3, None  # Score neutre si pas de donnée

    @classmethod
    def calculate_investment_score(
        cls,
        prix_m2: float,
        surface: float,
        nb_transactions: int,
        prix_m2_moyen_zone: float,
        loyer_m2_estime: float = None,
    ) -> Dict:
        """
        Calcule un score d'investissement basé sur plusieurs critères

        Args:
            prix_m2: Prix au m² du bien
            surface: Surface du bien
            nb_transactions: Nombre de transactions dans la zone
            prix_m2_moyen_zone: Prix moyen au m² dans la zone
            loyer_m2_estime: Loyer estimé au m² (optionnel)

        Returns:
            Dictionnaire avec les scores et métriques
        """
        scores = {}

        # Calcul des scores individuels
        scores["score_prix"] = cls._calculate_price_score(prix_m2, prix_m2_moyen_zone)
        scores["score_liquidite"] = cls._calculate_liquidity_score(nb_transactions)
        scores["score_taille"] = cls._calculate_size_score(surface)

        score_rendement, rendement_brut = cls._calculate_yield_score(
            prix_m2, loyer_m2_estime
        )
        scores["score_rendement"] = score_rendement

        if rendement_brut is not None:
            scores["rendement_brut_estime"] = rendement_brut

        # Score global (moyenne pondérée)
        poids = {
            "score_prix": 0.3,
            "score_liquidite": 0.2,
            "score_taille": 0.2,
            "score_rendement": 0.3,
        }

        score_global = sum(scores[k] * poids[k] for k in poids.keys())
        scores["score_global"] = round(score_global, 2)

        # Classification
        if score_global >= 4.5:
            scores["classification"] = "Excellent"
        elif score_global >= 3.5:
            scores["classification"] = "Très bon"
        elif score_global >= 2.5:
            scores["classification"] = "Bon"
        elif score_global >= 1.5:
            scores["classification"] = "Moyen"
        else:
            scores["classification"] = "Faible"

        return scores

    @staticmethod
    def find_investment_opportunities(
        df: pd.DataFrame,
        max_prix_m2: float = None,
        min_surface: float = 30,
        max_surface: float = 120,
        min_transactions_zone: int = 10,
    ) -> pd.DataFrame:
        """
        Identifie les opportunités d'investissement dans le dataset

        Args:
            df: DataFrame avec les données DVF nettoyées
            max_prix_m2: Prix maximum au m² accepté
            min_surface: Surface minimale
            max_surface: Surface maximale
            min_transactions_zone: Nombre minimum de transactions dans la zone

        Returns:
            DataFrame avec les opportunités triées par score
        """
        # Filtrage de base
        opportunities = df.copy()

        if min_surface:
            opportunities = opportunities[
                opportunities["surface_reelle_bati"] >= min_surface
            ]
        if max_surface:
            opportunities = opportunities[
                opportunities["surface_reelle_bati"] <= max_surface
            ]
        if max_prix_m2:
            opportunities = opportunities[opportunities["prix_m2"] <= max_prix_m2]

        # Calcul des statistiques par commune
        commune_stats = (
            opportunities.groupby("nom_commune")
            .agg({"prix_m2": "mean", "valeur_fonciere": "count"})
            .rename(
                columns={
                    "prix_m2": "prix_m2_moyen_commune",
                    "valeur_fonciere": "nb_transactions_commune",
                }
            )
        )

        # Filtrer les communes avec assez de transactions
        commune_stats = commune_stats[
            commune_stats["nb_transactions_commune"] >= min_transactions_zone
        ]

        # Joindre les statistiques
        opportunities = opportunities.merge(
            commune_stats, left_on="nom_commune", right_index=True, how="inner"
        )

        # Calcul des scores d'investissement
        scores_list = []
        for _, row in opportunities.iterrows():
            score = InvestmentAnalyzer.calculate_investment_score(
                prix_m2=row["prix_m2"],
                surface=row["surface_reelle_bati"],
                nb_transactions=row["nb_transactions_commune"],
                prix_m2_moyen_zone=row["prix_m2_moyen_commune"],
            )
            scores_list.append(score)

        # Ajouter les scores au DataFrame
        scores_df = pd.DataFrame(scores_list)
        opportunities = pd.concat(
            [opportunities.reset_index(drop=True), scores_df], axis=1
        )

        # Trier par score global décroissant
        opportunities = opportunities.sort_values("score_global", ascending=False)

        return opportunities[
            [
                "nom_commune",
                "valeur_fonciere",
                "surface_reelle_bati",
                "prix_m2",
                "prix_m2_moyen_commune",
                "score_global",
                "classification",
                "score_prix",
                "score_liquidite",
                "score_taille",
                "score_rendement",
            ]
        ]


def load_dvf_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données DVF depuis un fichier CSV

    Args:
        file_path: Chemin vers le fichier CSV

    Returns:
        DataFrame avec les données DVF
    """
    try:
        # Essayer différents encodages pour les fichiers DVF français
        encodings = ["utf-8", "iso-8859-1", "windows-1252", "cp1252"]

        for encoding in encodings:
            try:
                # DVF utilise généralement le point-virgule comme séparateur
                df = pd.read_csv(
                    file_path, low_memory=False, encoding=encoding, sep=";"
                )
                print(
                    f"✅ Données chargées avec encodage {encoding} : "
                    f"{df.shape[0]} lignes, {df.shape[1]} colonnes"
                )

                # Conversion automatique de la date si présente
                if "date_mutation" in df.columns:
                    df["date_mutation"] = pd.to_datetime(df["date_mutation"])
                    print(
                        f"📅 Période couverte : {df['date_mutation'].min()} "
                        f"à {df['date_mutation'].max()}"
                    )

                return df
            except UnicodeDecodeError:
                continue

        # Si aucun encodage ne fonctionne, essayer avec errors='ignore'
        df = pd.read_csv(
            file_path, low_memory=False, encoding="utf-8", errors="ignore", sep=";"
        )
        print(
            f"✅ Données chargées avec encodage UTF-8 (errors='ignore') : {df.shape[0]} lignes, {df.shape[1]} colonnes"
        )

        if "date_mutation" in df.columns:
            df["date_mutation"] = pd.to_datetime(df["date_mutation"])
            print(
                f"📅 Période couverte : {df['date_mutation'].min()} à {df['date_mutation'].max()}"
            )

        return df

    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {file_path}")
        raise
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        raise


class StatisticalAnalyzer:
    """
    Classe pour les analyses statistiques avancées des données DVF (T015-T019)
    """

    @staticmethod
    def comprehensive_descriptive_stats(
        df: pd.DataFrame, variables: List[str] = None
    ) -> Dict:
        """
        T015 - Statistiques descriptives complètes pour les variables principales

        Args:
            df: DataFrame avec les données
            variables: Liste des variables à analyser (par défaut: prix, surface, pièces)

        Returns:
            Dictionnaire avec les statistiques complètes
        """
        if variables is None:
            variables = ["valeur_fonciere", "prix_m2", "surface_reelle_bati"]
            if "nombre_pieces_principales" in df.columns:
                variables.append("nombre_pieces_principales")

        stats_dict = {}

        for var in variables:
            if var in df.columns:
                data = df[var].dropna()

                if len(data) > 0:
                    stats_dict[var] = {
                        "count": len(data),
                        "mean": float(data.mean()),
                        "median": float(data.median()),
                        "std": float(data.std()),
                        "min": float(data.min()),
                        "max": float(data.max()),
                        "q1": float(data.quantile(0.25)),
                        "q3": float(data.quantile(0.75)),
                        "skewness": float(stats.skew(data)),
                        "kurtosis": float(stats.kurtosis(data)),
                        "cv": (
                            float(data.std() / data.mean() * 100)
                            if data.mean() != 0
                            else np.nan
                        ),
                    }

        return stats_dict

    @staticmethod
    def geographical_price_analysis(
        df: pd.DataFrame, by_commune: bool = True, by_department: bool = True
    ) -> Dict:
        """
        T016 - Analyse des prix par commune et département

        Args:
            df: DataFrame avec les données
            by_commune: Analyser par commune
            by_department: Analyser par département

        Returns:
            Dictionnaire avec les analyses géographiques
        """
        results = {}

        if by_department and "code_departement" in df.columns:
            dept_analysis = (
                df.groupby("code_departement")
                .agg(
                    {
                        "prix_m2": ["mean", "median", "std", "count"],
                        "valeur_fonciere": ["mean", "median"],
                        "surface_reelle_bati": "mean",
                    }
                )
                .round(2)
            )

            dept_analysis.columns = [
                "_".join(col).strip() for col in dept_analysis.columns
            ]
            dept_analysis = dept_analysis.reset_index()
            dept_analysis = dept_analysis[
                dept_analysis["prix_m2_count"] >= 10
            ]  # Min 10 transactions

            results["departements"] = dept_analysis.sort_values(
                "prix_m2_mean", ascending=False
            )

        if by_commune and "nom_commune" in df.columns:
            commune_analysis = (
                df.groupby(["nom_commune", "code_departement"])
                .agg(
                    {
                        "prix_m2": ["mean", "median", "count"],
                        "valeur_fonciere": "mean",
                        "surface_reelle_bati": "mean",
                    }
                )
                .round(2)
            )

            commune_analysis.columns = [
                "_".join(col).strip() for col in commune_analysis.columns
            ]
            commune_analysis = commune_analysis.reset_index()
            commune_analysis = commune_analysis[
                commune_analysis["prix_m2_count"] >= 5
            ]  # Min 5 transactions

            results["communes"] = commune_analysis.sort_values(
                "prix_m2_mean", ascending=False
            )

        return results

    @staticmethod
    def property_type_analysis(df: pd.DataFrame) -> Dict:
        """
        T017 - Analyse détaillée par type de propriété

        Args:
            df: DataFrame avec les données

        Returns:
            Dictionnaire avec l'analyse par type de bien
        """
        if "type_local" not in df.columns:
            return {"error": "Colonne type_local non disponible"}

        results = {}

        # Analyse globale par type
        type_analysis = (
            df.groupby("type_local")
            .agg(
                {
                    "prix_m2": ["mean", "median", "std", "count"],
                    "valeur_fonciere": ["mean", "median", "std"],
                    "surface_reelle_bati": ["mean", "median", "std"],
                }
            )
            .round(2)
        )

        type_analysis.columns = ["_".join(col).strip() for col in type_analysis.columns]
        type_analysis = type_analysis.reset_index()

        results["global_analysis"] = type_analysis

        # Analyse par type et département
        type_dept_analysis = {}
        for type_bien in df["type_local"].value_counts().head(3).index:
            df_type = df[df["type_local"] == type_bien]
            dept_type = (
                df_type.groupby("code_departement")
                .agg({"prix_m2": ["mean", "count"], "surface_reelle_bati": "mean"})
                .round(2)
            )

            dept_type.columns = ["_".join(col).strip() for col in dept_type.columns]
            dept_type = dept_type.reset_index()
            dept_type = dept_type[dept_type["prix_m2_count"] >= 5]

            type_dept_analysis[type_bien] = dept_type.sort_values(
                "prix_m2_mean", ascending=False
            )

        results["by_department"] = type_dept_analysis

        return results

    @staticmethod
    def temporal_evolution_analysis(df: pd.DataFrame) -> Dict:
        """
        T018 - Analyse de l'évolution temporelle

        Args:
            df: DataFrame avec les données (doit contenir date_mutation)

        Returns:
            Dictionnaire avec les analyses temporelles
        """
        if "date_mutation" not in df.columns:
            return {"error": "Colonne date_mutation non disponible"}

        results = {}

        # Analyse annuelle
        yearly_analysis = (
            df.groupby("annee_mutation")
            .agg(
                {
                    "prix_m2": ["mean", "median", "count"],
                    "valeur_fonciere": ["mean", "sum"],
                    "surface_reelle_bati": "mean",
                }
            )
            .round(2)
        )

        yearly_analysis.columns = [
            "_".join(col).strip() for col in yearly_analysis.columns
        ]
        yearly_analysis = yearly_analysis.reset_index()

        # Calcul des taux de croissance
        yearly_analysis["croissance_prix"] = (
            yearly_analysis["prix_m2_mean"].pct_change() * 100
        )
        yearly_analysis["croissance_volume"] = (
            yearly_analysis["prix_m2_count"].pct_change() * 100
        )

        results["yearly"] = yearly_analysis

        # Analyse mensuelle
        monthly_analysis = (
            df.groupby(["annee_mutation", "mois_mutation"])
            .agg({"prix_m2": ["mean", "count"], "valeur_fonciere": "mean"})
            .round(2)
        )

        monthly_analysis.columns = [
            "_".join(col).strip() for col in monthly_analysis.columns
        ]
        monthly_analysis = monthly_analysis.reset_index()

        results["monthly"] = monthly_analysis

        # Analyse de saisonnalité
        seasonal_analysis = (
            df.groupby("mois_mutation")
            .agg({"prix_m2": ["mean", "count"], "valeur_fonciere": "mean"})
            .round(2)
        )

        seasonal_analysis.columns = [
            "_".join(col).strip() for col in seasonal_analysis.columns
        ]
        seasonal_analysis = seasonal_analysis.reset_index()

        # Calcul des variations par rapport à la moyenne annuelle
        prix_moyen_annuel = df["prix_m2"].mean()
        seasonal_analysis["variation_vs_moyenne"] = (
            seasonal_analysis["prix_m2_mean"] / prix_moyen_annuel - 1
        ) * 100

        results["seasonal"] = seasonal_analysis

        return results

    @staticmethod
    def outlier_detection(
        df: pd.DataFrame, variables: List[str] = None, method: str = "iqr"
    ) -> Dict:
        """
        T019 - Détection d'outliers et d'anomalies

        Args:
            df: DataFrame avec les données
            variables: Variables à analyser pour les outliers
            method: Méthode de détection ('iqr', 'zscore', 'modified_zscore')

        Returns:
            Dictionnaire avec les outliers détectés
        """
        if variables is None:
            variables = ["prix_m2", "surface_reelle_bati", "valeur_fonciere"]

        results = {}

        for var in variables:
            if var not in df.columns:
                continue

            data = df[var].dropna()
            outliers_info = {}

            if method == "iqr":
                Q1 = data.quantile(0.25)
                Q3 = data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers_mask = (data < lower_bound) | (data > upper_bound)

                outliers_info = {
                    "method": "IQR",
                    "q1": float(Q1),
                    "q3": float(Q3),
                    "iqr": float(IQR),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                    "outliers_count": int(outliers_mask.sum()),
                    "outliers_percentage": float(outliers_mask.sum() / len(data) * 100),
                    "outliers_indices": outliers_mask[outliers_mask].index.tolist(),
                }

            elif method == "zscore":
                z_scores = np.abs(stats.zscore(data))
                threshold = 3
                outliers_mask = z_scores > threshold

                outliers_info = {
                    "method": "Z-Score",
                    "threshold": threshold,
                    "outliers_count": int(outliers_mask.sum()),
                    "outliers_percentage": float(outliers_mask.sum() / len(data) * 100),
                    "outliers_indices": data.index[outliers_mask].tolist(),
                }

            results[var] = outliers_info

        return results

    @staticmethod
    def market_anomalies_detection(df: pd.DataFrame) -> Dict:
        """
        T019 - Détection d'anomalies spécifiques au marché immobilier

        Args:
            df: DataFrame avec les données

        Returns:
            Dictionnaire avec les anomalies détectées
        """
        results = {}

        # Anomalies temporelles
        if "date_mutation" in df.columns:
            daily_volumes = df.groupby("date_mutation").size()
            high_volume_threshold = daily_volumes.quantile(0.95)
            high_volume_days = daily_volumes[daily_volumes > high_volume_threshold]

            results["temporal_anomalies"] = {
                "high_volume_days": len(high_volume_days),
                "threshold": float(high_volume_threshold),
                "dates": high_volume_days.index.strftime("%Y-%m-%d").tolist(),
                "volumes": high_volume_days.values.tolist(),
            }

        # Anomalies géographiques (communes avec écarts importants vs département)
        if all(
            col in df.columns for col in ["nom_commune", "code_departement", "prix_m2"]
        ):
            dept_avg_prices = df.groupby("code_departement")["prix_m2"].mean()

            commune_vs_dept = (
                df.groupby(["nom_commune", "code_departement"])
                .agg({"prix_m2": ["mean", "count"]})
                .round(2)
            )

            commune_vs_dept.columns = ["prix_m2_commune", "nb_transactions"]
            commune_vs_dept = commune_vs_dept.reset_index()
            commune_vs_dept = commune_vs_dept[commune_vs_dept["nb_transactions"] >= 5]

            commune_vs_dept["prix_m2_dept"] = commune_vs_dept["code_departement"].map(
                dept_avg_prices
            )
            commune_vs_dept["ecart_vs_dept"] = (
                commune_vs_dept["prix_m2_commune"] / commune_vs_dept["prix_m2_dept"] - 1
            ) * 100

            # Communes avec surprime/décote importante
            surprimes = commune_vs_dept[commune_vs_dept["ecart_vs_dept"] > 50]
            decotes = commune_vs_dept[commune_vs_dept["ecart_vs_dept"] < -30]

            results["geographical_anomalies"] = {
                "surprimes_importantes": {
                    "count": len(surprimes),
                    "communes": surprimes.nlargest(10, "ecart_vs_dept")[
                        [
                            "nom_commune",
                            "code_departement",
                            "ecart_vs_dept",
                            "prix_m2_commune",
                        ]
                    ].to_dict("records"),
                },
                "decotes_importantes": {
                    "count": len(decotes),
                    "communes": decotes.nsmallest(10, "ecart_vs_dept")[
                        [
                            "nom_commune",
                            "code_departement",
                            "ecart_vs_dept",
                            "prix_m2_commune",
                        ]
                    ].to_dict("records"),
                },
            }

        return results

    @staticmethod
    def investment_market_analysis(df: pd.DataFrame, target_yield: float = 4.0) -> Dict:
        """
        Analyse complète pour l'investissement immobilier

        Args:
            df: DataFrame avec les données DVF
            target_yield: Rendement cible en pourcentage

        Returns:
            Dictionnaire avec l'analyse d'investissement
        """
        results = {}

        # Segments par surface pour l'investissement locatif
        df_copy = df.copy()
        df_copy["segment_surface"] = pd.cut(
            df_copy["surface_reelle_bati"],
            bins=[0, 30, 50, 70, 100, 150, float("inf")],
            labels=["<30m²", "30-50m²", "50-70m²", "70-100m²", "100-150m²", ">150m²"],
        )

        segment_analysis = (
            df_copy.groupby("segment_surface")
            .agg(
                {
                    "prix_m2": ["mean", "count"],
                    "valeur_fonciere": "mean",
                    "surface_reelle_bati": "mean",
                }
            )
            .round(2)
        )

        segment_analysis.columns = [
            "_".join(col).strip() for col in segment_analysis.columns
        ]
        segment_analysis = segment_analysis.reset_index()

        results["surface_segments"] = segment_analysis

        # Estimation de rentabilité par type et zone
        if "type_local" in df.columns:
            # Hypothèses de rendement par type (taux mensuel)
            rental_rates = {
                "Appartement": 0.009,  # 0.9% par mois
                "Maison": 0.008,  # 0.8% par mois
                "Local industriel. commercial ou assimilé": 0.007,  # 0.7% par mois
            }

            yield_analysis = []

            for type_bien in df["type_local"].value_counts().head(3).index:
                df_type = df[df["type_local"] == type_bien]
                monthly_rate = rental_rates.get(type_bien, 0.008)

                type_stats = {
                    "type_bien": type_bien,
                    "prix_achat_moyen": float(df_type["valeur_fonciere"].mean()),
                    "prix_m2_moyen": float(df_type["prix_m2"].mean()),
                    "surface_moyenne": float(df_type["surface_reelle_bati"].mean()),
                    "taux_mensuel_estime": monthly_rate,
                    "loyer_mensuel_estime": float(
                        df_type["valeur_fonciere"].mean() * monthly_rate
                    ),
                    "rendement_brut_estime": float(monthly_rate * 12 * 100),
                    "nb_transactions": len(df_type),
                }

                yield_analysis.append(type_stats)

            results["yield_analysis"] = yield_analysis

        return results


class DashboardAnalytics:
    """
    Classe pour les analyses du tableau de bord interactif (T020-T023)
    """

    @staticmethod
    def filter_dashboard_data(
        df: pd.DataFrame,
        dept: str = "Tous",
        years: tuple = None,
        prix_range: tuple = None,
        surface_range: tuple = None,
        types: list = None,
        prix_m2_range: tuple = None,
    ) -> pd.DataFrame:
        """
        Filtre les données selon les critères du tableau de bord

        Args:
            df: DataFrame source
            dept: Code département ou 'Tous'
            years: Tuple (année_min, année_max)
            prix_range: Tuple (prix_min, prix_max)
            surface_range: Tuple (surface_min, surface_max)
            types: Liste des types de biens
            prix_m2_range: Tuple (prix_m2_min, prix_m2_max)

        Returns:
            DataFrame filtré
        """
        filtered_data = df.copy()

        # Filtre par département
        if dept != "Tous":
            filtered_data = filtered_data[filtered_data["code_departement"] == dept]

        # Filtre par années
        if years is not None:
            filtered_data = filtered_data[
                (filtered_data["annee"] >= years[0])
                & (filtered_data["annee"] <= years[1])
            ]

        # Filtre par prix
        if prix_range is not None:
            filtered_data = filtered_data[
                (filtered_data["valeur_fonciere"] >= prix_range[0])
                & (filtered_data["valeur_fonciere"] <= prix_range[1])
            ]

        # Filtre par surface
        if surface_range is not None:
            filtered_data = filtered_data[
                (filtered_data["surface_reelle_bati"] >= surface_range[0])
                & (filtered_data["surface_reelle_bati"] <= surface_range[1])
            ]

        # Filtre par type
        if types is not None:
            filtered_data = filtered_data[filtered_data["type_local"].isin(types)]

        # Filtre par prix/m²
        if prix_m2_range is not None:
            filtered_data = filtered_data[
                (filtered_data["prix_m2"] >= prix_m2_range[0])
                & (filtered_data["prix_m2"] <= prix_m2_range[1])
            ]

        return filtered_data

    @staticmethod
    def calculate_dashboard_stats(df: pd.DataFrame) -> Dict:
        """
        Calcule les statistiques pour le tableau de bord

        Args:
            df: DataFrame filtré

        Returns:
            Dictionnaire avec les statistiques
        """
        if len(df) == 0:
            return {
                "nb_transactions": 0,
                "prix_median": 0,
                "prix_m2_median": 0,
                "surface_mediane": 0,
                "periode": "Aucune donnée",
            }

        stats = {
            "nb_transactions": len(df),
            "prix_median": float(df["valeur_fonciere"].median()),
            "prix_m2_median": float(df["prix_m2"].median()),
            "surface_mediane": float(df["surface_reelle_bati"].median()),
            "prix_moyen": float(df["valeur_fonciere"].mean()),
            "prix_m2_moyen": float(df["prix_m2"].mean()),
            "surface_moyenne": float(df["surface_reelle_bati"].mean()),
            "periode": f"{df['annee'].min()} - {df['annee'].max()}",
        }

        return stats

    @staticmethod
    def get_top_communes_dashboard(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """
        Obtient les top communes pour le tableau de bord

        Args:
            df: DataFrame filtré
            n: Nombre de communes à retourner

        Returns:
            DataFrame avec les top communes
        """
        if len(df) == 0:
            return pd.DataFrame()

        top_communes = (
            df.groupby("nom_commune")
            .agg({"valeur_fonciere": "count", "prix_m2": "median"})
            .round(0)
        )

        top_communes.columns = ["nb_transactions", "prix_m2_median"]
        top_communes = top_communes.sort_values(
            "nb_transactions", ascending=False
        ).head(n)

        return top_communes.reset_index()

    @staticmethod
    def calculate_investment_score_simple(
        prix_m2: float,
        surface: float,
        nb_transactions_commune: int,
        prix_m2_median_commune: float,
    ) -> Dict:
        """
        Calcule un score d'investissement simplifié pour le dashboard

        Args:
            prix_m2: Prix au m² du bien
            surface: Surface du bien
            nb_transactions_commune: Nombre de transactions dans la commune
            prix_m2_median_commune: Prix médian/m² dans la commune

        Returns:
            Dictionnaire avec le score et les composants
        """
        scores = {}

        # Score prix (comparaison avec médiane locale)
        ratio_prix = (
            prix_m2 / prix_m2_median_commune if prix_m2_median_commune > 0 else 1
        )
        if ratio_prix <= 0.8:
            scores["score_prix"] = 10
        elif ratio_prix <= 0.9:
            scores["score_prix"] = 8
        elif ratio_prix <= 1.0:
            scores["score_prix"] = 6
        elif ratio_prix <= 1.1:
            scores["score_prix"] = 4
        else:
            scores["score_prix"] = 2

        # Score liquidité (basé sur volume de transactions)
        if nb_transactions_commune >= 50:
            scores["score_liquidite"] = 10
        elif nb_transactions_commune >= 20:
            scores["score_liquidite"] = 8
        elif nb_transactions_commune >= 10:
            scores["score_liquidite"] = 6
        elif nb_transactions_commune >= 5:
            scores["score_liquidite"] = 4
        else:
            scores["score_liquidite"] = 2

        # Score surface (taille optimale pour location)
        if 50 <= surface <= 80:
            scores["score_surface"] = 10
        elif 40 <= surface <= 100:
            scores["score_surface"] = 8
        elif 30 <= surface <= 120:
            scores["score_surface"] = 6
        else:
            scores["score_surface"] = 4

        # Score global
        scores["score_global"] = (
            scores["score_prix"] * 0.4
            + scores["score_liquidite"] * 0.3
            + scores["score_surface"] * 0.3
        )

        # Classification
        if scores["score_global"] >= 8:
            scores["classification"] = "Excellent"
        elif scores["score_global"] >= 6:
            scores["classification"] = "Très bon"
        elif scores["score_global"] >= 4:
            scores["classification"] = "Bon"
        else:
            scores["classification"] = "Moyen"

        return scores

    @staticmethod
    def generate_investment_insights(df: pd.DataFrame) -> Dict:
        """
        Génère des insights d'investissement basés sur les données filtrées

        Args:
            df: DataFrame filtré

        Returns:
            Dictionnaire avec les insights
        """
        if len(df) == 0:
            return {"error": "Aucune donnée disponible"}

        insights = {}

        # Analyse des prix
        prix_stats = {
            "prix_min": float(df["valeur_fonciere"].min()),
            "prix_max": float(df["valeur_fonciere"].max()),
            "prix_median": float(df["valeur_fonciere"].median()),
            "prix_m2_median": float(df["prix_m2"].median()),
            "ecart_type_prix_m2": float(df["prix_m2"].std()),
        }
        insights["prix_stats"] = prix_stats

        # Identification des opportunités (prix/m² < médiane - 1 écart-type)
        seuil_opportunite = (
            prix_stats["prix_m2_median"] - prix_stats["ecart_type_prix_m2"]
        )
        opportunites = df[df["prix_m2"] < seuil_opportunite]

        insights["opportunites"] = {
            "nb_opportunites": len(opportunites),
            "pourcentage": float(len(opportunites) / len(df) * 100),
            "seuil_prix_m2": float(seuil_opportunite),
            "surface_moyenne_opportunites": (
                float(opportunites["surface_reelle_bati"].median())
                if len(opportunites) > 0
                else 0
            ),
        }

        # Analyse par type de bien
        if "type_local" in df.columns:
            type_analysis = (
                df.groupby("type_local")
                .agg(
                    {
                        "valeur_fonciere": ["count", "median"],
                        "prix_m2": "median",
                        "surface_reelle_bati": "median",
                    }
                )
                .round(0)
            )

            type_analysis.columns = [
                "nb_transactions",
                "prix_median",
                "prix_m2_median",
                "surface_mediane",
            ]
            insights["analyse_types"] = type_analysis.to_dict("index")

        # Tendances temporelles si plusieurs années
        if df["annee"].nunique() > 1:
            temporal_analysis = (
                df.groupby("annee")
                .agg({"prix_m2": "median", "valeur_fonciere": "count"})
                .round(0)
            )

            temporal_analysis["variation_prix"] = (
                temporal_analysis["prix_m2"].pct_change() * 100
            )
            insights["tendances_temporelles"] = temporal_analysis.to_dict("index")

        return insights


class RecommendationEngine:
    """
    Moteur de recommandations simplifié pour l'application (T022)
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialise le moteur avec les données DVF

        Args:
            df: DataFrame avec les données DVF nettoyées
        """
        self.df = df.copy()
        self._prepare_commune_stats()

    def _prepare_commune_stats(self):
        """Prépare les statistiques par commune pour les calculs"""
        self.commune_stats = (
            self.df.groupby("nom_commune")
            .agg(
                {
                    "prix_m2": ["median", "count"],
                    "valeur_fonciere": "median",
                    "surface_reelle_bati": "median",
                }
            )
            .round(2)
        )

        self.commune_stats.columns = [
            "prix_m2_median",
            "nb_transactions",
            "prix_median",
            "surface_mediane",
        ]
        self.commune_stats = self.commune_stats.reset_index()

    def recommend_by_profile(
        self,
        profile: str,
        budget_max: float,
        surface_range: tuple,
        filtered_data: pd.DataFrame = None,
    ) -> Dict:
        """
        Génère des recommandations selon le profil d'investisseur

        Args:
            profile: 'debutant', 'experimente', ou 'equilibre'
            budget_max: Budget maximum
            surface_range: Tuple (surface_min, surface_max)
            filtered_data: Données pré-filtrées (optionnel)

        Returns:
            Dictionnaire avec les recommandations
        """
        # Utiliser les données filtrées ou toutes les données
        data = filtered_data.copy() if filtered_data is not None else self.df.copy()

        # Filtrage de base selon les critères
        data = data[
            (data["valeur_fonciere"] <= budget_max)
            & (data["surface_reelle_bati"] >= surface_range[0])
            & (data["surface_reelle_bati"] <= surface_range[1])
        ]

        if len(data) == 0:
            return {"error": "Aucun bien ne correspond aux critères"}

        # Joindre les statistiques communales
        data = data.merge(
            self.commune_stats[["nom_commune", "prix_m2_median", "nb_transactions"]],
            on="nom_commune",
            how="left",
            suffixes=("", "_commune"),
        )

        # Calcul des scores selon le profil
        if profile == "debutant":
            data = self._score_for_beginner(data)
            sort_column = "score_securite"
        elif profile == "experimente":
            data = self._score_for_experienced(data)
            sort_column = "score_opportunite"
        else:  # equilibre
            data = self._score_for_balanced(data)
            sort_column = "score_equilibre"

        # Top 10 des recommandations
        recommendations = data.nlargest(10, sort_column)

        # Analyse des zones recommandées
        zones_analysis = self._analyze_recommended_zones(recommendations)

        # Conseils personnalisés
        conseils = self._get_personalized_advice(profile)

        return {
            "profile": profile,
            "budget": budget_max,
            "surface_range": surface_range,
            "nb_biens_analyses": len(data),
            "recommendations": recommendations[
                [
                    "nom_commune",
                    "code_departement",
                    "valeur_fonciere",
                    "surface_reelle_bati",
                    "prix_m2",
                    "type_local",
                    "nombre_pieces_principales",
                    "annee",
                    sort_column,
                ]
            ].to_dict("records"),
            "zones_analysis": zones_analysis,
            "conseils": conseils,
        }

    def _score_for_beginner(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calcule le score pour profil débutant (sécurité prioritaire)"""
        data = data.copy()
        median_prix_m2 = data["prix_m2"].median()
        median_prix = data["valeur_fonciere"].median()

        data["score_securite"] = (
            (1 - (data["prix_m2"] / median_prix_m2)) * 40  # Bonus prix/m² bas
            + (1 - (data["valeur_fonciere"] / median_prix))
            * 30  # Bonus prix absolu bas
            + np.log(data["nb_transactions"] + 1) * 15  # Bonus volume transactions
        )

        return data

    def _score_for_experienced(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calcule le score pour profil expérimenté (opportunités prioritaires)"""
        data = data.copy()

        # Écart par rapport au prix médian de la commune
        data["ecart_prix"] = (data["prix_m2_median"] - data["prix_m2"]) / data[
            "prix_m2_median"
        ]
        data["ecart_prix"] = data["ecart_prix"].fillna(0)

        data["score_opportunite"] = (
            data["ecart_prix"] * 50  # Bonus pour prix sous la médiane communale
            + (1000 / data["prix_m2"]) * 20  # Bonus prix/m² relativement bas
            + np.log(data["nb_transactions"] + 1) * 15  # Bonus activité
        )

        return data

    def _score_for_balanced(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calcule le score pour profil équilibré"""
        data = data.copy()
        median_prix_m2 = data["prix_m2"].median()

        # Écart par rapport au prix médian de la commune
        data["ecart_prix"] = (data["prix_m2_median"] - data["prix_m2"]) / data[
            "prix_m2_median"
        ]
        data["ecart_prix"] = data["ecart_prix"].fillna(0)

        data["score_equilibre"] = (
            (1 - (data["prix_m2"] / median_prix_m2)) * 25  # Sécurité prix
            + data["ecart_prix"] * 25  # Opportunité
            + np.log(data["nb_transactions"] + 1) * 20  # Volume
            + (data["surface_reelle_bati"] / 100) * 10  # Bonus surface
        )

        return data

    def _analyze_recommended_zones(self, recommendations: pd.DataFrame) -> Dict:
        """Analyse les zones des biens recommandés"""
        zones_analysis = (
            recommendations.groupby("nom_commune")
            .agg(
                {
                    "valeur_fonciere": ["count", "median"],
                    "prix_m2": "median",
                    "surface_reelle_bati": "median",
                }
            )
            .round(0)
        )

        zones_analysis.columns = [
            "nb_recommandations",
            "prix_median",
            "prix_m2_median",
            "surface_mediane",
        ]
        zones_analysis = zones_analysis.sort_values(
            "nb_recommandations", ascending=False
        )

        return zones_analysis.to_dict("index")

    def _get_personalized_advice(self, profile: str) -> List[str]:
        """Génère des conseils personnalisés selon le profil"""
        conseils_base = {
            "debutant": [
                "🔒 Privilégiez les zones avec beaucoup de transactions (marché liquide)",
                "📈 Évitez les prix/m² trop éloignés de la médiane locale",
                "🏦 Considérez la facilité de revente dans ces zones actives",
                "📍 Concentrez-vous sur les départements que vous connaissez",
                "⏱️ Prenez le temps d'analyser plusieurs biens similaires",
            ],
            "experimente": [
                "🎯 Recherchez les biens sous-évalués par rapport à leur commune",
                "📊 Analysez les tendances d'évolution des prix dans ces zones",
                "🔄 Considérez le potentiel de rénovation/amélioration",
                "💹 Évaluez les perspectives de développement local",
                "⚡ Agissez rapidement sur les bonnes opportunités",
            ],
            "equilibre": [
                "⚖️ Équilibrez sécurité (volume) et opportunité (prix)",
                "📈 Diversifiez géographiquement vos investissements",
                "🔍 Vérifiez la cohérence prix/surface/localisation",
                "📋 Constituez une liste de surveillance de plusieurs biens",
                "🎯 Définissez des critères clairs avant de visiter",
            ],
        }

        return conseils_base.get(profile, conseils_base["equilibre"])


class InvestmentRecommendationEngine:
    """
    Moteur de recommandations d'investissement immobilier (T028-T034)
    """

    def __init__(self, dvf_data: pd.DataFrame, rental_data: pd.DataFrame = None):
        """
        Initialise le moteur de recommandations

        Args:
            dvf_data: DataFrame avec les données DVF nettoyées
            rental_data: DataFrame avec les données de loyer par département
        """
        self.dvf_data = dvf_data.copy()
        self.rental_data = rental_data.copy() if rental_data is not None else None
        self._prepare_data()

    def _prepare_data(self):
        """Prépare les données pour les calculs"""
        # Conversion des codes département
        if "code_departement" in self.dvf_data.columns:
            self.dvf_data["code_departement"] = (
                self.dvf_data["code_departement"].astype(str).str.replace(".0", "")
            )

        # Calcul du mois de mutation
        if "date_mutation" in self.dvf_data.columns:
            self.dvf_data["mois_mutation"] = self.dvf_data["date_mutation"].dt.month

    def integrate_rental_data(self) -> pd.DataFrame:
        """
        T028 - Intègre les données de loyer avec les données DVF

        Returns:
            DataFrame intégré avec estimations de loyer
        """
        if self.rental_data is None:
            print(
                "⚠️ Pas de données de loyer disponibles - création de données simulées"
            )
            return self._create_simulated_rental_data()

        # Préparation des codes département dans les données de loyer
        if "Département" in self.rental_data.columns:
            self.rental_data["code_departement"] = (
                self.rental_data["Département"].astype(str).str.zfill(2)
            )

        # Fusion des données
        integrated_data = self.dvf_data.merge(
            self.rental_data[["code_departement", "Loyer médian", "Loyer/m² médian"]],
            on="code_departement",
            how="left",
        )

        # Calcul des estimations de loyer mensuel
        integrated_data["loyer_mensuel_estime"] = (
            integrated_data["surface_reelle_bati"] * integrated_data["Loyer/m² médian"]
        )

        return integrated_data

    def _create_simulated_rental_data(self) -> pd.DataFrame:
        """Crée des données de loyer simulées basées sur les prix DVF"""
        dvf_with_rental = self.dvf_data.copy()

        # Estimation basée sur un ratio prix/loyer typique (20-25 ans)
        ratio_prix_loyer = 22  # 22 années de loyer = prix d'achat

        dvf_with_rental["loyer_mensuel_estime"] = dvf_with_rental["valeur_fonciere"] / (
            ratio_prix_loyer * 12
        )

        dvf_with_rental["loyer_m2_estime"] = (
            dvf_with_rental["loyer_mensuel_estime"]
            / dvf_with_rental["surface_reelle_bati"]
        )

        return dvf_with_rental

    def calculate_rental_yields(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        T029 - Calcule les rendements locatifs

        Args:
            data: DataFrame avec les données intégrées

        Returns:
            DataFrame avec les rendements calculés
        """
        data_with_yields = data.copy()

        # Rendement brut
        data_with_yields["rendement_brut"] = (
            (data_with_yields["loyer_mensuel_estime"] * 12)
            / data_with_yields["valeur_fonciere"]
            * 100
        )

        # Rendement net estimé (brut - 25% de charges et impôts)
        data_with_yields["rendement_net_estime"] = (
            data_with_yields["rendement_brut"] * 0.75
        )

        # Classification des rendements
        conditions = [
            data_with_yields["rendement_brut"] >= 8,
            data_with_yields["rendement_brut"] >= 6,
            data_with_yields["rendement_brut"] >= 4,
            data_with_yields["rendement_brut"] >= 3,
        ]

        choices = ["Excellent", "Très bon", "Bon", "Moyen"]

        data_with_yields["classe_rendement"] = np.select(
            conditions, choices, default="Faible"
        )

        return data_with_yields

    def calculate_multi_criteria_score(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        T030 - Calcule un score multi-critères d'investissement

        Args:
            data: DataFrame avec les données et rendements

        Returns:
            DataFrame avec les scores multi-critères
        """
        data_with_scores = data.copy()

        # Calcul des statistiques par commune pour les scores relatifs
        commune_stats = (
            data.groupby("nom_commune")
            .agg({"prix_m2": "mean", "valeur_fonciere": "count"})
            .rename(
                columns={
                    "prix_m2": "prix_m2_moyen_commune",
                    "valeur_fonciere": "nb_transactions_commune",
                }
            )
        )

        # Ajouter le rendement moyen par commune si disponible
        if "rendement_brut" in data.columns:
            commune_stats["rendement_moyen_commune"] = data.groupby("nom_commune")[
                "rendement_brut"
            ].mean()

        data_with_scores = data_with_scores.merge(
            commune_stats, left_on="nom_commune", right_index=True, how="left"
        )

        # Score prix (0-10) - plus c'est en dessous de la moyenne, mieux c'est
        data_with_scores["ratio_prix"] = (
            data_with_scores["prix_m2"] / data_with_scores["prix_m2_moyen_commune"]
        )
        data_with_scores["score_prix"] = np.where(
            data_with_scores["ratio_prix"] <= 0.8,
            10,
            np.where(
                data_with_scores["ratio_prix"] <= 0.9,
                8,
                np.where(
                    data_with_scores["ratio_prix"] <= 1.0,
                    6,
                    np.where(
                        data_with_scores["ratio_prix"] <= 1.1,
                        4,
                        np.where(data_with_scores["ratio_prix"] <= 1.2, 2, 0),
                    ),
                ),
            ),
        )

        # Score liquidité (0-10) - basé sur le nombre de transactions
        data_with_scores["score_liquidite"] = np.where(
            data_with_scores["nb_transactions_commune"] >= 100,
            10,
            np.where(
                data_with_scores["nb_transactions_commune"] >= 50,
                8,
                np.where(
                    data_with_scores["nb_transactions_commune"] >= 20,
                    6,
                    np.where(
                        data_with_scores["nb_transactions_commune"] >= 10,
                        4,
                        np.where(
                            data_with_scores["nb_transactions_commune"] >= 5, 2, 0
                        ),
                    ),
                ),
            ),
        )

        # Score surface (0-10) - privilégier les surfaces moyennes
        data_with_scores["score_surface"] = np.where(
            (data_with_scores["surface_reelle_bati"] >= 50)
            & (data_with_scores["surface_reelle_bati"] <= 80),
            10,
            np.where(
                (data_with_scores["surface_reelle_bati"] >= 40)
                & (data_with_scores["surface_reelle_bati"] <= 100),
                8,
                np.where(
                    (data_with_scores["surface_reelle_bati"] >= 30)
                    & (data_with_scores["surface_reelle_bati"] <= 120),
                    6,
                    np.where(
                        (data_with_scores["surface_reelle_bati"] >= 25)
                        & (data_with_scores["surface_reelle_bati"] <= 150),
                        4,
                        2,
                    ),
                ),
            ),
        )

        # Score rendement (0-10)
        data_with_scores["score_rendement"] = np.where(
            data_with_scores["rendement_brut"] >= 8,
            10,
            np.where(
                data_with_scores["rendement_brut"] >= 6,
                8,
                np.where(
                    data_with_scores["rendement_brut"] >= 4,
                    6,
                    np.where(
                        data_with_scores["rendement_brut"] >= 3,
                        4,
                        np.where(data_with_scores["rendement_brut"] >= 2, 2, 0),
                    ),
                ),
            ),
        )

        # Score global pondéré
        weights = {
            "score_prix": 0.25,
            "score_liquidite": 0.20,
            "score_surface": 0.15,
            "score_rendement": 0.40,
        }

        data_with_scores["score_global"] = (
            data_with_scores["score_prix"] * weights["score_prix"]
            + data_with_scores["score_liquidite"] * weights["score_liquidite"]
            + data_with_scores["score_surface"] * weights["score_surface"]
            + data_with_scores["score_rendement"] * weights["score_rendement"]
        )

        # Classification finale
        data_with_scores["classe_investissement"] = np.where(
            data_with_scores["score_global"] >= 8,
            "Excellent",
            np.where(
                data_with_scores["score_global"] >= 6,
                "Très bon",
                np.where(
                    data_with_scores["score_global"] >= 4,
                    "Bon",
                    np.where(data_with_scores["score_global"] >= 2, "Moyen", "Faible"),
                ),
            ),
        )

        return data_with_scores

    def identify_attractive_zones(
        self, data: pd.DataFrame, min_transactions: int = 10
    ) -> pd.DataFrame:
        """
        T031 - Identifie les zones attractives pour l'investissement

        Args:
            data: DataFrame avec les scores calculés
            min_transactions: Nombre minimum de transactions par zone

        Returns:
            DataFrame avec les zones attractives
        """
        # Agrégation par commune
        agg_dict = {
            "score_global": "mean",
            "prix_m2": "mean",
            "valeur_fonciere": ["mean", "count"],
            "surface_reelle_bati": "mean",
            "score_prix": "mean",
            "score_liquidite": "mean",
        }

        # Ajouter le rendement et score rendement s'ils existent
        if "rendement_brut" in data.columns:
            agg_dict["rendement_brut"] = "mean"
        if "score_rendement" in data.columns:
            agg_dict["score_rendement"] = "mean"

        zones_analysis = (
            data.groupby(["nom_commune", "code_departement"]).agg(agg_dict).round(2)
        )

        # Debug: print columns before flattening
        # print("Colonnes avant aplatissement:", zones_analysis.columns.tolist())

        # Aplatir les colonnes multi-index plus soigneusement
        new_columns = []
        for col in zones_analysis.columns.values:
            if isinstance(col, tuple):
                if len(col) > 1 and col[1] != "":
                    new_columns.append("_".join(col).strip())
                else:
                    new_columns.append(col[0])
            else:
                new_columns.append(col)

        zones_analysis.columns = new_columns
        zones_analysis = zones_analysis.reset_index()

        # Debug: print columns after flattening
        # print("Colonnes après aplatissement:", zones_analysis.columns.tolist())

        # Renommer les colonnes pour plus de clarté
        zones_analysis = zones_analysis.rename(
            columns={
                "valeur_fonciere_mean": "prix_moyen",
                "valeur_fonciere_count": "nb_transactions",
                "score_global_mean": "score_global",
                "prix_m2_mean": "prix_m2",
                "surface_reelle_bati_mean": "surface_reelle_bati",
                "score_prix_mean": "score_prix",
                "score_liquidite_mean": "score_liquidite",
                "rendement_brut_mean": "rendement_brut",
                "score_rendement_mean": "score_rendement",
            }
        )

        # Filtrer par nombre minimum de transactions
        zones_attractives = zones_analysis[
            zones_analysis["nb_transactions"] >= min_transactions
        ]

        # Ajouter des indicateurs de performance
        if (
            "rendement_brut" in zones_attractives.columns
            and "score_prix" in zones_attractives.columns
        ):
            zones_attractives["rentabilite_prix"] = (
                zones_attractives["rendement_brut"]
                * zones_attractives["score_prix"]
                / 100
            )

        # Classement par score global
        zones_attractives = zones_attractives.sort_values(
            "score_global", ascending=False
        )

        # Catégorisation des zones
        zones_attractives["categorie_zone"] = np.where(
            zones_attractives["score_global"] >= 7,
            "Zone Premium",
            np.where(
                zones_attractives["score_global"] >= 5,
                "Zone Attractive",
                np.where(
                    zones_attractives["score_global"] >= 3,
                    "Zone Correct",
                    "Zone à Éviter",
                ),
            ),
        )

        return zones_attractives

    def _filter_zones_by_criteria(
        self,
        zones_data: pd.DataFrame,
        budget_max: float,
        surface_min: float,
        surface_max: float,
        rendement_min: float,
    ) -> pd.DataFrame:
        """Filtre les zones selon les critères de l'investisseur"""
        filter_conditions = []

        if "prix_moyen" in zones_data.columns:
            filter_conditions.append(zones_data["prix_moyen"] <= budget_max)
        if "surface_reelle_bati" in zones_data.columns:
            filter_conditions.append(zones_data["surface_reelle_bati"] >= surface_min)
            filter_conditions.append(zones_data["surface_reelle_bati"] <= surface_max)
        if "rendement_brut" in zones_data.columns:
            filter_conditions.append(zones_data["rendement_brut"] >= rendement_min)

        if filter_conditions:
            combined_filter = filter_conditions[0]
            for condition in filter_conditions[1:]:
                combined_filter = combined_filter & condition
            return zones_data[combined_filter].copy()
        else:
            return zones_data.copy()

    def _get_top_recommendations(self, filtered_zones: pd.DataFrame) -> list:
        """Obtient les 5 meilleures recommandations"""
        top_recommendations = filtered_zones.head(5)

        available_cols = ["nom_commune", "code_departement"]
        optional_cols = [
            "score_global",
            "rendement_brut",
            "prix_moyen",
            "prix_m2",
            "categorie_zone",
        ]

        for col in optional_cols:
            if col in top_recommendations.columns:
                available_cols.append(col)

        return top_recommendations[available_cols].to_dict("records")

    def _get_strategies_recommendations(self, filtered_zones: pd.DataFrame) -> dict:
        """Génère les recommandations par stratégie"""
        strategies = {}

        if "rendement_brut" in filtered_zones.columns:
            strategies["rendement_max"] = filtered_zones.nlargest(3, "rendement_brut")
        if "score_prix" in filtered_zones.columns:
            strategies["prix_attractif"] = filtered_zones.nlargest(3, "score_prix")
        if "score_global" in filtered_zones.columns:
            strategies["equilibre"] = filtered_zones.nlargest(3, "score_global")

        strategy_recommendations = {}
        for strategy_name, strategy_data in strategies.items():
            strategy_cols = ["nom_commune", "code_departement"]
            for col in ["rendement_brut", "prix_moyen", "score_global"]:
                if col in strategy_data.columns:
                    strategy_cols.append(col)

            strategy_recommendations[f"strategie_{strategy_name}"] = strategy_data[
                strategy_cols
            ].to_dict("records")

        return strategy_recommendations

    def _analyze_departments(self, filtered_zones: pd.DataFrame) -> dict:
        """Analyse les zones par département"""
        dept_analysis = (
            filtered_zones.groupby("code_departement")
            .agg(
                {
                    "score_global": "mean",
                    "rendement_brut": "mean",
                    "prix_moyen": "mean",
                    "nom_commune": "count",
                }
            )
            .rename(columns={"nom_commune": "nb_communes_attractives"})
        )

        return dept_analysis.sort_values("score_global", ascending=False).to_dict(
            "index"
        )

    def _calculate_portfolio_stats(
        self, filtered_zones: pd.DataFrame, budget_max: float
    ) -> dict:
        """Calcule les statistiques du portefeuille recommandé"""
        portfolio_stats = {"nb_zones_eligibles": len(filtered_zones)}

        if "rendement_brut" in filtered_zones.columns:
            portfolio_stats["rendement_moyen_estime"] = float(
                filtered_zones["rendement_brut"].mean()
            )
        if "prix_moyen" in filtered_zones.columns:
            portfolio_stats["prix_moyen_zone"] = float(
                filtered_zones["prix_moyen"].mean()
            )
            min_ratio = filtered_zones["prix_moyen"].min() / budget_max * 100
            max_ratio = filtered_zones["prix_moyen"].max() / budget_max * 100
            portfolio_stats["budget_utilisation"] = (
                f"{min_ratio:.1f}% - {max_ratio:.1f}%"
            )
        if "score_global" in filtered_zones.columns:
            portfolio_stats["score_global_moyen"] = float(
                filtered_zones["score_global"].mean()
            )

        return portfolio_stats

    def generate_personalized_recommendations(
        self,
        zones_data: pd.DataFrame,
        budget_max: float,
        surface_min: float = 30,
        surface_max: float = 120,
        rendement_min: float = 4.0,
    ) -> Dict:
        """
        T032 - Génère des recommandations personnalisées

        Args:
            zones_data: DataFrame avec les zones analysées
            budget_max: Budget maximum de l'investisseur
            surface_min: Surface minimale souhaitée
            surface_max: Surface maximale souhaitée
            rendement_min: Rendement minimum souhaité

        Returns:
            Dictionnaire avec les recommandations personnalisées
        """
        recommendations = {}

        # Filtrage selon les critères
        filtered_zones = self._filter_zones_by_criteria(
            zones_data, budget_max, surface_min, surface_max, rendement_min
        )

        if len(filtered_zones) == 0:
            recommendations["message"] = (
                "Aucune zone ne correspond à vos critères. "
                "Considérez ajuster votre budget ou vos exigences."
            )
            return recommendations

        # Génération des recommandations
        recommendations["top_5_global"] = self._get_top_recommendations(filtered_zones)
        recommendations.update(self._get_strategies_recommendations(filtered_zones))
        recommendations["analyse_departements"] = self._analyze_departments(
            filtered_zones
        )
        recommendations["statistiques_portefeuille"] = self._calculate_portfolio_stats(
            filtered_zones, budget_max
        )

        return recommendations

    def create_executive_summary(
        self, recommendations: Dict, zones_data: pd.DataFrame
    ) -> Dict:
        """
        T033 - Crée un résumé exécutif des recommandations

        Args:
            recommendations: Dictionnaire des recommandations
            zones_data: DataFrame avec toutes les zones analysées

        Returns:
            Dictionnaire avec le résumé exécutif
        """
        summary = {}

        # Vue d'ensemble du marché
        market_overview = {
            "total_zones_analysees": len(zones_data),
            "zones_premium": len(
                zones_data[zones_data["categorie_zone"] == "Zone Premium"]
            ),
            "zones_attractives": len(
                zones_data[zones_data["categorie_zone"] == "Zone Attractive"]
            ),
            "rendement_moyen_marche": float(zones_data["rendement_brut"].mean()),
            "prix_m2_moyen_marche": float(zones_data["prix_m2"].mean()),
        }

        summary["vue_ensemble_marche"] = market_overview

        # Opportunités principales
        if "top_5_global" in recommendations:
            top_opportunity = recommendations["top_5_global"][0]

            principales_opportunites = {
                "meilleure_opportunite": {
                    "commune": top_opportunity["nom_commune"],
                    "departement": top_opportunity["code_departement"],
                    "score": top_opportunity["score_global"],
                    "rendement": top_opportunity["rendement_brut"],
                    "prix_moyen": top_opportunity["prix_moyen"],
                },
                "points_forts": [
                    f"Score d'investissement: {top_opportunity['score_global']:.1f}/10",
                    f"Rendement estimé: {top_opportunity['rendement_brut']:.1f}%",
                    f"Catégorie: {top_opportunity['categorie_zone']}",
                ],
            }

            summary["principales_opportunites"] = principales_opportunites

        # Analyse des risques
        risk_analysis = {
            "zones_a_eviter": len(
                zones_data[zones_data["categorie_zone"] == "Zone à Éviter"]
            ),
            "zones_faible_liquidite": len(
                zones_data[zones_data["nb_transactions"] < 10]
            ),
            "zones_rendement_faible": len(zones_data[zones_data["rendement_brut"] < 3]),
            "recommandations_risque": [
                "Privilégier les zones avec plus de 10 transactions annuelles",
                "Éviter les zones avec rendement < 3%",
                "Diversifier géographiquement les investissements",
            ],
        }

        summary["analyse_risques"] = risk_analysis

        # Conseils stratégiques
        strategic_advice = {
            "investisseur_debutant": [
                "Commencer par les zones 'Premium' ou 'Attractives'",
                "Privilégier un rendement de 4-6% pour commencer",
                "Choisir des biens de 50-80m² pour faciliter la location",
            ],
            "investisseur_experimente": [
                "Explorer les zones émergentes avec potentiel",
                "Considérer des rendements de 6%+ pour plus de plus-value",
                "Diversifier sur plusieurs départements",
            ],
            "tendances_marche": [
                f"Rendement moyen du marché: {market_overview['rendement_moyen_marche']:.1f}%",
                f"{market_overview['zones_premium']} zones premium identifiées",
                "Opportunités principalement en périphérie des grandes métropoles",
            ],
        }

        summary["conseils_strategiques"] = strategic_advice

        # Checklist pour l'investisseur
        investor_checklist = {
            "avant_achat": [
                "✓ Vérifier l'état du marché locatif local",
                "✓ Estimer les frais de rénovation nécessaires",
                "✓ Calculer la rentabilité nette (charges comprises)",
                "✓ Vérifier les projets d'aménagement du territoire",
                "✓ Analyser la démographie et l'emploi local",
            ],
            "criteres_selection": [
                "✓ Score d'investissement > 5/10",
                "✓ Rendement brut > 4%",
                "✓ Zone avec > 10 transactions/an",
                "✓ Prix en dessous de la moyenne locale",
                "✓ Surface adaptée au marché locatif (30-120m²)",
            ],
            "apres_achat": [
                "✓ Optimiser la fiscalité (régime micro-BIC ou réel)",
                "✓ Souscrire les assurances appropriées",
                "✓ Mettre en place une gestion locative efficace",
                "✓ Surveiller l'évolution du marché local",
                "✓ Planifier les travaux de maintenance",
            ],
        }

        summary["checklist_investisseur"] = investor_checklist

        return summary
